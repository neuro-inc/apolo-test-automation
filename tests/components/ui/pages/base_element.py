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
        locator: Optional[Locator] = None,  # 👈 new
        **kwargs: Any,
    ) -> None:
        self.page: Page = page
        self.selector: str = selector or ""
        self.locator: Locator
        self._resolve_method: str = ""
        self._resolve_args: dict[str, Any] = kwargs

        if locator:  # 👈 if locator is passed, use it directly
            self.locator = locator
            self._resolve_method = "direct"
            return

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
            raise ValueError(
                "Provide one of: 'selector', 'by_label', 'by_role', or 'locator'."
            )

    async def expect_to_be_loaded(self, timeout: int = 5000) -> bool:
        try:
            await expect(self.locator).to_be_visible(timeout=timeout)
            return True
        except TimeoutError:
            return False

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
                await self.page.wait_for_timeout(interval)
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

    async def double_click(self) -> None:
        await self.locator.wait_for(state="visible")
        await self.locator.hover()
        await self.locator.click()
        await self.locator.click()

    async def hover(self) -> None:
        await self.locator.hover()
        await self.page.wait_for_timeout(200)

    async def check(self) -> None:
        await self.locator.check()

    async def fill(self, value: str) -> None:
        await self.locator.click()
        await self.locator.fill("")
        await self.locator.fill(value)
        await self.page.wait_for_timeout(200)

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

    async def scroll_half_window(self, container_locator: Locator) -> None:
        """
        Scrolls the given container down by half of its currently displayed window (clientHeight).
        :param container_locator: Locator for the scrollable container.
        """
        try:
            await container_locator.evaluate(
                """el => {
                    const halfWindow = el.clientHeight / 2;
                    el.scrollBy({ top: halfWindow, behavior: "smooth" });
                }"""
            )
        except Exception as e:
            raise e

    async def is_element_in_viewport(self) -> bool:
        """
        Check if the element is at least partially visible
        within the current viewport of the page.
        """
        try:
            box = await self.locator.bounding_box()
            if not box:
                return False

            # Try Playwright's viewport_size first, fallback to JS window size
            viewport_size = self.page.viewport_size
            if not viewport_size:
                viewport_size = await self.page.evaluate(
                    "() => ({ width: window.innerWidth, height: window.innerHeight })"
                )

            vp_width, vp_height = viewport_size["width"], viewport_size["height"]

            # Allow partial overlap instead of full containment
            horizontally_visible = (
                box["x"] + box["width"] > 0  # right edge is past left viewport edge
                and box["x"] < vp_width  # left edge is before right viewport edge
            )
            vertically_visible = (
                box["y"] + box["height"] > 0  # bottom edge is past top viewport edge
                and box["y"] < vp_height  # top edge is before bottom viewport edge
            )

            return horizontally_visible and vertically_visible

        except Exception:
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

    @classmethod
    async def find_all(
        cls,
        page: Page,
        selector: Optional[str] = None,
        *,
        by_label: Optional[str] = None,
        by_role: Optional[str] = None,
        locator: Optional[Locator] = None,  # 👈 support locators
        **kwargs: Any,
    ) -> list["BaseElement"]:
        """
        Return a list of BaseElement instances for all elements matching the locator.
        """
        if locator:
            base_locator = locator
        elif by_label:
            base_locator = page.get_by_label(by_label, **kwargs)
        elif by_role:
            base_locator = page.get_by_role(cast("Any", by_role), **kwargs)
        elif selector:
            base_locator = page.locator(selector, **kwargs)
        else:
            raise ValueError(
                "Provide one of: 'selector', 'by_label', 'by_role', or 'locator'."
            )

        count = await base_locator.count()
        elements = []
        for i in range(count):
            el = cls(page, locator=base_locator.nth(i))  # 👈 direct locator injection
            elements.append(el)

        return elements
