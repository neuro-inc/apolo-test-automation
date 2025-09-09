from tests.reporting_hooks.reporting import async_step
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.test_data import DataManager


class StorageSteps:
    def __init__(
        self,
        test_config: ConfigManager,
        apolo_cli: ApoloCLI,
        data_manager: DataManager,
    ) -> None:
        self._test_config = test_config
        self._apolo_cli = apolo_cli
        self._data_manager = data_manager

    @async_step("Upload file via CLI")
    async def cli_upload_file(self, file_path: str, expected_error: str = "") -> None:
        result, error_message = await self._apolo_cli.storage.upload_file(
            file_path=file_path
        )
        if expected_error:
            assert not result, (
                f"Command should have failed with error: {expected_error}"
            )
            assert error_message == expected_error, (
                f"Expected error: {expected_error}, got: {error_message}"
            )
        else:
            assert result, error_message

    @async_step("Download file via CLI")
    async def cli_download_file(self, src_file_name: str) -> str:
        download_path = self._data_manager.download_path
        result, error_message = await self._apolo_cli.storage.download_file(
            src_file_name=src_file_name, dst_path=download_path
        )
        assert result, error_message
        return f"{download_path}/{src_file_name}"

    @async_step("Rename file via CLI")
    async def cli_rename_file(self, file_name: str, new_file_name: str) -> None:
        result, error_message = await self._apolo_cli.storage.rename_file(
            file_name=file_name, new_file_name=new_file_name
        )
        assert result, error_message

    @async_step("Remove file via CLI")
    async def cli_remove_file(self, file_name: str) -> None:
        result, error_message = await self._apolo_cli.storage.remove_file(
            file_name=file_name
        )
        assert result, error_message

    @async_step("List all files via CLI")
    async def cli_list_all_files(self) -> None:
        result, error_message = await self._apolo_cli.storage.list_all_files()
        assert result, error_message

    @async_step("Create folder via CLI")
    async def cli_create_folder(
        self, folder_name: str, expected_error: str = ""
    ) -> None:
        result, error_message = await self._apolo_cli.storage.create_folder(
            folder_name=folder_name
        )
        if expected_error:
            assert not result, (
                f"Command should have failed with error: {expected_error}"
            )
            assert error_message == expected_error, (
                f"Expected error: {error_message}, got: {error_message}"
            )
        else:
            assert result, error_message

    @async_step("Rename folder via CLI")
    async def cli_rename_folder(self, folder_name: str, new_folder_name: str) -> None:
        result, error_message = await self._apolo_cli.storage.rename_folder(
            folder_name=folder_name, new_folder_name=new_folder_name
        )
        assert result, error_message

    @async_step("Remove folder via CLI")
    async def cli_remove_folder(self, folder_name: str) -> None:
        result, error_message = await self._apolo_cli.storage.remove_folder(
            folder_name=folder_name
        )
        assert result, error_message

    @async_step("Generate bin file")
    async def generate_bin_file(self) -> tuple[str, str]:
        return self._data_manager.generate_dummy_bin_file()

    @async_step("Generate txt file")
    async def generate_txt_file(self) -> tuple[str, str]:
        return self._data_manager.generate_dummy_txt_file()

    @async_step("Validate if downloaded file matches expected file")
    async def validate_file_matches_expected_file(
        self, file_path_1: str, file_path_2: str
    ) -> None:
        assert self._data_manager.compare_files_md5(file_path_1, file_path_2), (
            "MD5 hash does not match!"
        )

    @async_step("Verify folder listed in ls output")
    async def verify_folder_listed(self, folder_name: str) -> None:
        (
            result,
            error_message,
        ) = await self._apolo_cli.storage.verify_folder_listed_in_ls_output(
            folder_name=folder_name
        )
        assert result, error_message

    @async_step("Verify folder not listed in ls output")
    async def verify_folder_not_listed(self, folder_name: str) -> None:
        (
            result,
            error_message,
        ) = await self._apolo_cli.storage.verify_folder_listed_in_ls_output(
            folder_name=folder_name
        )
        assert not result, f"{folder_name} should not have been listed!"

    @async_step("Verify file listed in ls output")
    async def verify_file_listed(self, file_name: str) -> None:
        (
            result,
            error_message,
        ) = await self._apolo_cli.storage.verify_file_listed_in_ls_output(
            file_name=file_name
        )
        assert result, error_message

    @async_step("Verify file not listed in ls output")
    async def verify_file_not_listed(self, file_name: str) -> None:
        (
            result,
            error_message,
        ) = await self._apolo_cli.storage.verify_file_listed_in_ls_output(
            file_name=file_name
        )
        assert not result, f"{file_name} should not have been listed!"
