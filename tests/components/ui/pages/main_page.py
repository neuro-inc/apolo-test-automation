from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def is_loaded(self, organization=None):
        """Returns True if the page is considered loaded (key elements are visible)."""
        return (
            self._get_apps_button().expect_to_be_loaded()
            and self._get_jobs_button().expect_to_be_loaded()
        )

    def _get_apps_button(self):
        return BaseElement(self.page, 'a[href="/apps"]')

    def _get_create_first_project_text_field(self, org_name):
        return BaseElement(self.page, f'p:text("Create project for{org_name}organization")')

    def is_create_first_project_text_field_displayed(self, org_name):
        return self._get_create_first_project_text_field(org_name).is_visible()

    def _get_create_first_project_button(self):
        return BaseElement(self.page, 'button', has_text="Create project")

    def is_create_first_project_button_displayed(self):
        return self._get_create_first_project_button().is_visible()

    def click_apps_button(self):
        self._get_apps_button().click()

    def _get_jobs_button(self):
        return BaseElement(self.page, 'a[href^="/jobs"]')

    def click_jobs_button(self):
        self._get_jobs_button().click()
