import logging
import re
from typing import Optional

from tests.utils.cli.apolo_components.apolo_runner import ApoloRunner

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloAdmin:
    def __init__(self, runner: ApoloRunner) -> None:
        self._runner = runner
        self._parsed_get_orgs_output: list[str] = []
        self._parsed_get_org_users_output: list[dict[str, str]] = []
        self._parsed_get_proj_users_output: list[dict[str, str]] = []
        self._parsed_get_projects_output: list[dict[str, str]] = []

    @property
    def parsed_get_orgs_output(self) -> list[str]:
        return self._parsed_get_orgs_output

    async def create_organization(self, org_name: str) -> tuple[bool, str]:
        return await self._runner.run_command(
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
        return await self._runner.run_command(
            *arguments,
            action=f"create project {proj_name} under {org_name}",
        )

    async def get_projects(
        self, org_name: str, cluster: str = "default"
    ) -> tuple[bool, str]:
        result, error_message = await self._runner.run_command(
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
        return await self._runner.run_command(
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

    async def get_proj_users(
        self, org_name: str, proj_name: str, cluster: str = "default"
    ) -> tuple[bool, str]:
        result, error_message = await self._runner.run_command(
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
        return await self._runner.run_command(
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
        return await self._runner.run_command(
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
        return await self._runner.run_command(
            *args, action=f"remove organization '{org_name}'"
        )

    async def get_organizations(self) -> list[str]:
        await self._runner.run_command("admin", "get-orgs", action="get organizations")
        organizations: list[str] = []
        lines = (self._runner.last_command_output or "").splitlines()
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

    async def add_user_to_org(
        self, org_name: str, username: str, role: str
    ) -> tuple[bool, str]:
        return await self._runner.run_command(
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
        return await self._runner.run_command(
            "admin",
            "remove-org-user",
            org_name,
            username,
            action=f"remove user {username} from {org_name}",
        )

    async def get_org_users(self, org_name: str) -> tuple[bool, str]:
        result, error_message = await self._runner.run_command(
            "admin", "get-org-users", org_name, action="get org users"
        )
        if result:
            self._parsed_get_org_users_output = self._parse_get_org_users_output()
        return result, error_message

    def _parse_get_org_users_output(self) -> list[dict[str, str]]:
        """
        Parse CLI table output using '│' as column delimiter.
        Returns a list of dicts with username, email, role, credits.
        """
        lines = self._runner.last_command_output.strip().splitlines()
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
        lines = self._runner.last_command_output.strip().splitlines()
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
            for line in self._runner.last_command_output.strip().splitlines()
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
        return await self._runner.run_command(
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
        return await self._runner.run_command(
            *args,
            action=f"remove project '{project_name}' from cluster '{cluster_name}'",
        )

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
