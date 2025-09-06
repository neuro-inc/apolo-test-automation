import logging
import re

from tests.utils.cli.apolo_components.apolo_runner import ApoloRunner
from tests.utils.test_data_management.disk_data import DiskData

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloDisk:
    def __init__(self, runner: ApoloRunner) -> None:
        self._runner = runner
        self._parsed_create_disk_output: dict[str, str] = {}
        self._parsed_disk_list_output: list[dict[str, str]] = []

    async def create_disk(self, disk: DiskData) -> tuple[bool, str]:
        options = ["--name", disk.name, "--org", disk.org_name]
        if disk.proj_name:
            options.append("--project")
            options.append(disk.proj_name)
        result, error_message = await self._runner.run_command(
            "disk",
            "create",
            *options,
            disk.storage,
            action=f"create disk {disk.name} with storage size {disk.storage}",
        )
        if not result:
            return result, error_message
        else:
            parsed_output = self._parse_create_disk_output()
            self._parsed_create_disk_output = parsed_output
            disk.id = parsed_output["id"]
            disk.uri = parsed_output["uri"]
            return result, error_message

    async def list_disks(self, org_name: str, proj_name: str) -> tuple[bool, str]:
        result, error_message = await self._runner.run_command(
            "disk",
            "ls",
            "--full-uri",
            "--org",
            org_name,
            "--project",
            proj_name,
            "--long-format",
            action="list disks",
        )
        if result:
            self._parsed_disk_list_output = self._parse_disk_list_output()
            return result, error_message
        else:
            return result, error_message

    async def get_disk_by_id(
        self, org_name: str, proj_name: str, disk_id: str
    ) -> tuple[bool, str]:
        result, error_message = await self._runner.run_command(
            "disk",
            "get",
            "--full-uri",
            "--org",
            org_name,
            "--project",
            proj_name,
            disk_id,
            action=f"get disk {disk_id}",
        )
        if not result:
            return result, error_message
        else:
            parsed_output = self._parse_create_disk_output()
            self._parsed_create_disk_output = parsed_output
            return result, error_message

    async def remove_disk(
        self, org_name: str, proj_name: str, disk_id: str
    ) -> tuple[bool, str]:
        return await self._runner.run_command(
            "disk",
            "rm",
            "--org",
            org_name,
            "--project",
            proj_name,
            disk_id,
            action=f"remove disk {disk_id} from {org_name} {proj_name}",
        )

    def _parse_create_disk_output(self) -> dict[str, str]:
        """
        Parse CLI disk details and return only selected fields in snake_case.
        """
        mapping = {
            "Id": "id",
            "Storage": "storage",
            "Uri": "uri",
            "Name": "name",
            "Org name": "org_name",
            "Project name": "proj_name",
            "Owner": "owner",
        }

        result = {}
        for line in self._runner.last_command_output.splitlines():
            if not line.strip():
                continue

            # Split by at least two spaces — keeps multi-word keys like "Org name"
            parts = [p.strip() for p in line.split("  ") if p.strip()]
            if len(parts) == 2:
                key, value = parts
            elif len(parts) == 1:
                key, value = parts[0], ""
            else:
                continue

            if key in mapping:
                result[mapping[key]] = value

        return result

    def verify_create_disk_output(self, disk: DiskData) -> tuple[bool, str]:
        """
        Compare DiskData object attributes to parsed CLI output.
        Returns (True, "") if all match, else (False, diff messages).
        """

        def _normalize_storage(value: str) -> str:
            if not value:
                return ""
            val = (
                value.strip().upper().replace(" ", "")
            )  # normalize case & remove spaces
            # Ensure unit is last 2 characters (e.g., GB, MB, KB, PB)
            unit = val[-2:]
            num_str = val[:-2]
            try:
                num = float(num_str)
                return f"{num:.1f}{unit}"
            except ValueError:
                return val  # fallback if parsing fails

        def _validate_uri(uri: str) -> bool:
            expected_uri = f"disk://default/{disk.org_name}/{disk.proj_name}/{disk.id}"
            return uri.strip() == expected_uri.strip()

        fields_to_check = [
            "id",
            "storage",
            "uri",
            "name",
            "org_name",
            "proj_name",
            "owner",
        ]

        diffs = []
        for field in fields_to_check:
            expected = getattr(disk, field, "")
            actual = self._parsed_create_disk_output.get(field, "")

            if field == "storage":
                if _normalize_storage(expected) != _normalize_storage(actual):
                    diffs.append(f"{field}: expected '{expected}', got '{actual}'")
            elif field == "uri":
                if not _validate_uri(actual):
                    diffs.append(
                        f"{field}: expected 'disk://default/{disk.org_name}/{disk.proj_name}/{disk.id}', got '{actual}'"
                    )
            else:
                if expected != actual:
                    diffs.append(f"{field}: expected '{expected}', got '{actual}'")

        if diffs:
            return False, "; ".join(diffs)
        return True, ""

    def _parse_disk_list_output(self) -> list[dict[str, str]]:
        """
        Parse disk list CLI output and return a list of dicts
        with only selected fields.
        """
        mapping = {
            "Id": "id",
            "Name": "name",
            "Storage": "storage",
            "Uri": "uri",
            "Org name": "org_name",
            "Project name": "proj_name",
        }

        def clean_line(line: str) -> str:
            # Remove ANSI escape codes
            line = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", line)
            # Replace box drawing characters with spaces
            return re.sub(r"[╺╸━│╷╵]", " ", line)

        lines = [
            clean_line(line)
            for line in self._runner.last_command_output.splitlines()
            if line.strip()
        ]
        data = []
        headers = []
        header_index = None
        col_positions = []

        # Find header row and determine column boundaries
        for i, line in enumerate(lines):
            if "Id" in line and "Name" in line and "Storage" in line:
                header_index = i
                headers = re.split(r"\s{2,}", line.strip())
                # Record start positions for each column
                last_pos = 0
                for h in headers:
                    pos = line.index(h, last_pos)
                    col_positions.append(pos)
                    last_pos = pos + len(h)
                col_positions.append(len(line))  # end of last col
                break

        if header_index is None:
            raise ValueError("Header row not found in disk list output.")

        # Process rows after the header + separator
        for row in lines[header_index + 2 :]:
            if not row.strip():
                continue
            cols = [
                row[col_positions[i] : col_positions[i + 1]].strip()
                for i in range(len(headers))
            ]
            row_dict = {}
            for header, col in zip(headers, cols):
                if header in mapping:
                    row_dict[mapping[header]] = col
            if row_dict:
                data.append(row_dict)

        return data

    async def verify_disk_in_list_output(self, disk: DiskData) -> tuple[bool, str]:
        """
        Look up the disk by name in _parsed_list_disks_output and
        verify that id, storage, uri, org_name, proj_name, owner match expected values.
        Returns (True, "") if fields match; else (False, error message).
        """

        parsed_disk = None
        for d in self._parsed_disk_list_output:
            if d.get("name") == disk.name:
                parsed_disk = d
                break

        if not parsed_disk:
            return False, f"Disk '{disk.name}' not found in list"

        def _normalize_storage(value: str) -> str:
            """Normalize storage like 1G / 1.0 GB / 500MB → 1.0GB, 500.0MB, etc."""
            if not value:
                return ""
            val = value.strip().upper().replace(" ", "")
            unit = val[-2:]  # e.g. GB, MB, KB, PB
            num_str = val[:-2]
            try:
                num = float(num_str)
                return f"{num:.1f}{unit}"
            except ValueError:
                return val

        def _validate_uri(uri: str) -> bool:
            expected_uri = f"disk://default/{disk.org_name}/{disk.proj_name}/{disk.id}"
            return uri.strip() == expected_uri.strip()

        errors = []
        # ID
        if parsed_disk.get("id") != disk.id:
            errors.append(f"id: expected '{disk.id}', got '{parsed_disk.get('id')}'")

        if _normalize_storage(parsed_disk.get("storage", "")) != _normalize_storage(
            disk.storage
        ):
            errors.append(
                f"storage: expected '{disk.storage}', got '{parsed_disk.get('storage')}'"
            )

        if not _validate_uri(parsed_disk.get("uri", "")):
            errors.append(
                f"uri: expected 'disk://default/{disk.org_name}/{disk.proj_name}/{disk.id}', got '{parsed_disk.get('uri')}'"
            )

        if parsed_disk.get("org_name") != disk.org_name:
            errors.append(
                f"org_name: expected '{disk.org_name}', got '{parsed_disk.get('org_name')}'"
            )

        if parsed_disk.get("proj_name") != disk.proj_name:
            errors.append(
                f"proj_name: expected '{disk.proj_name}', got '{parsed_disk.get('proj_name')}'"
            )

        if not errors:
            logger.info(
                f"✅ Disk '{disk.name}' fields match: id='{disk.id}', storage='{disk.storage}', "
                f"uri='{parsed_disk.get('uri')}', org_name='{disk.org_name}', proj_name='{disk.proj_name}', owner='{disk.owner}'"
            )
            return True, ""
        else:
            return False, "; ".join(errors)
