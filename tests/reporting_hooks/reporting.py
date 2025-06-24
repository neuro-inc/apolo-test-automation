from __future__ import annotations

import os
import uuid
from collections.abc import Awaitable
from collections.abc import Callable
import inspect
import logging
from functools import wraps
from typing import Any, TypeVar

import allure

from tests.utils.exception_handling.exception_manager import ExceptionManager
from tests.conftest import SCREENSHOTS_DIR

logger = logging.getLogger("[📘TEST_INFO]")
exception_manager = ExceptionManager(logger=logger)

ReportFunc = TypeVar("ReportFunc", bound=Callable[..., Awaitable[Any]])


def async_step(step_name: str) -> Callable[[ReportFunc], ReportFunc]:
    def decorator(func: ReportFunc) -> Any:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info(f"▶️ STEP started: {step_name}")
            with allure.step(step_name):
                result = None
                page = None
                is_failed = False

                # Try to extract page if it's a UI step
                if "ui_" in func.__name__ and args:
                    self_instance = args[0]
                    page_manager = getattr(self_instance, "_pm", None)
                    if page_manager and hasattr(page_manager, "page"):
                        page = page_manager.page

                try:
                    result = await func(*args, **kwargs)
                    if page:
                        await page.wait_for_load_state("networkidle")
                    logger.info(f"✅ STEP completed: {step_name}")
                    return result

                except Exception as e:
                    is_failed = True
                    logger.error(f"❌ STEP failed: {step_name}")
                    formatted_msg = exception_manager.handle(e, context=step_name)
                    raise AssertionError(formatted_msg) from e

                finally:
                    if page:
                        try:
                            await page._cleanup() # type: ignore[attr-defined]
                            suffix = "fail" if is_failed else "success"
                            screenshot_name = (
                                f"{func.__name__}_{suffix}_{uuid.uuid4().hex[:6]}.png"
                            )
                            screenshot_path = os.path.join(
                                SCREENSHOTS_DIR, screenshot_name
                            )
                            await page.screenshot(path=screenshot_path, full_page=True)
                            with open(screenshot_path, "rb") as image_file:
                                allure.attach(
                                    image_file.read(),
                                    name=f"Screenshot: {step_name} ({suffix})",
                                    attachment_type=allure.attachment_type.PNG,
                                )
                            logger.info(
                                f"📸 Screenshot captured and attached ({suffix}): {screenshot_path}"
                            )
                        except Exception as ss_error:
                            logger.warning(
                                f"⚠️ Could not capture screenshot ({suffix}): {ss_error}"
                            )

        return wrapper

    return decorator


def async_title(title_name: str) -> Callable[[ReportFunc], ReportFunc]:
    def decorator(func: ReportFunc) -> Any:
        @allure.title(title_name)  # type: ignore[misc, no-untyped-call]
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

        return wrapper

    return decorator


def async_suite(suite_name: str) -> Callable[[type[Any]], type[Any]]:
    def decorator(cls: type[Any]) -> type[Any]:
        cls.__allure_suite__ = suite_name
        setattr(cls, "__suite_name__", suite_name)
        cls = allure.suite(suite_name)(cls)  # type: ignore[no-untyped-call]
        suite_logged = {"started": False}
        test_count = sum(1 for a in dir(cls) if a.startswith("test_"))
        results = {"ran": 0, "passed": 0, "failed": 0}

        for attr_name in dir(cls):
            if not attr_name.startswith("test_"):
                continue

            method = getattr(cls, attr_name)
            if not callable(method):
                continue

            if inspect.iscoroutinefunction(method):

                @wraps(method)
                async def wrapped(
                    self: Any,
                    *args: Any,
                    _method: Callable[..., Awaitable[Any]] = method,
                    _name: str = attr_name,
                    **kwargs: Any,
                ) -> Any:
                    if not suite_logged["started"]:
                        logger.info("=" * 60)
                        logger.info(f"📁 SUITE STARTED: {suite_name}")
                        logger.info("=" * 60)
                        suite_logged["started"] = True
                    try:
                        result = await _method(self, *args, **kwargs)
                        results["passed"] += 1
                        return result
                    except Exception as e:
                        results["failed"] += 1
                        raise e
                    finally:
                        results["ran"] += 1
                        if results["ran"] == test_count:
                            logger.info("=" * 60)
                            logger.info(
                                f"📊 SUITE SUMMARY: {results['passed']} passed, "
                                f"{results['failed']} failed"
                            )
                            logger.info("=" * 60)

                setattr(cls, attr_name, wrapped)

        return cls

    return decorator
