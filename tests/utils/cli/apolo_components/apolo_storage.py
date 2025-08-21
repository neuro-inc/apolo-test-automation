import logging

from tests.utils.cli.apolo_components.apolo_runner import ApoloRunner

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloStorage:
    def __init__(self, runner: ApoloRunner) -> None:
        self._runner = runner
        self._last_ls_output: str = ""

    async def upload_file(self, file_path: str) -> tuple[bool, str]:
        return await self._runner.run_command(
            "storage",
            "cp",
            file_path,
            "storage:",
            action=f"upload {file_path} to storage:",
        )

    async def download_file(
        self, src_file_name: str, dst_path: str
    ) -> tuple[bool, str]:
        return await self._runner.run_command(
            "storage",
            "cp",
            f"storage:{src_file_name}",
            dst_path,
            action=f"download {src_file_name} to {dst_path}",
        )

    async def rename_file(self, file_name: str, new_file_name: str) -> tuple[bool, str]:
        return await self._runner.run_command(
            "storage",
            "mv",
            f"storage:{file_name}",
            f"storage:{new_file_name}",
            action=f"rename {file_name} to {new_file_name}",
        )

    async def remove_file(self, file_name: str) -> tuple[bool, str]:
        return await self._runner.run_command(
            "storage", "rm", f"storage:{file_name}", action=f"remove {file_name}"
        )

    async def create_folder(self, folder_name: str) -> tuple[bool, str]:
        return await self._runner.run_command(
            "storage",
            "mkdir",
            f"storage:{folder_name}",
            action=f"create folder {folder_name}",
        )

    async def rename_folder(
        self, folder_name: str, new_folder_name: str
    ) -> tuple[bool, str]:
        return await self._runner.run_command(
            "storage",
            "mv",
            f"storage:{folder_name}",
            f"storage:{new_folder_name}",
            action=f"rename {folder_name} to {new_folder_name}",
        )

    async def remove_folder(self, folder_name: str) -> tuple[bool, str]:
        return await self._runner.run_command(
            "storage",
            "rm",
            "-r",
            f"storage:{folder_name}",
            action=f"delete {folder_name}",
        )

    async def list_all_files(self) -> tuple[bool, str]:
        result, error_message = await self._runner.run_command(
            "storage", "ls", "-l", action="list all files"
        )
        self._last_ls_output = self._runner.last_command_output
        return result, error_message

    async def verify_folder_listed_in_ls_output(
        self, folder_name: str
    ) -> tuple[bool, str]:
        """
        Parse output like: 'dm  0  2025-08-11 23:29:47  my_folder'
        and check if it is a directory and the name matches.
        Returns (True, "") if ok, else (False, reason).
        """
        if not self._last_ls_output.strip():
            return False, "No entries found"

        parts = self._last_ls_output.strip().split()
        if len(parts) < 5:
            return False, "Invalid format"

        file_type = parts[0]
        is_dir = file_type.startswith("d")
        name = parts[-1]

        if not is_dir:
            return False, f"Not a directory (type: {file_type})"

        if name != folder_name:
            return False, f"Name mismatch: expected '{folder_name}', got '{name}'"

        return True, ""

    async def verify_file_listed_in_ls_output(self, file_name: str) -> tuple[bool, str]:
        """
        Parse output like: 'dm  0  2025-08-11 23:29:47  my_folder'
        and check if it is a directory and the name matches.
        Returns (True, "") if ok, else (False, reason).
        """
        if not self._last_ls_output.strip():
            return False, "No entries found"

        parts = self._last_ls_output.strip().split()
        if len(parts) < 5:
            return False, "Invalid format"

        file_type = parts[0]
        is_file = file_type.startswith("-")
        name = parts[-1]

        if not is_file:
            return False, f"Not a file (type: {file_type})"

        if name != file_name:
            return False, f"Name mismatch: expected '{file_name}', got '{name}'"

        return True, ""
