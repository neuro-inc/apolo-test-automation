from typing import Any
from playwright.async_api import Page
from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class OrganizationBillingPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    async def is_loaded(self, **kwargs: Any) -> bool:
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page loaded")
        return await self._get_clusters_btn().is_visible()

    def _get_clusters_btn(self) -> BaseElement:
        return BaseElement(self.page, by_role="button", name="All Clusters")
