import logging
import re
from tests.utils.cli.cli_command_manager import CLICommandManager

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloCLI:
    def __init__(self):
        self.__binary = "apolo"
        self.manager = CLICommandManager(binary=self.__binary)
        self.__login_success = False
        self.__last_command_output = None
        self.__parsed_get_orgs_output = []

    @property
    def parsed_get_orgs_output(self):
        """Returns the parsed output from get_organizations()."""
        return self.__parsed_get_orgs_output

    @property
    def login_successful(self):
        return self.__login_success

    def is_cli_installed(self):
        """
        Verifies if Apolo CLI client is installed by running 'apolo --version'.
        Raises RuntimeError if not installed.
        """
        return self._run_command("--version", action="check CLI version")

    def login_with_token(self, token: str, api_url: str):
        success = self._run_command(
            "config", "login-with-token", token, api_url, action="login-with-token"
        )
        self.__login_success = success
        return success

    def run_job(self, job_name, image, command, wait_for_output_timeout=20):
        base_command = ["run", "--name", job_name, image, "--"]
        command_parts = command.strip().split()
        cli_args = base_command + command_parts

        self._run_command(*cli_args, action=f"run job '{job_name}'", timeout=wait_for_output_timeout)

        job_id_match = re.search(r'Job ID:\s*(job-[\w-]+)', self.__last_command_output)
        logger.info(f"Job ID match: {job_id_match}")
        job_id = job_id_match.group(1) if job_id_match else None
        logger.info(f"Job ID logging: {job_id}")

        if job_id:
            logger.info(f"Extracted Job ID: {job_id}")
        else:
            logger.warning("Job ID not found in output.")

        return job_id

    def create_organization(self, org_name: str):
        """
        Creates a new organization using 'apolo admin add-org <org_name>'.

        Raises RuntimeError if the command fails.
        """
        logger.info(f"Creating organization '{org_name}'")
        return self._run_command("admin", "add-org", org_name, action=f"create organization '{org_name}'")

    def remove_organization(self, org_name: str, force: bool = True):
        """
        Removes an organization using 'apolo admin remove-org <org_name> [--force]'.

        Parameters:
        - org_name: Name of the organization to remove.
        - force: Whether to force removal (default is True).

        Raises RuntimeError if the command fails.
        """
        logger.info(f"Removing organization '{org_name}' (force={force})")
        args = ["admin", "remove-org", org_name]
        if force:
            args.append("--force")
        return self._run_command(*args, action=f"remove organization '{org_name}'")

    def get_organizations(self):
        """
        Fetches and parses organizations using 'apolo admin get-orgs'.
        Parses lines that appear after the header (e.g., 'Name' and separator lines).
        Stores parsed output in self._parsed_get_orgs_output.
        """
        self._run_command("admin", "get-orgs", action="get organizations")

        organizations = []
        lines = self.__last_command_output.splitlines()

        # Find the header line index
        header_index = None
        for i, line in enumerate(lines):
            if re.match(r"^\s*Name\s*$", line):
                header_index = i
                break

        if header_index is not None:
            # Skip the header and separator line
            for line in lines[header_index + 2:]:
                org_name = line.strip()
                if org_name:
                    organizations.append(org_name)

        self.__parsed_get_orgs_output = organizations
        logger.info(f"Fetched organizations: {organizations}")
        return organizations

    def create_project(self, project_name: str, cluster_name="default"):
        """
        Creates a new project using 'apolo admin add-project <cluster_name> <project_name>'.

        Raises RuntimeError if the command fails.
        """
        logger.info(f"Creating project '{project_name}' in cluster '{cluster_name}'")
        return self._run_command("admin", "add-project", cluster_name, project_name,
                                 action=f"create project '{project_name}' in cluster '{cluster_name}'")

    def remove_project(self, cluster_name: str, project_name: str, force: bool = True):
        """
        Removes a project using 'apolo admin remove-project <cluster_name> <project_name> [--force]'.

        Parameters:
        - cluster_name: The name of the cluster containing the project.
        - project_name: The name of the project to remove.
        - force: Whether to force removal (default is True).

        Raises RuntimeError if the command fails.
        """
        logger.info(f"Removing project '{project_name}' from cluster '{cluster_name}' (force={force})")
        args = ["admin", "remove-project", cluster_name, project_name]
        if force:
            args.append("--force")
        return self._run_command(*args, action=f"remove project '{project_name}' from cluster '{cluster_name}'")

    def _run_command(self, *args, action: str, timeout=None):
        """
        Executes a CLI command asynchronously, waits for completion, raises an exception on failure.
        """
        default_timeout = timeout if timeout else 60
        logger.info(f"{action} running command via cli:\n\n{self.__binary} {" ".join(args)}\n")
        self.manager.run_async(*args)
        self.manager.wait(timeout=default_timeout)
        self.__last_command_output = self.manager.get_output()
        error = self.manager.get_error()

        if error:
            error_message = f"{action} failed:\n{error}\n{self.__last_command_output}\n"
            logger.error(error_message)
            raise RuntimeError(error_message)

        logger.info(f"{action} succeeded:\n\n{self.__last_command_output}\n")
        return True

    def verify_login_output(
        self,
        expected_url: str,
        expected_user: str,
        expected_org: str,
        expected_project: str,
    ):
        output = self.__last_command_output
        url_match = re.search(r"Logged into (\S+)", output)
        user_match = re.search(r"as (\S+)", output)
        org_match = re.search(r"org is ([\w-]+)", output)
        project_match = re.search(r"project is ([\w-]+)", output)

        actual_url = url_match.group(1) if url_match else None
        actual_user = user_match.group(1) if user_match else None
        actual_org = org_match.group(1) if org_match else None
        actual_project = project_match.group(1) if project_match else None

        errors = []
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
            raise AssertionError(f"Login verification failed:\n" + "\n".join(errors))
        else:
            logger.info(
                f"\nLogin verification passed for user '{actual_user}' with org '{actual_org}' and project '{actual_project}'"
            )
            return True
