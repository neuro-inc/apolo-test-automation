import pytest

from tests.reporting_hooks.reporting import async_suite, async_title

from tests.test_cases.base_test_class import BaseTestClass


@async_suite("CLI Storage", parent="CLI Tests")
class TestCLIStorage(BaseTestClass):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        self._ui_steps = await self.init_ui_test_steps()
        self._cli_steps = await self.init_cli_test_steps()

        # Verify CLI client installed
        await self._cli_steps.verify_cli_client_installed()

    @async_title("Admin create folder without project created via CLI")
    async def test_admin_create_folder_no_project_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        Verify that:
            - User cannot create folder if there is no project created yet via CLI.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)

        expected_error = "ERROR: The current project is not selected. Please create one with 'apolo admin add-project', or switch to the existing one with 'apolo config switch-project'."
        await self._cli_steps.storage.cli_create_folder(
            folder_name="my_folder", expected_error=expected_error
        )

    @async_title("Admin create folder via CLI")
    async def test_admin_create_folder_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        Verify that:
            - User can create folder via CLI.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )

        await self._cli_steps.storage.cli_create_folder(folder_name="my_folder")
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_folder_listed(folder_name="my_folder")

    @async_title("Admin rename folder via CLI")
    async def test_admin_rename_folder_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Create new folder via CLI.
        Verify that:
            - User can rename folder via CLI.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )

        await self._cli_steps.storage.cli_create_folder(folder_name="my_folder")
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_folder_listed(folder_name="my_folder")
        await self._cli_steps.storage.cli_rename_folder(
            folder_name="my_folder", new_folder_name="new_folder_name"
        )
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_folder_listed(
            folder_name="new_folder_name"
        )

    @async_title("Admin remove folder via CLI")
    async def test_admin_remove_folder_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Create new folder via CLI.
        Verify that:
            - User can remove folder via CLI.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )

        await self._cli_steps.storage.cli_create_folder(folder_name="my_folder")
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_folder_listed(folder_name="my_folder")
        await self._cli_steps.storage.cli_remove_folder(folder_name="my_folder")
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_folder_not_listed(folder_name="my_folder")

    @async_title("Admin upload file without project created via CLI")
    async def test_admin_upload_no_project_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        Verify that:
            - User cannot upload file if there is no project created yet via CLI.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        file_path, file_name = await self._cli_steps.storage.generate_txt_file()

        expected_error = "ERROR: The current project is not selected. Please create one with 'apolo admin add-project', or switch to the existing one with 'apolo config switch-project'."
        await self._cli_steps.storage.cli_upload_file(
            file_path=file_path, expected_error=expected_error
        )

    @async_title("Admin upload text file via CLI")
    async def test_admin_upload_txt_file_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        Verify that:
            - User can upload txt file via CLI.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )
        file_path, file_name = await self._cli_steps.storage.generate_txt_file()

        await self._cli_steps.storage.cli_upload_file(file_path=file_path)
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_file_listed(file_name=file_name)

    @async_title("Admin upload bin file via CLI")
    async def test_admin_upload_bin_file_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        Verify that:
            - User can upload bin file via CLI.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )
        file_path, file_name = await self._cli_steps.storage.generate_bin_file()

        await self._cli_steps.storage.cli_upload_file(file_path=file_path)
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_file_listed(file_name=file_name)

    @async_title("Admin download text file via CLI")
    async def test_admin_download_txt_file_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Upload text file via CLI.
        Verify that:
            - User can download txt file via CLI.
            - downloaded txt file md5 hash matches expected file.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )
        file_path, file_name = await self._cli_steps.storage.generate_txt_file()

        await self._cli_steps.storage.cli_upload_file(file_path=file_path)
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_file_listed(file_name=file_name)

        downloaded_file_path = await self._cli_steps.storage.cli_download_file(
            src_file_name=file_name
        )
        await self._cli_steps.storage.validate_file_matches_expected_file(
            file_path, downloaded_file_path
        )

    @async_title("Admin download bin file via CLI")
    async def test_admin_download_bin_file_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Upload bin file via CLI.
        Verify that:
            - User can download bin file via CLI.
            - downloaded bin file md5 hash matches expected file.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )
        file_path, file_name = await self._cli_steps.storage.generate_bin_file()

        await self._cli_steps.storage.cli_upload_file(file_path=file_path)
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_file_listed(file_name=file_name)

        downloaded_file_path = await self._cli_steps.storage.cli_download_file(
            src_file_name=file_name
        )
        await self._cli_steps.storage.validate_file_matches_expected_file(
            file_path, downloaded_file_path
        )

    @async_title("Admin rename text file via CLI")
    async def test_admin_rename_txt_file_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Upload text file via CLI.
        Verify that:
            - User can rename txt file via CLI.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )
        file_path, file_name = await self._cli_steps.storage.generate_txt_file()

        await self._cli_steps.storage.cli_upload_file(file_path=file_path)
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_file_listed(file_name=file_name)

        await self._cli_steps.storage.cli_rename_file(
            file_name=file_name, new_file_name="new_file_name.txt"
        )
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_file_listed(file_name="new_file_name.txt")

    @async_title("Admin remove text file via CLI")
    async def test_admin_remove_txt_file_cli(self) -> None:
        """
        -Login with valid credentials via UI.
        -Get Bearer auth token from Playwright local storage.
        -Create new organization via API.
        -Login with Bearer auth token via CLI.
        -Create new project via CLI.
        -Upload text file via CLI.
        Verify that:
            - User can remove txt file via CLI.
        """
        user = self._users_manager.main_user
        await self._ui_steps.ui_login(user=user)
        await self._ui_steps.ui_add_org_api(
            token=user.token, gherkin_name="My-organization"
        )

        await self._cli_steps.config.cli_login_with_token(token=user.token)
        org = self._data_manager.get_organization_by_gherkin_name("My-organization")
        proj1 = org.add_project("project 1")
        await self._cli_steps.admin.cli_add_new_project(
            org_name=org.org_name, proj_name=proj1.project_name
        )
        file_path, file_name = await self._cli_steps.storage.generate_txt_file()

        await self._cli_steps.storage.cli_upload_file(file_path=file_path)
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_file_listed(file_name=file_name)

        await self._cli_steps.storage.cli_remove_file(file_name=file_name)
        await self._cli_steps.storage.cli_list_all_files()
        await self._cli_steps.storage.verify_file_not_listed(file_name=file_name)
