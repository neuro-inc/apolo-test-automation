import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.base_test_class import BaseTestClass


@async_suite("UI Files", parent="UI Tests")
class TestUIFiles(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_ui_test_steps()
        self._steps: UISteps = steps

    @async_title("Verify Writer can create new folder")
    async def test_writer_create_folder(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Signup second user.
        -Invite second user to organization via API.
        -Invite second user to project with Writer role.
        Verify that:
            - Writer can create new folder
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        proj = org.add_project("Project-1")
        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=second_user.email,
            username=second_user.username,
            role="Writer",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_enabled()

        await u2_steps.files_page.ui_click_add_folder_btn()
        await u2_steps.new_folder_popup.verify_ui_popup_displayed()

        await u2_steps.new_folder_popup.ui_enter_folder_name(name="New Folder 1")
        await u2_steps.new_folder_popup.ui_click_create_btn()
        await u2_steps.new_folder_popup.ui_wait_to_disappear()

        await u2_steps.files_page.verify_ui_file_displayed(name="New Folder 1")

    @async_title("Verify Manager can create new folder")
    async def test_manager_create_folder(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Signup second user.
        -Invite second user to organization via API.
        -Invite second user to project with Manager role.
        Verify that:
            - Manager can create new folder
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        proj = org.add_project("Project-1")
        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=second_user.email,
            username=second_user.username,
            role="Manager",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_enabled()

        await u2_steps.files_page.ui_click_add_folder_btn()
        await u2_steps.new_folder_popup.verify_ui_popup_displayed()

        await u2_steps.new_folder_popup.ui_enter_folder_name(name="New Folder 1")
        await u2_steps.new_folder_popup.ui_click_create_btn()
        await u2_steps.new_folder_popup.ui_wait_to_disappear()

        await u2_steps.files_page.verify_ui_file_displayed(name="New Folder 1")

    @async_title("Verify Admin can create new folder")
    async def test_admin_create_folder(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Signup second user.
        -Invite second user to organization via API.
        -Invite second user to project with Admin role.
        Verify that:
            - Admin can create new folder
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)
        u2_steps = await self.init_ui_test_steps()
        second_user = await u2_steps.ui_get_second_user()
        await u2_steps.ui_login(second_user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        await u2_steps.welcome_new_user_page.ui_click_lets_do_it_button()

        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        await steps.ui_add_user_to_org_api(
            user=user,
            org_name=org.org_name,
            username=second_user.username,
            role="User",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.main_page.verify_ui_create_project_message_displayed(
            org.org_name
        )

        proj = org.add_project("Project-1")
        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )
        await steps.ui_invite_user_to_proj(
            org_name=org.org_name,
            proj_name=proj.project_name,
            user_email=second_user.email,
            username=second_user.username,
            role="Admin",
        )

        await u2_steps.ui_reload_page()
        await u2_steps.apps_page.verify_ui_page_displayed()

        await u2_steps.main_page.ui_click_files_btn()
        await u2_steps.files_page.verify_ui_page_displayed()
        await u2_steps.files_page.verify_ui_add_folder_btn_enabled()

        await u2_steps.files_page.ui_click_add_folder_btn()
        await u2_steps.new_folder_popup.verify_ui_popup_displayed()

        await u2_steps.new_folder_popup.ui_enter_folder_name(name="New Folder 1")
        await u2_steps.new_folder_popup.ui_click_create_btn()
        await u2_steps.new_folder_popup.ui_wait_to_disappear()

        await u2_steps.files_page.verify_ui_file_displayed(name="New Folder 1")

    @async_title("User make single click on Folder")
    async def test_folder_single_click(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Create new folder.
        Verify that after single click on folder following elements appear:
            - Folder info section
            - Folder action bar
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        await steps.files_page.ui_click_add_folder_btn()

        await steps.new_folder_popup.ui_enter_folder_name(name="New Folder 1")
        await steps.new_folder_popup.ui_click_create_btn()
        await steps.new_folder_popup.ui_wait_to_disappear()

        await steps.files_page.verify_ui_file_displayed(name="New Folder 1")
        await steps.files_page.ui_click_file_btn(name="New Folder 1")

        path = f"/{org.org_name}/{proj.project_name}"
        await steps.files_page.verify_ui_file_info_section_displayed(
            name="New Folder 1", path=path
        )
        await steps.files_page.verify_ui_file_action_bar_displayed(name="New Folder 1")

    @async_title("User make double click on Folder")
    async def test_folder_double_click(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Create new folder.
        Verify that:
            - User opens a folder with a double click on it.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        await steps.files_page.ui_click_add_folder_btn()

        await steps.new_folder_popup.ui_enter_folder_name(name="New Folder 1")
        await steps.new_folder_popup.ui_click_create_btn()
        await steps.new_folder_popup.ui_wait_to_disappear()

        await steps.files_page.verify_ui_file_displayed(name="New Folder 1")
        await steps.files_page.ui_double_click_file_btn(name="New Folder 1")

        path = f"files/{org.org_name}/{proj.project_name}/New Folder 1"
        await steps.files_page.verify_ui_file_url_path_is_valid(expected_path=path)
        await steps.files_page.verify_ui_folder_up_btn_displayed()

    @async_title("User rename Folder")
    async def test_rename_folder(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Create new folder.
        Verify that:
            - User can rename a folder with Rename button from File action bar.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        await steps.files_page.ui_click_add_folder_btn()

        await steps.new_folder_popup.ui_enter_folder_name(name="New Folder 1")
        await steps.new_folder_popup.ui_click_create_btn()
        await steps.new_folder_popup.ui_wait_to_disappear()

        await steps.files_page.verify_ui_file_displayed(name="New Folder 1")
        await steps.files_page.ui_click_file_btn(name="New Folder 1")

        await steps.files_page.verify_ui_file_action_bar_displayed(name="New Folder 1")
        await steps.files_page.ui_click_rename_file_btn()
        await steps.rename_file_popup.verify_ui_popup_displayed()

        await steps.rename_file_popup.ui_enter_new_file_name(name="Folder 2")
        await steps.rename_file_popup.ui_click_rename_button()
        await steps.rename_file_popup.ui_wait_to_disappear()

        await steps.files_page.verify_ui_file_not_displayed(name="New Folder 1")
        await steps.files_page.verify_ui_file_displayed(name="Folder 2")

    @async_title("User delete Folder")
    async def test_delete_folder(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Create new folder.
        Verify that:
            - User can delete a folder with Delete button from File action bar.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        await steps.files_page.ui_click_add_folder_btn()

        await steps.new_folder_popup.ui_enter_folder_name(name="New Folder 1")
        await steps.new_folder_popup.ui_click_create_btn()
        await steps.new_folder_popup.ui_wait_to_disappear()

        await steps.files_page.verify_ui_file_displayed(name="New Folder 1")
        await steps.files_page.ui_click_file_btn(name="New Folder 1")

        await steps.files_page.verify_ui_file_action_bar_displayed(name="New Folder 1")
        await steps.files_page.ui_click_delete_file_btn()
        await steps.delete_file_popup.verify_ui_popup_displayed(name="New Folder 1")

        await steps.delete_file_popup.ui_click_delete_button()
        await steps.delete_file_popup.ui_wait_to_disappear(name="New Folder 1")

        await steps.files_page.verify_ui_file_not_displayed(name="New Folder 1")

    @async_title("User upload bin file")
    async def test_upload_bin_file(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        Verify that:
            User can upload bin file via UI.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        file_path, file_name = await steps.files_page.generate_bin_file()
        await steps.ui_upload_file(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            file_path=file_path,
        )
        await steps.files_page.verify_ui_file_displayed(name=file_name)

    @async_title("User upload txt file")
    async def test_upload_txt_file(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        Verify that:
            - User can upload txt file via UI.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        file_path, file_name = await steps.files_page.generate_txt_file()
        await steps.ui_upload_file(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            file_path=file_path,
        )
        await steps.files_page.verify_ui_file_displayed(name=file_name)

    @async_title("User make single click on File")
    async def test_file_single_click(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Upload txt file.
        Verify that after single click on file following elements appear:
            - File info section
            - File action bar
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        file_path, file_name = await steps.files_page.generate_txt_file()
        await steps.ui_upload_file(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            file_path=file_path,
        )
        await steps.files_page.verify_ui_file_displayed(name=file_name)

        await steps.files_page.ui_click_file_btn(name=file_name)

        path = f"/{org.org_name}/{proj.project_name}"
        await steps.files_page.verify_ui_file_info_section_displayed(
            name=file_name, path=path
        )
        await steps.files_page.verify_ui_file_action_bar_displayed(name=file_name)

    @async_title("User download bin file")
    async def test_download_bin_file(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Upload bin file.
        Verify that:
            - user can download bin file via UI.
            - downloaded bin file md5 hash matches expected file.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        file_path, file_name = await steps.files_page.generate_bin_file()
        await steps.ui_upload_file(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            file_path=file_path,
        )
        await steps.files_page.verify_ui_file_displayed(name=file_name)

        await steps.files_page.ui_click_file_btn(name=file_name)
        await steps.files_page.verify_ui_file_action_bar_displayed(name=file_name)

        downloaded_file_path = await steps.ui_download_file()
        await steps.validate_file_matches_expected_file(file_path, downloaded_file_path)

    @async_title("User download txt file")
    async def test_download_txt_file(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Upload txt file.
        Verify that:
            - user can download txt file via UI.
            - downloaded bin file md5 hash matches expected file.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        file_path, file_name = await steps.files_page.generate_txt_file()
        await steps.ui_upload_file(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            file_path=file_path,
        )
        await steps.files_page.verify_ui_file_displayed(name=file_name)

        await steps.files_page.ui_click_file_btn(name=file_name)
        await steps.files_page.verify_ui_file_action_bar_displayed(name=file_name)

        downloaded_file_path = await steps.ui_download_file()
        await steps.validate_file_matches_expected_file(file_path, downloaded_file_path)

    @async_title("User rename File")
    async def test_rename_file(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Upload txt file.
        Verify that:
            - User can rename a file with Rename button from File action bar.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        file_path, file_name = await steps.files_page.generate_txt_file()
        await steps.ui_upload_file(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            file_path=file_path,
        )
        await steps.files_page.verify_ui_file_displayed(name=file_name)

        await steps.files_page.ui_click_file_btn(name=file_name)
        await steps.files_page.verify_ui_file_action_bar_displayed(name=file_name)

        await steps.files_page.ui_click_rename_file_btn()
        await steps.rename_file_popup.verify_ui_popup_displayed()

        await steps.rename_file_popup.ui_enter_new_file_name(name="New-file_name.txt")
        await steps.rename_file_popup.ui_click_rename_button()
        await steps.rename_file_popup.ui_wait_to_disappear()

        await steps.files_page.verify_ui_file_not_displayed(name=file_name)
        await steps.files_page.verify_ui_file_displayed(name="New-file_name.txt")

    @async_title("User delete File")
    async def test_delete_file(self) -> None:
        """
        -Login with valid credentials.
        -Create new organization via API.
        -Create new project.
        -Upload txt file.
        Verify that:
            - User can delete a file with Delete button from File action bar.
        """

        steps = self._steps
        user = self._users_manager.main_user
        await steps.ui_login(user)

        await steps.ui_add_org_api(
            token=user.token, gherkin_name="Default-organization"
        )
        org = self._data_manager.get_organization_by_gherkin_name(
            "Default-organization"
        )
        proj = org.add_project("Project-1")

        await steps.ui_create_first_proj_from_top_pane(
            org_name=org.org_name, proj_name=proj.project_name
        )

        await steps.main_page.ui_click_files_btn()
        await steps.files_page.verify_ui_page_displayed()
        await steps.files_page.verify_ui_add_folder_btn_enabled()

        file_path, file_name = await steps.files_page.generate_txt_file()
        await steps.ui_upload_file(
            token=user.token,
            org_name=org.org_name,
            proj_name=proj.project_name,
            file_path=file_path,
        )
        await steps.files_page.verify_ui_file_displayed(name=file_name)

        await steps.files_page.ui_click_file_btn(name=file_name)
        await steps.files_page.verify_ui_file_action_bar_displayed(name=file_name)

        await steps.files_page.ui_click_delete_file_btn()
        await steps.delete_file_popup.verify_ui_popup_displayed(name=file_name)

        await steps.delete_file_popup.ui_click_delete_button()
        await steps.delete_file_popup.ui_wait_to_disappear(name=file_name)

        await steps.files_page.verify_ui_file_not_displayed(name=file_name)
