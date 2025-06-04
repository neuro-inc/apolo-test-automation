from tests.reporting_hooks.reporting import async_step
from tests.utils.browser_helper import extract_access_token_from_local_storage


class UICommonSteps:
    def __init__(self, page_manager, test_config, data_manager):
        self.__page_manager = page_manager
        self.__test_config = test_config
        self.__data_manager = data_manager

    @async_step("Login via UI")
    async def ui_login(self):
        await self.__page_manager.auth_page.click_log_in_button()
        await self.__page_manager.login_page.login(self.__test_config)
        assert await self.__page_manager.welcome_new_user_page.is_loaded()
        token = await extract_access_token_from_local_storage(self.__page_manager.login_page.page)
        self.__test_config.auth.token = token

    @async_step("Pass new user onboarding and create first organization via UI")
    async def ui_pass_new_user_onboarding(self, gherkin_name):
        await self.__page_manager.auth_page.click_log_in_button()
        await self.__page_manager.login_page.login(self.__test_config)
        assert await self.__page_manager.welcome_new_user_page.is_loaded()
        token = await extract_access_token_from_local_storage(self.__page_manager.login_page.page)
        self.__test_config.auth.token = token

        await self.__page_manager.page.wait_for_timeout(500)
        await self.__page_manager.welcome_new_user_page.click_lets_do_it_button()
        await self.__page_manager.join_organization_page.click_create_organization_button()

        organization = self.__data_manager.add_organization(gherkin_name=gherkin_name)
        organization_name = organization.org_name
        page = self.__page_manager.name_your_organization_page
        await page.enter_organization_name(organization_name)
        await self.__page_manager.name_your_organization_page.click_next_button()

        await self.__page_manager.page.wait_for_timeout(500)
        await self.__page_manager.welcome_new_user_page.click_lets_do_it_button()