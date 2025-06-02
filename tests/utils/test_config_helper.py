import yaml

from box import Box
from playwright.sync_api import BrowserContext


class ConfigManager:
    def __init__(self, path_to_config):
        """
        Initialize the ConfigManager.
        Args:
            path_to_config (str): Path to the YAML config file.
        """
        self._config = Box.from_yaml(filename=path_to_config, default_box=True, default_box_attr=None)

    def read_config(self, path_to_config):
        with open(path_to_config, "r") as f:
            return yaml.safe_load(f)

    @property
    def context(self) -> BrowserContext:
        """
        Returns:
            Any: The current Playwright browser context instance.
        Notes:
            This property is intended to store the browser context used in automation tests.
            It allows shared access to Playwright's `BrowserContext` object across different
            parts of the test framework, such as for page creation, cookie handling, or storage state.
        """
        return self._config.context

    @context.setter
    def context(self, value: BrowserContext):
        """
        Sets the Playwright browser context for reuse across test modules.

        Args:
            value (BrowserContext): The browser context instance to store.
        """
        self._config.context = value

    @property
    def env(self):
        """
        Returns:
            str: The current environment name (e.g., 'dev', 'prod').
        """
        return self._config.env

    @property
    def base_url(self):
        """
        Returns:
            str: The base URL for the UI.
        """
        return self._config.base_url

    @property
    def cli_login_url(self):
        """
        Returns:
            str: The base URL for the test_cli login.
        """
        return self._config.cli_login_url

    @property
    def auth(self):
        """
        Returns:
            Box: Authentication configuration.
        Fields:
            token (str): Bearer token for authenticated API access. Empty by default.
            username (str): Username.
            email (str): Login email.
            password (str): Password for login automation.
        """
        return self._config.auth

    @property
    def project(self):
        """
        Returns:
            Box: Project-specific information.
        Fields:
            organization (str): Organization name.
            name (str): Project name.
        """
        return self._config.project

    @property
    def endpoints(self):
        """
        Returns:
            Box: API endpoint templates.
        Fields:
            templates (str): Templated URL for fetching templates, should be formatted .format(org=..., project=...).
        """
        return self._config.endpoints

    def get_template_url(self, organization=None, project_name=None):
        """
        Returns:
            str: Fully formatted template API URL, with org and project values substituted.
        """
        organization = organization if organization else self._config.project.organization
        project_name = project_name if project_name else self._config.project.name
        return self.endpoints.templates.format(
            organization=organization,
            project=project_name
        )
