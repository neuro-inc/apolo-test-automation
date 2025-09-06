import logging

from tests.utils.cli.apolo_components.apolo_runner import ApoloRunner

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloSecret:
    def __init__(self, runner: ApoloRunner) -> None:
        self._runner = runner
        self._parsed_list_secrets_output: list[dict[str, str]] = []

    async def create_secret(
        self, secret_name: str, secret_value: str
    ) -> tuple[bool, str]:
        return await self._runner.run_command(
            "secret",
            "add",
            secret_name,
            secret_value,
            action=f"create secret {secret_name} with value {secret_value}",
        )

    async def list_secrets(self) -> tuple[bool, str]:
        result, error_message = await self._runner.run_command(
            "secret",
            "ls",
            # "--full-uri",
            action="list secrets",
        )
        self._parsed_list_secrets_output = self._parse_list_secrets_output()
        return result, error_message

    async def remove_secret(self, secret_name: str) -> tuple[bool, str]:
        return await self._runner.run_command(
            "secret",
            "rm",
            secret_name,
            action=f"remove secret {secret_name}",
        )

    def _parse_list_secrets_output(self) -> list[dict[str, str]]:
        """
        Parses CLI-like table output into a list of dictionaries.
        Returns:
            list[dict]: A list of dictionaries with keys: key, org_name, project_name.
        """
        lines = self._runner.last_command_output.strip().split("\n")

        # Skip header and separator lines
        data_lines = [
            line.strip()
            for line in lines
            if line.strip() and not line.startswith("━") and not line.startswith("Key")
        ]

        result = []
        for line in data_lines:
            parts = line.split()
            if len(parts) >= 3:
                key_value = parts[0].replace("secret:", "", 1)
                result.append(
                    {"key": key_value, "org_name": parts[1], "project_name": parts[2]}
                )

        return result

    async def verify_secret_in_list_output(
        self, key: str, org_name: str, proj_name: str
    ) -> tuple[bool, str]:
        """
        Look up the secret by key in _parsed_list_secrets_output and
        verify that key, org_name, project_name match expected values.

        Args:
            key (str): The expected secret key (already without 'secret:' prefix).
            org_name (str): The expected organization name.
            proj_name (str): The expected project name.

        Returns:
            tuple[bool, str]: (True, "") if matches; (False, error_message) otherwise.
        """

        parsed_secret = None
        for s in self._parsed_list_secrets_output:
            if s.get("key") == key:
                parsed_secret = s
                break

        if not parsed_secret:
            return False, f"Secret with key '{key}' not found in list"

        errors = []

        if parsed_secret.get("key") != key:
            errors.append(f"key: expected '{key}', got '{parsed_secret.get('key')}'")

        if parsed_secret.get("org_name") != org_name:
            errors.append(
                f"org_name: expected '{org_name}', got '{parsed_secret.get('org_name')}'"
            )

        if parsed_secret.get("project_name") != proj_name:
            errors.append(
                f"project_name: expected '{proj_name}', got '{parsed_secret.get('project_name')}'"
            )

        if not errors:
            logger.info(
                f"✅ Secret '{key}' fields match: key='{key}', org_name='{org_name}', project_name='{proj_name}'"
            )
            return True, ""
        else:
            return False, "; ".join(errors)
