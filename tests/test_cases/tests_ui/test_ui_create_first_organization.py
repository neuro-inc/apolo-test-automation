import pytest

from tests.test_cases.common_steps.ui_steps.ui_common_steps import UICommonSteps
from tests.reporting_hooks.reporting import async_step, async_title, async_suite


@async_suite("UI Login")
@pytest.mark.asyncio
class TestUICreateFirstOrganization():

    @pytest.fixture(autouse=True)
    async def setup(self, page_manager, data_manager, test_config):
        """
        Initialize shared resources for the test methods.
        """
        self.__page_manager = page_manager
        self.__data_manager = data_manager
        self.__test_config = test_config
        self.ui_common_steps = UICommonSteps(self.__page_manager, self.__test_config, self.__data_manager)

        # Login via UI
        await self.ui_common_steps.ui_login()

    @async_title("Create First Organization via UI")
    async def test_new_user_login(self):
        await self.ui_click_welcome_lets_do_it_button()
        await self.verify_ui_join_organization_page_displayed()
        await self.ui_click_create_organization_button()
        await self.verify_ui_name_organization_page_displayed()
        await self.ui_enter_organization_name("My-organization")
        await self.ui_click_next_button()
        await self.verify_ui_thats_it_page_displayed()
        await self.ui_click_thats_it_lets_do_it_button()
        await self.verify_ui_main_page_displayed()
        await self.verify_ui_create_project_message_displayed("My-organization")
        await self.verify_ui_create_project_button_displayed()

    @async_step("Click the let's do it button on Welcome page")
    async def ui_click_welcome_lets_do_it_button(self):
        await self.__page_manager.welcome_new_user_page.click_lets_do_it_button()

    @async_step("Verify Join organization page displayed")
    async def verify_ui_join_organization_page_displayed(self):
        assert await self.__page_manager.join_organization_page.is_loaded()

    @async_step("Click create organization button")
    async def ui_click_create_organization_button(self):
        await self.__page_manager.join_organization_page.click_create_organization_button()

    @async_step("Verify Name organization page displayed")
    async def verify_ui_name_organization_page_displayed(self):
        assert await self.__page_manager.name_your_organization_page.is_loaded()

    @async_step("Enter organization name")
    async def ui_enter_organization_name(self, gherkin_name):
        organization = self.__data_manager.add_organization(gherkin_name=gherkin_name)
        organization_name = organization.org_name
        page = self.__page_manager.name_your_organization_page
        await page.enter_organization_name(organization_name)

    @async_step("Click next button")
    async def ui_click_next_button(self):
        await self.__page_manager.name_your_organization_page.click_next_button()

    @async_step("Verify That's it page displayed")
    async def verify_ui_thats_it_page_displayed(self):
        assert await self.__page_manager.thats_it_page.is_loaded()

    @async_step("Click lets do it button on That's it page")
    async def ui_click_thats_it_lets_do_it_button(self):
        await self.__page_manager.thats_it_page.click_lets_do_it_button()

    @async_step("Verify Main page is displayed")
    async def verify_ui_main_page_displayed(self):
        assert await self.__page_manager.main_page.is_loaded()

    @async_step("Verify project creation message is displayed")
    async def verify_ui_create_project_message_displayed(self, gherkin_name):
        organization = self.__data_manager.get_organization_by_gherkin_name(gherkin_name)
        page = self.__page_manager.main_page
        assert await page.is_create_first_project_text_field_displayed(organization.org_name)

    @async_step("Verify create project button displayed")
    async def verify_ui_create_project_button_displayed(self):
        assert await self.__page_manager.main_page.is_create_first_project_button_displayed()





