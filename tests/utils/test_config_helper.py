import yaml
import aiofiles
from omegaconf import OmegaConf, DictConfig, ListConfig

from playwright.async_api import BrowserContext


class ConfigManager:
    def __init__(self, path_to_config):
        """
        Initialize the ConfigManager.
        Args:
            path_to_config (str): Path to the YAML config file.
        """
        self._config = OmegaConf.load(path_to_config)
        self.__context = None

        if not isinstance(self._config, (DictConfig, ListConfig)):
            raise ValueError("Unsupported YAML root type: expected DictConfig or ListConfig")

    async def read_config(self, path_to_config):
        async with aiofiles.open(path_to_config, "r") as f:
            content = await f.read()
            return yaml.safe_load(content)

    @property
    def context(self) -> BrowserContext:
        """
        Returns:
            BrowserContext: The current Playwright browser context instance.
        Notes:
            This property is intended to store the browser context used in automation tests.
            It allows shared access to Playwright's `BrowserContext` object across different
            parts of the test framework, such as for page creation, cookie handling, or storage state.
        """
        return self.__context

    @context.setter
    def context(self, value: BrowserContext):
        """
        Sets the Playwright browser context for reuse across test modules.

        Args:
            value (BrowserContext): The browser context instance to store.
        """
        self.__context = value

    @property
    def env(self):
        return self._config.env

    @property
    def base_url(self):
        return self._config.base_url

    @property
    def cli_login_url(self):
        return self._config.cli_login_url

    @property
    def auth(self):
        return self._config.auth

    @property
    def project(self):
        return self._config.project

    @property
    def endpoints(self):
        return self._config.endpoints

    def get_template_url(self, organization=None, project_name=None):
        organization = organization if organization else self._config.project.organization
        project_name = project_name if project_name else self._config.project.name
        return self.endpoints.templates.format(
            organization=organization,
            project=project_name
        )
