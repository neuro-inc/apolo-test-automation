import os

from tests.reporting_hooks.reporting import async_step
from tests.test_cases.steps.ui_steps.page_steps import PageSteps
from tests.utils.api_helper import APIHelper
from tests.utils.browser_helper import extract_access_token_from_local_storage
from tests.components.ui.page_manager import PageManager
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager
from tests.utils.test_data_management.users_manager import UsersManager, UserData


class UISteps(PageSteps):
    def __init__(
        self,
        page_manager: PageManager,
        test_config: ConfigManager,
        data_manager: DataManager,
        users_manager: UsersManager,
        api_helper: APIHelper,
    ) -> None:
        super().__init__(page_manager, data_manager)
        self._pm = page_manager
        self._test_config = test_config
        self._data_manager = data_manager
        self._users_manager = users_manager
        self._api_helper = api_helper

    @async_step("Reload page")
    async def ui_reload_page(self) -> None:
        await self._pm.page.reload()
        await self._pm.page.wait_for_timeout(500)
        await self._pm.main_page.wait_for_spinner()

    @async_step("Wait for timeout")
    async def ui_wait_for_timeout(self, timeout: int) -> None:
        await self._pm.page.wait_for_timeout(timeout)

    @async_step("Verify user email with the activation link")
    async def activate_email_verification_link(self, email: str) -> None:
        needs_verification, url = await self._api_helper.check_user_needs_verification(
            email
        )
        assert needs_verification, f"User {email} does not need verification!!!!"

        await self.main_page.ui_open_url_in_browser(url)

        (
            needs_verification,
            response,
        ) = await self._api_helper.check_user_needs_verification(
            email,
        )
        assert not needs_verification, f"User {email} still needs verification!!!!"
        assert response == "Email already verified", (
            f"User {email} still needs verification!!!!"
        )

    @async_step("Open product base page")
    async def ui_open_product_base_page(self) -> None:
        base_url = self._test_config.base_url
        await self.main_page.ui_open_url_in_browser(base_url)
        await self._pm.page.wait_for_load_state("networkidle")

    @async_step("Login via UI")
    async def ui_login(self, user: UserData) -> None:
        if not user.authorized:
            await self.auth_page.ui_click_login_button()
            await self.login_page.ui_enter_email(email=user.email)
            await self.login_page.ui_enter_password(password=user.password)
            await self.login_page.ui_click_continue_button()
            await self.welcome_new_user_page.verify_ui_page_displayed(email=user.email)
            token = await extract_access_token_from_local_storage(
                self._pm.login_page.page
            )
            user.token = token

    # ********************   Onboarding steps   ****************************
    @async_step("Pass new user onboarding and create first organization via UI")
    async def ui_pass_new_user_onboarding(
        self, user: UserData, gherkin_name: str
    ) -> None:
        await self.welcome_new_user_page.ui_click_lets_do_it_button()
        await self.join_org_page.verify_ui_page_displayed(username=user.username)

        await self.join_org_page.ui_click_create_organization_button()
        await self.name_org_page.verify_ui_page_displayed()

        organization = self._data_manager.add_organization(gherkin_name=gherkin_name)
        org_name = organization.org_name

        await self.name_org_page.ui_enter_organization_name(org_name)
        await self.name_org_page.ui_click_next_button()

        await self.thats_it_page.ui_click_lets_do_it_button()

        await self.main_page.verify_ui_page_displayed()
        user.orgs.append(org_name)

    # ********************   New user signup steps   ****************************
    @async_step("Signup new user via UI and activate email verification link")
    async def ui_signup_new_user_ver_link(self) -> UserData:
        user = self._users_manager.generate_user()
        await self.auth_page.ui_click_signup_button()
        await self.signup_page.ui_enter_email(user.email)
        await self.signup_page.ui_enter_password(user.password)
        await self.signup_page.ui_click_continue_button()
        await self.main_page.verify_ui_email_message_displayed()

        await self.activate_email_verification_link(email=user.email)

        base_url = self._test_config.base_url
        await self.main_page.ui_open_url_in_browser(base_url)
        await self.auth_page.verify_ui_page_displayed()

        await self.auth_page.ui_click_login_button()
        await self.signup_username_page.verify_ui_page_displayed()

        await self.signup_username_page.ui_enter_username(user.username)
        await self.signup_username_page.ui_click_signup_button()
        await self.main_page.verify_ui_terms_of_agreement_displayed()

        await self.main_page.ui_check_agreement_checkbox()
        await self.main_page.ui_click_i_agree_button()
        await self.main_page.ui_wait_user_agreement_disappear()
        await self.ui_wait_for_timeout(3000)
        await self.welcome_new_user_page.verify_ui_page_displayed(email=user.email)

        token = await extract_access_token_from_local_storage(self._pm.login_page.page)
        user.token = token
        user.authorized = True

        return user

    @async_step("Get second user")
    async def ui_get_second_user(self) -> UserData:
        if self._users_manager.second_user:
            return self._users_manager.second_user
        else:
            user = await self.ui_signup_new_user_ver_link()
            self._users_manager.second_user = user
            return user

    @async_step("Get third user")
    async def ui_get_third_user(self) -> UserData:
        if self._users_manager.third_user:
            return self._users_manager.third_user
        else:
            user = await self.ui_signup_new_user_ver_link()
            self._users_manager.third_user = user
            return user

    # ********************   invite user to organization steps   ****************************
    @async_step("Invite user to organization via UI")
    async def ui_invite_user_to_org(
        self, email: str, username: str, add_user_email: str, role: str = "User"
    ) -> None:
        await self.main_page.ui_click_organization_settings_button(email)
        await self.org_settings_popup.verify_ui_popup_displayed(
            email=email, username=username
        )

        await self.org_settings_popup.ui_click_people_button()
        await self.org_people_page.verify_ui_page_displayed()

        await self.org_people_page.ui_click_invite_people_button()
        await self.invite_org_member_popup.verify_ui_popup_displayed()

        await self.invite_org_member_popup.ui_enter_invite_email(email=add_user_email)
        await self.invite_org_member_popup.ui_select_user_role(role=role)
        await self.invite_org_member_popup.verify_ui_invite_user_button_displayed(
            email=add_user_email
        )

        await self.invite_org_member_popup.ui_click_invite_user_button(
            email=add_user_email
        )
        await self.invite_org_member_popup.ui_click_send_invite_button()
        await self.invite_org_member_popup.ui_wait_to_disappear()

    # ********************   Create additional organization steps   ****************************
    @async_step("Create additional organization via UI")
    async def ui_create_add_org(self, email: str, org_name: str) -> None:
        await self.main_page.ui_click_organization_settings_button(email=email)
        await self.org_settings_popup.ui_click_create_new_org_btn()
        await self.create_org_popup.verify_ui_popup_displayed()

        await self.create_org_popup.ui_enter_org_name(org_name)
        await self.create_org_popup.ui_click_create_button()
        await self.create_org_popup.ui_wait_to_disappear()

        await self.main_page.verify_ui_create_project_message_displayed(
            org_name=org_name
        )
        await self.main_page.verify_ui_create_project_button_displayed()

    # ********************   Accept invite to organization steps   ****************************
    @async_step("Accept invite to organization via UI")
    async def ui_accept_invite_to_org(
        self, org_name: str, email: str, role: str
    ) -> None:
        await self.main_page.verify_ui_invite_to_org_displayed(org_name=org_name)

        await self.main_page.ui_click_invite_to_org_button(org_name=org_name)
        await self.main_page.verify_ui_invite_org_info_displayed(org_name=org_name)
        await self.main_page.verify_ui_invite_to_org_role_is_valid(
            org_name=org_name, role=role
        )

        await self.main_page.ui_click_accept_invite_to_org(org_name=org_name)
        await self.main_page.ui_click_organization_settings_button(email=email)
        await self.org_settings_popup.verify_ui_select_org_button_displayed(
            org_name=org_name
        )

        await self.ui_reload_page()

    # ********************   Create project steps   ****************************
    @async_step("Create first project from main page")
    async def ui_create_first_proj_from_main_page(
        self,
        org_name: str,
        proj_name: str,
        default_role: str,
        make_default: bool = False,
    ) -> None:
        await self.main_page.ui_click_create_proj_button_main_page()
        await self.create_proj_popup.verify_ui_popup_displayed(org_name)

        await self.create_proj_popup.ui_enter_proj_name(proj_name)
        await self.create_proj_popup.ui_select_role(default_role)
        if make_default:
            await self.create_proj_popup.ui_click_make_default_checkbox()
        await self.create_proj_popup.ui_click_create_button()
        await self.create_proj_popup.ui_wait_to_disappear(org_name=org_name)

        await self.apps_page.verify_ui_page_displayed()

    @async_step("Invite member to project via UI")
    async def ui_invite_user_to_proj(
        self,
        org_name: str,
        proj_name: str,
        user_email: str,
        username: str,
        role: str,
    ) -> None:
        await self.main_page.ui_click_proj_button_top_pane()
        await self.proj_info_popup.ui_click_people_btn()
        await self.proj_people_page.verify_ui_page_displayed()

        await self.proj_people_page.ui_click_invite_people_proj_people_btn()
        await self.invite_proj_member_popup.verify_ui_popup_displayed(
            org_name=org_name, proj_name=proj_name
        )

        await self.invite_proj_member_popup.ui_enter_user_data(email=user_email)
        await self.invite_proj_member_popup.ui_select_user_role(role=role)
        await self.invite_proj_member_popup.verify_ui_invite_user_btn_displayed(
            email=user_email
        )
        await self.invite_proj_member_popup.verify_ui_invite_bth_disabled()

        await self.invite_proj_member_popup.ui_click_invite_user_btn(email=user_email)
        await self.invite_proj_member_popup.verify_ui_invite_bth_enabled()

        await self.invite_proj_member_popup.ui_click_invite_btn()
        await self.invite_proj_member_popup.ui_wait_to_disappear(
            org_name=org_name, proj_name=proj_name
        )
        await self.proj_people_page.verify_ui_page_displayed()
        await self.proj_people_page.verify_ui_user_displayed_in_users_list(
            username=username
        )
        await self.proj_people_page.verify_ui_user_role(username=username, role=role)

    # ********************   Create project steps   ****************************

    @async_step("Create first project from the top pane on main page")
    async def ui_create_first_proj_from_top_pane(
        self, org_name: str, proj_name: str
    ) -> None:
        await self.main_page.ui_click_proj_button_top_pane()
        await self.no_proj_popup.verify_ui_popup_displayed(org_name)

        await self.no_proj_popup.ui_click_create_new_proj_button()

        await self.create_proj_popup.verify_ui_popup_displayed(org_name)

        await self.create_proj_popup.ui_enter_proj_name(proj_name)
        await self.create_proj_popup.ui_select_role("Reader")
        await self.create_proj_popup.ui_click_create_button()
        await self.create_proj_popup.ui_wait_to_disappear(org_name=org_name)

        await self.main_page.verify_ui_page_displayed()

    # ********************   Upload/Download file steps   ****************************
    @async_step("Upload file via API and reload page")
    async def ui_upload_file(
        self, token: str, org_name: str, proj_name: str, file_path: str
    ) -> None:
        response = await self._api_helper.upload_file(
            token=token,
            organization=org_name,
            project_name=proj_name,
            file_path=file_path,
        )
        assert response.status == 201, (
            f"Expected HTTP 201 response but got {response.status_code}!"
        )
        await self.ui_reload_page()

    @async_step("Download file via UI")
    async def ui_download_file(self) -> str:
        async with self._pm.files_page.page.expect_download() as download_info:
            await self._pm.files_page.click_file_action_bar_download_btn()
        download = await download_info.value

        file_path = os.path.join(
            self._data_manager.download_path, download.suggested_filename
        )
        await download.save_as(file_path)
        return file_path

    @async_step("Validate if downloaded file matches expected file")
    async def validate_file_matches_expected_file(
        self, file_path_1: str, file_path_2: str
    ) -> None:
        assert self._data_manager.compare_files_md5(file_path_1, file_path_2), (
            "MD5 hash does not match!"
        )

    # ********************   Organization API steps   ****************************
    @async_step("Add user to organization via API and reload page")
    async def ui_add_user_to_org_api(
        self, user: UserData, org_name: str, username: str, role: str = "user"
    ) -> None:
        response = await self._api_helper.add_user_to_org(
            token=user.token,
            org_name=org_name,
            username=username,
            role=role.lower(),
        )
        assert response.status == 201, (
            f"Expected HTTP 201 response but got {response.status_code}!"
        )
        await self.ui_reload_page()
        await self.ui_reload_page()
        await self.main_page.ui_click_organization_settings_button(user.email)
        await self.org_settings_popup.verify_ui_popup_displayed(
            email=user.email, username=user.username
        )

        await self.org_settings_popup.ui_click_people_button()
        await self.org_people_page.verify_ui_page_displayed()

    @async_step("Add organization via API and reload page")
    async def ui_add_org_api(self, token: str, gherkin_name: str) -> None:
        organization = self._data_manager.add_organization(gherkin_name=gherkin_name)
        org_name = organization.org_name
        response = await self._api_helper.add_org(
            token=token,
            org_name=org_name,
        )
        assert response.status == 201, (
            f"Expected HTTP 201 response but got {response.status_code}!"
        )
        await self.ui_reload_page()

    # ********************   Secrets steps   ****************************
    @async_step("Create Secret via UI")
    async def ui_create_secret(
        self, secret_name: str, secret_value: str, first_secret: bool = True
    ) -> None:
        await self.main_page.ui_click_secrets_btn()
        await self.secrets_page.verify_ui_page_displayed()
        if first_secret:
            await self.secrets_page.verify_ui_no_secrets_message_displayed()

        await self.secrets_page.ui_click_create_new_secret_btn()
        await self.create_secret_popup.verify_ui_popup_displayed()

        await self.create_secret_popup.ui_enter_secret_name(secret_name)
        await self.create_secret_popup.ui_enter_secret_value(secret_value)
        await self.create_secret_popup.ui_click_create_secret_btn()
        await self.create_secret_popup.ui_wait_to_disappear()
        await self.secrets_page.verify_ui_no_secrets_message_not_displayed()

    # ********************   Secrets steps   ****************************
    @async_step("Create Disk via UI")
    async def ui_create_disk(
        self,
        disk_name: str,
        storage_value: str,
        storage_units: str,
        lifespan_value: str,
        first_disk: bool = True,
    ) -> None:
        await self.main_page.ui_click_disks_btn()
        await self.disks_page.verify_ui_page_displayed()
        if first_disk:
            await self.disks_page.verify_ui_no_disks_message_displayed()

        await self.disks_page.ui_click_create_new_disk_btn()
        await self.create_disk_popup.verify_ui_popup_displayed()

        await self.create_disk_popup.ui_enter_disk_storage_value(storage_value)
        await self.create_disk_popup.ui_select_disk_storage_units(storage_units)
        await self.create_disk_popup.ui_enter_disk_name(disk_name)
        await self.create_disk_popup.ui_enter_disk_lifespan_value(lifespan_value)
        await self.create_disk_popup.ui_click_create_disk_btn()
        await self.create_disk_popup.ui_wait_to_disappear()
