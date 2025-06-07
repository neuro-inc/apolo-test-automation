import logging
import re
from typing import Optional

from tests.utils.cli.cli_command_manager import CLICommandManager

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloCLI:
    def __init__(self) -> None:
        self._binary: str = "apolo"
        self._manager: CLICommandManager = CLICommandManager(binary=self._binary)
        self._login_success: bool = False
        self._last_command_output: Optional[str] = None
        self._parsed_get_orgs_output: list[str] = []

    @property
    def parsed_get_orgs_output(self) -> list[str]:
        return self._parsed_get_orgs_output

    @property
    def login_successful(self) -> bool:
        return self._login_success

    async def is_cli_installed(self) -> bool:
        return await self._run_command("--version", action="check CLI version")

    async def login_with_token(self, token: str, api_url: str) -> bool:
        success = await self._run_command(
            "config", "login-with-token", token, api_url, action="login-with-token"
        )
        self._login_success = success
        return success

    async def run_job(
        self,
        job_name: str,
        image: str,
        command: str,
        wait_for_output_timeout: int = 20,
    ) -> Optional[str]:
        base_command = ["run", "--name", job_name, image, "--"]
        command_parts = command.strip().split()
        cli_args = base_command + command_parts

        await self._run_command(
            *cli_args, action=f"run job '{job_name}'", timeout=wait_for_output_timeout
        )

        job_id_match = re.search(
            r"Job ID:\s*(job-[\w-]+)", self._last_command_output or ""
        )
        logger.info(f"Job ID match: {job_id_match}")
        job_id: Optional[str] = job_id_match.group(1) if job_id_match else None
        logger.info(f"Job ID logging: {job_id}")

        if job_id:
            logger.info(f"Extracted Job ID: {job_id}")
        else:
            logger.warning("Job ID not found in output.")

        return job_id

    async def create_organization(self, org_name: str) -> bool:
        return await self._run_command(
            "admin", "add-org", org_name, action=f"create organization '{org_name}'"
        )

    async def remove_organization(self, org_name: str, force: bool = True) -> bool:
        logger.info(f"Removing organization '{org_name}' (force={force})")
        args = ["admin", "remove-org", org_name]
        if force:
            args.append("--force")
        return await self._run_command(
            *args, action=f"remove organization '{org_name}'"
        )

    async def get_organizations(self) -> list[str]:
        await self._run_command("admin", "get-orgs", action="get organizations")
        organizations: list[str] = []
        lines = (self._last_command_output or "").splitlines()
        header_index: Optional[int] = None
        for i, line in enumerate(lines):
            if re.match(r"^\s*Name\s*$", line):
                header_index = i
                break
        if header_index is not None:
            for line in lines[header_index + 2 :]:
                org_name = line.strip()
                if org_name:
                    organizations.append(org_name)
        self._parsed_get_orgs_output = organizations
        logger.info(f"Fetched organizations: {organizations}")
        return organizations

    async def create_project(
        self, project_name: str, cluster_name: str = "default"
    ) -> bool:
        return await self._run_command(
            "admin",
            "add-project",
            cluster_name,
            project_name,
            action=f"create project '{project_name}' in cluster '{cluster_name}'",
        )

    async def remove_project(
        self, cluster_name: str, project_name: str, force: bool = True
    ) -> bool:
        args = ["admin", "remove-project", cluster_name, project_name]
        if force:
            args.append("--force")
        return await self._run_command(
            *args,
            action=f"remove project '{project_name}' from cluster '{cluster_name}'",
        )

    async def _run_command(
        self, *args: str, action: str, timeout: Optional[int] = None
    ) -> bool:
        default_timeout: int = timeout if timeout else 60
        logger.info(
            f"{action} running command via cli:\n\n{self._binary} {' '.join(args)}\n"
        )

        await self._manager.run_async(*args)
        await self._manager.wait(timeout=default_timeout)

        raw_output = await self._manager.get_output()
        raw_error = await self._manager.get_error()

        def clean_output(text: str) -> str:
            if not text:
                return ""

            ignored_starts = [
                "You are using Apolo Platform Client",
                "You should consider upgrading via the following command:",
            ]

            cleaned_lines: list[str] = []
            skip_block = False
            for line in text.splitlines():
                if any(line.strip().startswith(prefix) for prefix in ignored_starts):
                    skip_block = True
                    continue
                if skip_block and (
                    line.strip().startswith("python -m") or not line.strip()
                ):
                    continue
                skip_block = False
                cleaned_lines.append(line)

            return "\n".join(cleaned_lines)

        self._last_command_output = clean_output(raw_output)
        cleaned_error = clean_output(raw_error)

        if cleaned_error:
            error_message = f"{action} failed:\n\n{cleaned_error}\n{self._last_command_output or ''}\n"
            logger.error(error_message)
            raise RuntimeError(error_message)

        logger.info(f"{action} succeeded:\n\n{self._last_command_output}\n")
        return True

    async def verify_login_output(
        self,
        expected_url: str,
        expected_user: str,
        expected_org: str | None,
        expected_project: str | None,
    ) -> bool:
        output = self._last_command_output or ""
        url_match = re.search(r"Logged into (\S+)", output)
        user_match = re.search(r"as (\S+)", output)
        org_match = re.search(r"org is ([\w-]+)", output)
        project_match = re.search(r"project is ([\w-]+)", output)

        actual_url = url_match.group(1) if url_match else None
        actual_user = user_match.group(1) if user_match else None
        actual_org = org_match.group(1) if org_match else None
        actual_project = project_match.group(1) if project_match else None

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
            f"\nLogin verification passed for user '{actual_user}' with org '{actual_org}' and project '{actual_project}'"
        )
        return True
