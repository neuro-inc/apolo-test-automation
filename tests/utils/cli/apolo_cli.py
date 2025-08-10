import asyncio
import logging
import re
from typing import Optional


from tests.utils.cli.cli_command_manager import CLICommandManager
from tests.utils.test_data_management.disk_data import DiskData

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloCLI:
    def __init__(self) -> None:
        self._binary: str = "apolo"
        self._manager: CLICommandManager = CLICommandManager(binary=self._binary)
        self._login_success: bool = False
        self._last_command_output: str = ""
        self._parsed_get_orgs_output: list[str] = []
        self._parsed_get_org_users_output: list[dict[str, str]] = []
        self._parsed_get_proj_users_output: list[dict[str, str]] = []
        self._parsed_get_projects_output: list[dict[str, str]] = []
        self._parsed_create_disk_output: dict[str, str] = {}
        self._parsed_disk_list_output: list[dict[str, str]] = []

    @property
    def parsed_get_orgs_output(self) -> list[str]:
        return self._parsed_get_orgs_output

    @property
    def login_successful(self) -> bool:
        return self._login_success

    async def is_cli_installed(self) -> tuple[bool, str]:
        return await self._run_command("--version", action="check CLI version")

    async def login_with_token(self, token: str, api_url: str) -> tuple[bool, str]:
        result, error_message = await self._run_command(
            "config", "login-with-token", token, api_url, action="login-with-token"
        )
        self._login_success = result
        return result, error_message

    async def run_job(
        self,
        job_name: str,
        image: str,
        command: str,
        wait_for_output_timeout: int = 60,
    ) -> Optional[str]:
        base_command = ["run", "--name", job_name, image, "--"]
        command_parts = command.strip().split()
        cli_args = base_command + command_parts

        result, error_message = await self._run_command(
            *cli_args, action=f"run job '{job_name}'", timeout=wait_for_output_timeout
        )
        if not result:
            raise RuntimeError(error_message)

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

    async def create_organization(self, org_name: str) -> tuple[bool, str]:
        return await self._run_command(
            "admin", "add-org", org_name, action=f"create organization '{org_name}'"
        )

    async def create_project(
        self,
        org_name: str,
        proj_name: str,
        default_role: str,
        cluster: str = "default",
        default_proj: bool = False,
    ) -> tuple[bool, str]:
        arguments = [
            "admin",
            "add-project",
            "--default-role",
            default_role,
            "--org",
            org_name,
            cluster,
            proj_name,
        ]
        if default_proj:
            arguments.insert(2, "--default")
        return await self._run_command(
            *arguments,
            action=f"create project {proj_name} under {org_name}",
        )

    async def get_projects(
        self, org_name: str, cluster: str = "default"
    ) -> tuple[bool, str]:
        result, error_message = await self._run_command(
            "admin",
            "get-projects",
            "--org",
            org_name,
            cluster,
            action=f"get projects in {org_name}",
        )
        if result:
            self._parsed_get_projects_output = self._parse_get_projects_output()
        return result, error_message

    async def add_proj_user(
        self,
        org_name: str,
        proj_name: str,
        username: str,
        role: str,
        cluster: str = "default",
    ) -> tuple[bool, str]:
        return await self._run_command(
            "admin",
            "add-project-user",
            "--org",
            org_name,
            cluster,
            proj_name,
            username,
            role.lower(),
            action=f"add user {username} to project {proj_name}",
        )

    async def switch_proj(self, proj_name: str) -> tuple[bool, str]:
        return await self._run_command(
            "config",
            "switch-project",
            proj_name,
            action=f"Switch project to '{proj_name}'",
        )

    async def get_proj_users(
        self, org_name: str, proj_name: str, cluster: str = "default"
    ) -> tuple[bool, str]:
        result, error_message = await self._run_command(
            "admin",
            "get-project-users",
            "--org",
            org_name,
            cluster,
            proj_name,
            action=f"get users in '{proj_name}'",
        )
        if result:
            self._parsed_get_proj_users_output = self._parse_get_proj_users_output()
        return result, error_message

    async def remove_proj_user(
        self, org_name: str, proj_name: str, username: str, cluster: str = "default"
    ) -> tuple[bool, str]:
        return await self._run_command(
            "admin",
            "remove-project-user",
            "--org",
            org_name,
            cluster,
            proj_name,
            username,
            action=f"remove user '{username}' in '{proj_name}'",
        )

    async def update_proj_user(
        self,
        org_name: str,
        proj_name: str,
        username: str,
        role: str,
        cluster: str = "default",
    ) -> tuple[bool, str]:
        return await self._run_command(
            "admin",
            "update-project-user",
            "--org",
            org_name,
            cluster,
            proj_name,
            username,
            role.lower(),
            action=f"update user '{username}' role in '{proj_name}' to '{role}'",
        )

    async def remove_organization(
        self, org_name: str, force: bool = True
    ) -> tuple[bool, str]:
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

    async def config_show(self) -> tuple[bool, str]:
        return await self._run_command("config", "show", action="show config info")

    async def switch_org(self, org_name: str) -> tuple[bool, str]:
        return await self._run_command(
            "config", "switch-org", org_name, action=f"switch org to {org_name}"
        )

    async def add_user_to_org(
        self, org_name: str, username: str, role: str
    ) -> tuple[bool, str]:
        return await self._run_command(
            "admin",
            "add-org-user",
            org_name,
            username,
            role,
            action=f"add user {username} to organization {org_name} as {role}",
        )

    async def remove_user_from_org(
        self, org_name: str, username: str
    ) -> tuple[bool, str]:
        return await self._run_command(
            "admin",
            "remove-org-user",
            org_name,
            username,
            action=f"remove user {username} from {org_name}",
        )

    async def get_org_users(self, org_name: str) -> tuple[bool, str]:
        result, error_message = await self._run_command(
            "admin", "get-org-users", org_name, action="get org users"
        )
        if result:
            self._parsed_get_org_users_output = self._parse_get_org_users_output()
        return result, error_message

    async def create_disk(self, disk: DiskData) -> tuple[bool, str]:
        options = ["--name", disk.name, "--org", disk.org_name]
        if disk.proj_name:
            options.append("--project")
            options.append(disk.proj_name)
        result, error_message = await self._run_command(
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
        result, error_message = await self._run_command(
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
        result, error_message = await self._run_command(
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
        return await self._run_command(
            "disk",
            "rm",
            "--org",
            org_name,
            "--project",
            proj_name,
            disk_id,
            action=f"remove disk {disk_id} from {org_name} {proj_name}",
        )

    def _parse_get_org_users_output(self) -> list[dict[str, str]]:
        """
        Parse CLI table output using '│' as column delimiter.
        Returns a list of dicts with username, email, role, credits.
        """
        lines = self._last_command_output.strip().splitlines()
        data_rows = []

        for i, line in enumerate(lines):
            if "Role" in line and "Email" in line and "Credits" in line:
                header_index = i
                break
        else:
            raise ValueError("Table header not found.")

        for row in lines[header_index + 2 :]:
            if (
                not row.strip()
                or row.strip().startswith("╺")
                or row.strip().startswith("━")
            ):
                continue

            cols = [col.strip() for col in row.strip(" │").split("│")]
            if len(cols) < 7:
                continue

            data_rows.append(
                {
                    "username": cols[0],
                    "role": cols[1],
                    "email": cols[2],
                    "credits": cols[5],
                }
            )

        return data_rows

    def _parse_get_proj_users_output(self) -> list[dict[str, str]]:
        """
        Parse CLI table output using '│' as column delimiter.
        Returns a list of dicts with keys: username, role, email.
        """
        lines = self._last_command_output.strip().splitlines()
        data_rows = []

        # Find the header row
        header_index = None
        for i, line in enumerate(lines):
            if (
                "Role" in line
                and "Email" in line
                and "Full name" in line
                and "Registered" in line
            ):
                header_index = i
                break
        if header_index is None:
            raise ValueError("Table header not found.")

        # Parse each data row after the header (skip separators and empty lines)
        for row in lines[header_index + 2 :]:
            if (
                not row.strip()
                or row.strip().startswith("╺")
                or row.strip().startswith("━")
                or row.strip().startswith("╵")
            ):
                continue

            cols = [col.strip() for col in row.strip(" │").split("│")]
            if len(cols) < 5:
                continue

            data_rows.append(
                {
                    "username": cols[0],
                    "role": cols[1],
                    "email": cols[2],
                }
            )

        return data_rows

    def _parse_get_projects_output(self) -> list[dict[str, str]]:
        """
        Parse CLI admin get-projects output into a list of dicts.
        Each dict has keys: proj_name, cluster, org_name, default_role, default_proj
        """
        lines = [
            line
            for line in self._last_command_output.strip().splitlines()
            if line.strip()
        ]
        header_idx = next(
            i
            for i, line in enumerate(lines)
            if "Project name" in line and "Cluster name" in line
        )

        data_lines = []
        for line in lines[header_idx + 2 :]:
            if line.startswith("━"):
                continue
            if line.strip() == "":
                continue
            data_lines.append(line)

        result = []
        for line in data_lines:
            cols = [col.strip() for col in line.split("  ") if col.strip()]
            if len(cols) < 5:
                cols = [col.strip() for col in line.split() if col.strip()]
            if len(cols) == 5:
                result.append(
                    {
                        "proj_name": cols[0],
                        "cluster": cols[1],
                        "org_name": cols[2],
                        "default_role": cols[3],
                        "default_proj": cols[4],
                    }
                )
        return result

    async def set_org_default_credits(
        self, org_name: str, credits_amount: int
    ) -> tuple[bool, str]:
        return await self._run_command(
            "admin",
            "set-org-defaults",
            "--user-default-credits",
            f"{credits_amount}",
            org_name,
            action=f"set default credits to {credits_amount} for {org_name}",
        )

    async def remove_project(
        self, cluster_name: str, project_name: str, force: bool = True
    ) -> tuple[bool, str]:
        args = ["admin", "remove-project", cluster_name, project_name]
        if force:
            args.append("--force")
        return await self._run_command(
            *args,
            action=f"remove project '{project_name}' from cluster '{cluster_name}'",
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

        output = self._last_command_output or ""

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

    async def _run_command(
        self, *args: str, action: str, timeout: Optional[int] = None
    ) -> tuple[bool, str]:
        default_timeout: int = timeout if timeout else 60
        logger.info(
            f"{action}. Running command via cli:\n\n{self._binary} {' '.join(args)}\n"
        )

        try:
            await asyncio.wait_for(
                self._manager.run_async(*args), timeout=default_timeout
            )
            await asyncio.wait_for(self._manager.wait(), timeout=default_timeout)
        except asyncio.TimeoutError:
            if hasattr(self._manager, "kill"):
                self._manager.kill()
            elif hasattr(self._manager, "process") and self._manager.process:
                self._manager.process.kill()
            logger.error(
                f"Command timed out after {default_timeout} seconds and was killed."
            )
            raise Exception(
                f"Command timed out after {default_timeout} seconds and was killed."
            )
        except Exception as exc:
            logger.exception(f"Error running command {args}: {exc}")
            raise

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
            return False, cleaned_error

        logger.info(f"{action} succeeded:\n\n{self._last_command_output}\n")
        return True, ""

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

        output = self._last_command_output or ""

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

    async def verify_user_in_org_users_output(
        self, username: str, role: str, email: str, credits: str | float | int
    ) -> tuple[bool, str]:
        """
        Look up the user by username in _parsed_get_org_users_output and
        verify that role, email, and credits match expected values.
        Returns (True, "") if fields match, else (False, details).
        """
        # Find user by username
        user = None
        for u in self._parsed_get_org_users_output:
            if u.get("username") == username:
                user = u
                break

        if user is None:
            return False, f"User '{username}' not found in list"

        def _credits_equal(a, b) -> bool:  # type: ignore
            def _norm(x: str | float | int) -> None | str | float:
                if x is None:
                    return None
                if isinstance(x, str) and x.strip().lower() == "unlimited":
                    return "unlimited"
                try:
                    return float(x)
                except (ValueError, TypeError):
                    return str(x).strip().lower()

            return _norm(a) == _norm(b)

        errors = []
        if user.get("role") != role.lower():
            errors.append(f"Expected role '{role}', got '{user.get('role')}'")
        if user.get("email") != email:
            errors.append(f"Expected email '{email}', got '{user.get('email')}'")
        if not _credits_equal(user.get("credits"), credits):
            errors.append(f"Expected credits '{credits}', got '{user.get('credits')}'")

        if not errors:
            logger.info(
                f"✅ User '{username}' fields match: role='{role}', email='{email}', credits='{credits}'"
            )
            return True, ""
        else:
            debug_msg = "; ".join(errors)
            return False, debug_msg

    async def verify_user_in_proj_users_output(
        self, username: str, role: str, email: str
    ) -> tuple[bool, str]:
        """
        Look up the user by username in _parsed_get_proj_users_output and
        verify that role and email match expected values.
        Returns (True, "") if fields match, else (False, details).
        """
        # Find user by username
        user = None
        for u in self._parsed_get_proj_users_output:
            if u.get("username") == username:
                user = u
                break

        if user is None:
            return False, f"User '{username}' not found in list"

        errors = []
        if user.get("role") != role.lower():
            errors.append(f"Expected role '{role}', got '{user.get('role')}'")
        if user.get("email") != email:
            errors.append(f"Expected email '{email}', got '{user.get('email')}'")

        if not errors:
            logger.info(
                f"✅ User '{username}' fields match: role='{role}', email='{email}'"
            )
            return True, ""
        else:
            debug_msg = "; ".join(errors)
            return False, debug_msg

    async def verify_get_projects_output(
        self,
        proj_name: str,
        org_name: str,
        default_role: str,
        default_proj: str | bool,
        cluster: str = "default",
    ) -> tuple[bool, str]:
        """
        Look up the project by proj_name in _parsed_get_projects_output and
        verify that org_name, default_role, default_proj, cluster match.
        Returns (True, "") if fields match; else (False, error message).
        """
        # Lookup project by proj_name
        project = None
        for p in self._parsed_get_projects_output:
            if p.get("proj_name") == proj_name:
                project = p
                break

        if not project:
            return False, f"Project '{proj_name}' not found in list"

        def _proj_equal(a, b) -> bool:  # type: ignore
            if isinstance(a, bool):
                a = str(a)
            if isinstance(b, bool):
                b = str(b)
            return str(a).strip().lower() == str(b).strip().lower()

        errors = []
        if project.get("cluster") != cluster:
            errors.append(
                f"Expected cluster '{cluster}', got '{project.get('cluster')}'"
            )
        if project.get("org_name") != org_name:
            errors.append(
                f"Expected org_name '{org_name}', got '{project.get('org_name')}'"
            )
        if project.get("default_role") != default_role:
            errors.append(
                f"Expected default_role '{default_role}', got '{project.get('default_role')}'"
            )
        if not _proj_equal(project.get("default_proj"), default_proj):
            errors.append(
                f"Expected default_proj '{default_proj}', got '{project.get('default_proj')}'"
            )

        if not errors:
            logger.info(
                f"✅ Project '{proj_name}' fields match: cluster='{cluster}', org_name='{org_name}', default_role='{default_role}', default_proj='{default_proj}'"
            )
            return True, ""
        else:
            debug_msg = "; ".join(errors)
            return False, debug_msg

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
        for line in self._last_command_output.splitlines():
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
            for line in self._last_command_output.splitlines()
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
