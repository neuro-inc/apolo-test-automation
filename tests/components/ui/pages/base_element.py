from typing import Optional, Any, cast
from playwright.async_api import Page, Locator, expect

from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class BaseElement:
    def __init__(
        self,
        page: Page,
        selector: Optional[str] = None,
        *,
        by_label: Optional[str] = None,
        by_role: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.page: Page = page
        self.selector: str
        self.locator: Locator
        self._resolve_method: str
        self._resolve_args: dict[str, Any] = kwargs

        if by_label:
            self.selector = by_label
            self._resolve_method = "label"
            self.locator = page.get_by_label(by_label, **kwargs)

        elif by_role:
            self.selector = by_role
            self._resolve_method = "role"
            self.locator = page.get_by_role(cast("Any", by_role), **kwargs)

        elif selector:
            self.selector = selector
            self._resolve_method = "locator"
            self.locator = page.locator(selector, **kwargs)

        else:
            raise ValueError("Provide one of: 'selector', 'by_label', or 'by_role'.")

    async def expect_to_be_loaded(self, timeout: int = 5000) -> bool:
        try:
            await expect(self.locator).to_be_visible(timeout=timeout)
            return True
        except TimeoutError:
            return False

    from playwright.async_api import TimeoutError as PlaywrightTimeoutError

    async def click(self, timeout: int = 10000, interval: int = 500) -> None:
        """
        Attempts to click the element after verifying it is attached, visible, and enabled.

        Parameters
        ----------
        timeout : int
            Max total wait time in milliseconds (default: 10000).
        interval : int
            Wait interval between checks in milliseconds (default: 500).
        """
        elapsed = 0
        last_error = None

        while elapsed < timeout:
            try:
                # Re-resolve locator to avoid stale references
                self.re_resolve()

                await self.locator.wait_for(state="attached", timeout=interval)
                await expect(self.locator).to_be_visible(timeout=interval)
                await expect(self.locator).to_be_enabled(timeout=interval)

                pointer_events = await self.locator.evaluate(
                    "el => getComputedStyle(el).pointerEvents"
                )
                if pointer_events != "none":
                    break
            except (AssertionError, PlaywrightTimeoutError) as e:
                last_error = e
                await self.page.wait_for_timeout(interval)
                elapsed += interval
        else:
            raise TimeoutError(
                f"Element not ready for click after {timeout}ms: {self.locator}\nLast error: {last_error}"
            )

        try:
            await self.locator.click()
        except PlaywrightTimeoutError:
            await self.locator.click(force=True)

    async def check(self) -> None:
        await self.locator.check()

    async def fill(self, value: str) -> None:
        await self.locator.fill(value)

    async def select_option(self, option_name: str) -> None:
        await self.locator.select_option(option_name)

    async def is_visible(self, timeout: int = 5000, interval: int = 500) -> bool:
        """
        Repeatedly checks if element is visible until timeout is reached.
        """
        elapsed = 0
        while elapsed < timeout:
            try:
                await expect(self.locator).to_be_visible(timeout=interval)
                return True
            except AssertionError:
                await self.page.wait_for_timeout(interval)
                elapsed += interval
        return False

    async def is_enabled(self) -> bool:
        return await self.locator.is_enabled()

    async def text_content(self) -> str:
        return await self.locator.inner_text()

    async def wait_for_selector(self, timeout: Optional[int] = None) -> None:
        await self.page.wait_for_selector(self.selector, timeout=timeout)

    async def wait_until_clickable(
        self, timeout: int = 5000, interval: int = 500
    ) -> bool:
        """
        Wait until the element is fully interactable:
        - attached to DOM
        - visible
        - enabled
        - pointer-events is not 'none'

        Returns
        -------
        bool
            True if element became clickable within timeout, otherwise False.
        """
        elapsed = 0
        while elapsed < timeout:
            try:
                await self.locator.wait_for(state="attached", timeout=interval)
                await expect(self.locator).to_be_visible(timeout=interval)
                await expect(self.locator).to_be_enabled(timeout=interval)
                pointer_events = await self.locator.evaluate(
                    "el => getComputedStyle(el).pointerEvents"
                )
                if pointer_events != "none":
                    return True
            except Exception:
                pass

            await self.page.wait_for_timeout(interval)
            elapsed += interval

        return False

    def re_resolve(self) -> None:
        if self._resolve_method == "label":
            self.locator = self.page.get_by_label(self.selector, **self._resolve_args)
        elif self._resolve_method == "role":
            self.locator = self.page.get_by_role(
                cast("Any", self.selector), **self._resolve_args
            )
        elif self._resolve_method == "locator":
            self.locator = self.page.locator(self.selector, **self._resolve_args)
