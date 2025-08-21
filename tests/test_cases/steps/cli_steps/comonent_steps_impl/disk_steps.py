from tests.reporting_hooks.reporting import async_step
from tests.utils.cli.apolo_cli import ApoloCLI
from tests.utils.test_config_helper import ConfigManager
from tests.utils.test_data_management.disk_data import DiskData
from tests.utils.test_data_management.test_data import DataManager


class DiskSteps:
    def __init__(
        self,
        test_config: ConfigManager,
        apolo_cli: ApoloCLI,
        data_manager: DataManager,
    ) -> None:
        self._test_config = test_config
        self._apolo_cli = apolo_cli
        self._data_manager = data_manager

    @async_step("Create disk via CLI")
    async def cli_create_disk(
        self,
        disk: DiskData,
        expected_error: str = "",
    ) -> None:
        result, error_message = await self._apolo_cli.disk.create_disk(
            disk=disk,
        )
        if expected_error:
            assert not result, f"Command should fail with: {expected_error}"
            assert error_message == expected_error, (
                f"Expected: \n{expected_error} \nbut got \n{error_message}"
            )
        else:
            assert result, error_message

    @async_step("Verify disk info output via CLI")
    async def verify_cli_disk_info_output(self, disk: DiskData) -> None:
        result, error_message = self._apolo_cli.disk.verify_create_disk_output(
            disk=disk
        )
        assert result, error_message

    @async_step("List disks via CLI")
    async def cli_list_disks(self, org_name: str, proj_name: str) -> None:
        result, error_message = await self._apolo_cli.disk.list_disks(
            org_name=org_name, proj_name=proj_name
        )
        assert result, error_message

    @async_step("Verify disk in list disks output via CLI")
    async def verify_cli_disk_in_list_disks_output(self, disk: DiskData) -> None:
        result, error_message = await self._apolo_cli.disk.verify_disk_in_list_output(
            disk=disk
        )
        assert result, error_message

    @async_step("Verify disk  not in list disks output via CLI")
    async def verify_cli_disk_not_in_list_disks_output(self, disk: DiskData) -> None:
        result, error_message = await self._apolo_cli.disk.verify_disk_in_list_output(
            disk=disk
        )
        assert not result, f"{disk.id} should not be present in list disks output"

    @async_step("Get disk by ID via CLI")
    async def cli_get_disk_by_id(
        self, org_name: str, proj_name: str, disk_id: str
    ) -> None:
        result, error_message = await self._apolo_cli.disk.get_disk_by_id(
            org_name=org_name, proj_name=proj_name, disk_id=disk_id
        )
        assert result, error_message

    @async_step("Remove disk by ID via CLI")
    async def cli_remove_disk_by_id(
        self, org_name: str, proj_name: str, disk_id: str
    ) -> None:
        result, error_message = await self._apolo_cli.disk.remove_disk(
            org_name=org_name, proj_name=proj_name, disk_id=disk_id
        )
        assert result, error_message
