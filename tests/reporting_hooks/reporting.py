from __future__ import annotations
from collections.abc import Awaitable
from collections.abc import Callable
import time
from threading import Lock
import os
import uuid
import logging
import inspect
from functools import wraps
from typing import Any, TypeVar, cast
from collections.abc import Callable as ABC_Callable

from playwright.async_api import Page

import allure

from tests.utils.exception_handling.exception_manager import ExceptionManager
from tests.conftest import SCREENSHOTS_DIR

logger = logging.getLogger("[📘TEST_INFO]")
exception_manager = ExceptionManager(logger=logger)

ReportFunc = TypeVar("ReportFunc", bound=Callable[..., Awaitable[Any]])

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SLOWEST_STEPS_LOG = os.path.join(PROJECT_ROOT, "reports", "logs", "step_durations.log")

_lock = Lock()


def async_step(step_name: str) -> Callable[[ReportFunc], ReportFunc]:
    def decorator(func: ReportFunc) -> ReportFunc:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            is_failed = False
            resolved_name, page = _resolve_step_name(func, args, step_name)

            logger.info(f"▶️ STEP started: {resolved_name}")
            start_time = time.perf_counter()
            with allure.step(resolved_name):
                try:
                    result = await func(*args, **kwargs)
                    if page:
                        await page.wait_for_load_state("networkidle")
                    return result
                except Exception as e:
                    is_failed = True
                    formatted_msg = exception_manager.handle(e, context=resolved_name)
                    raise AssertionError(formatted_msg) from e
                finally:
                    duration = time.perf_counter() - start_time
                    logger.info(
                        f"✅ STEP completed: {resolved_name} in {duration:.2f}s"
                    )

                    # Log to central file for session analysis
                    with _lock:
                        with open(SLOWEST_STEPS_LOG, "a") as f:
                            f.write(f"{resolved_name} - {duration:.2f}s\n")

                    allure.attach(
                        f"{duration:.2f} seconds",
                        name=f"Step duration - {resolved_name}",
                        attachment_type=allure.attachment_type.TEXT,
                    )

                    if page:
                        await _capture_screenshot(
                            page, resolved_name, func.__name__, is_failed
                        )

            return result

        return cast(ReportFunc, wrapper)

    return decorator


def async_title(title_name: str) -> Callable[[ReportFunc], ReportFunc]:
    def decorator(func: ReportFunc) -> ReportFunc:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info("-" * 60)
            logger.info(f"📝 TEST started: {title_name}")
            logger.info("-" * 60)

            try:
                result = await func(*args, **kwargs)
                logger.info(f"✅ TEST completed: {title_name}")
                return result
            except Exception as e:
                logger.error(f"❌ TEST failed: {title_name}\nException: {e}")
                raise e
            finally:
                logger.info("-" * 60)

        return cast(ReportFunc, allure.title(title_name)(wrapper))  # type: ignore[no-untyped-call]

    return decorator


def async_suite(
    suite_name: str, parent: str | None = None
) -> Callable[[type[Any]], type[Any]]:
    def decorator(cls: type[Any]) -> type[Any]:
        cls.__allure_suite__ = suite_name
        setattr(cls, "__suite_name__", suite_name)
        cls = allure.suite(suite_name)(cls)  # type: ignore[no-untyped-call]

        if parent:
            setattr(cls, "__allure_parent_suite__", parent)
            cls = allure.parent_suite(parent)(cls)  # type: ignore[no-untyped-call]

        suite_logged = {"started": False}
        test_count = sum(1 for a in dir(cls) if a.startswith("test_"))
        results = {"ran": 0, "passed": 0, "failed": 0}

        def wrap_method(
            method: Callable[..., Awaitable[Any]], name: str
        ) -> Callable[..., Awaitable[Any]]:
            @wraps(method)
            async def wrapped(self: Any, *args: Any, **kwargs: Any) -> Any:
                if not suite_logged["started"]:
                    logger.info("=" * 60)
                    logger.info(f"📁 SUITE STARTED: {suite_name}")
                    logger.info("=" * 60)
                    suite_logged["started"] = True
                try:
                    result = await method(self, *args, **kwargs)
                    results["passed"] += 1
                    return result
                except Exception:
                    results["failed"] += 1
                    raise
                finally:
                    results["ran"] += 1
                    if results["ran"] == test_count:
                        logger.info("=" * 60)
                        logger.info(
                            f"📊 SUITE SUMMARY: {results['passed']} passed, {results['failed']} failed"
                        )
                        logger.info("=" * 60)

            return wrapped

        for attr in dir(cls):
            if attr.startswith("test_"):
                method = getattr(cls, attr)
                if inspect.iscoroutinefunction(method):
                    setattr(cls, attr, wrap_method(method, attr))

        return cls

    return decorator


def _resolve_step_name(
    func: ABC_Callable[..., Any], args: tuple[Any, ...], base_name: str
) -> tuple[str, Any | None]:
    """Determine dynamic step name and extract page (if present)."""
    if "ui_" not in func.__name__ or not args:
        return base_name, None

    self_instance = args[0]
    page_manager = getattr(self_instance, "_pm", None)
    if not page_manager:
        return base_name, None

    user_label = getattr(page_manager, "user_label", "main")
    step_name = (
        f"<<{user_label}>> :: {base_name}" if user_label != "main" else base_name
    )
    page = getattr(page_manager, "page", None)
    return step_name, page


async def _capture_screenshot(
    page: Page, step_name: str, func_name: str, is_failed: bool
) -> None:
    """Capture and attach a screenshot to Allure, labeled with pass/fail."""
    suffix = "fail" if is_failed else "success"
    screenshot_name = f"{func_name}_{suffix}_{uuid.uuid4().hex[:6]}.png"
    screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)

    try:
        await page.screenshot(path=screenshot_path, full_page=True)
        with open(screenshot_path, "rb") as f:
            allure.attach(
                f.read(),
                name=f"Screenshot: {step_name} ({suffix})",
                attachment_type=allure.attachment_type.PNG,
            )
        logger.info(
            f"📸 Screenshot captured and attached ({suffix}): {screenshot_path}"
        )
    except Exception as e:
        logger.warning(f"⚠️ Could not capture screenshot ({suffix}): {e}")
