import logging
import re

from tests.utils.cli.apolo_components.apolo_runner import ApoloRunner

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloConfig:
    def __init__(self, runner: ApoloRunner) -> None:
        self._runner = runner
        self.current_token: str = ""

    async def login_with_token(self, token: str, api_url: str) -> tuple[bool, str]:
        result, error_message = await self._runner.run_command(
            "config", "login-with-token", token, api_url, action="login-with-token"
        )
        self.current_token = token
        return result, error_message

    async def switch_proj(self, proj_name: str) -> tuple[bool, str]:
        return await self._runner.run_command(
            "config",
            "switch-project",
            proj_name,
            action=f"Switch project to '{proj_name}'",
        )

    async def config_show(self) -> tuple[bool, str]:
        return await self._runner.run_command(
            "config", "show", action="show config info"
        )

    async def switch_org(self, org_name: str) -> tuple[bool, str]:
        return await self._runner.run_command(
            "config", "switch-org", org_name, action=f"switch org to {org_name}"
        )

    async def verify_config_show_output(
        self,
        expected_username: str,
        expected_org: str,
        expected_cluster: str = "default",
        expected_project: str = "<no-project>",
        expected_org_credit: int = 500,
    ) -> bool:
        """
        Verify CLI config show output contains expected fields.

        Parameters
        ----------
        expected_username : str
            Expected user name in CLI output.
        expected_cluster : str, default="default"
            Expected cluster name.
        expected_org : str
            Expected organization name.
        expected_project : str, default="<no-project>"
            Expected project name.
        expected_org_credit : int, default=500
            Expected org credits quota (will match integer or float).

        Returns
        -------
        bool
            True if all fields match; raises AssertionError otherwise.
        """

        def _normalize(val: str) -> str:
            if val == "":
                return ""
            return val.strip()

        output = self._runner.last_command_output or ""

        user_match = re.search(r"User Name\s+([^\n]+)", output)
        cluster_match = re.search(r"Current Cluster\s+([^\n]+)", output)
        org_match = re.search(r"Current Org\s+([^\n]+)", output)
        project_match = re.search(r"Current Project\s+([^\n]+)", output)
        org_credit_match = re.search(r"Org Credits Quota\s+([^\n]+)", output)

        actual_username = _normalize(user_match.group(1)) if user_match else None
        actual_cluster = _normalize(cluster_match.group(1)) if cluster_match else None
        actual_org = _normalize(org_match.group(1)) if org_match else None
        actual_project = _normalize(project_match.group(1)) if project_match else None
        actual_org_credit = None
        if org_credit_match:
            raw = org_credit_match.group(1).replace(",", "").strip()
            try:
                val = float(raw) if raw.lower() != "unlimited" else None
                actual_org_credit = int(val) if val is not None else None
            except ValueError:
                actual_org_credit = None

        expected_username = _normalize(expected_username)
        expected_cluster = _normalize(expected_cluster)
        expected_org = _normalize(expected_org)
        expected_project = _normalize(expected_project)
        expected_org_credit = (
            int(expected_org_credit) if expected_org_credit is not None else None
        )

        errors: list[str] = []
        if actual_username != expected_username:
            errors.append(
                f"Expected user name '{expected_username}', got '{actual_username}'"
            )
        if actual_cluster != expected_cluster:
            errors.append(
                f"Expected cluster '{expected_cluster}', got '{actual_cluster}'"
            )
        if actual_org != expected_org:
            errors.append(f"Expected org '{expected_org}', got '{actual_org}'")
        if actual_project != expected_project:
            errors.append(
                f"Expected project '{expected_project}', got '{actual_project}'"
            )
        if actual_org_credit != expected_org_credit:
            errors.append(
                f"Expected org credits quota '{expected_org_credit}', got '{actual_org_credit}'"
            )

        if errors:
            raise AssertionError(
                "Config show verification failed:\n" + "\n".join(errors)
            )

        logger.info(
            f"✅ Config show verification passed for user '{actual_username}', cluster '{actual_cluster}', org '{actual_org}', project '{actual_project}', org_credits '{actual_org_credit}'"
        )
        return True

    async def verify_login_output(
        self,
        expected_url: str,
        expected_user: str,
        expected_org: str | None = None,
        expected_project: str | None = None,
    ) -> bool:
        """
        Verify CLI login output contains expected user/org/project info.

        Parameters
        ----------
        expected_url : str
            The expected base URL shown in the CLI output.
        expected_user : str
            Username to match in CLI output.
        expected_org : str | None, default=None
            Expected organization (or None if not assigned).
        expected_project : str | None, default=None
            Expected project (or None if not assigned).

        Returns
        -------
        bool
            True if all fields match; raises AssertionError otherwise.
        """

        def _normalize(value: str | None) -> str | None:
            if value is None or value.strip(".,") == "None":
                return None
            return value.strip(".,").strip()

        output = self._runner.last_command_output or ""

        url_match = re.search(r"Logged into (\S+)", output)
        user_match = re.search(r"as (\S+)", output)
        org_match = re.search(r"org is ([\w\-]+)", output)
        project_match = re.search(r"project is ([\w\-]+)", output)

        actual_url = _normalize(url_match.group(1) if url_match else None)
        actual_user = _normalize(user_match.group(1) if user_match else None)
        actual_org = _normalize(org_match.group(1) if org_match else None)
        actual_project = _normalize(project_match.group(1) if project_match else None)

        expected_org = _normalize(expected_org)
        expected_project = _normalize(expected_project)

        errors: list[str] = []
        if actual_url != expected_url:
            errors.append(f"Expected URL '{expected_url}', got '{actual_url}'")
        if actual_user != expected_user:
            errors.append(f"Expected user '{expected_user}', got '{actual_user}'")
        if actual_org != expected_org:
            errors.append(f"Expected org '{expected_org}', got '{actual_org}'")
        if actual_project != expected_project:
            errors.append(
                f"Expected project '{expected_project}', got '{actual_project}'"
            )

        if errors:
            raise AssertionError("Login verification failed:\n" + "\n".join(errors))

        logger.info(
            f"✅ Login verification passed for user '{actual_user}' with org '{actual_org}' and project '{actual_project}'"
        )
        return True
