import aiofiles
import yaml
from typing import Any, Optional

from omegaconf import DictConfig, ListConfig, OmegaConf
from playwright.async_api import BrowserContext


class ConfigManager:
    def __init__(self, path_to_config: str) -> None:
        """
        Initialize the ConfigManager.
        Args:
            path_to_config (str): Path to the YAML config file.
        """
        config = OmegaConf.load(path_to_config)
        if not isinstance(config, (DictConfig, ListConfig)):
            raise ValueError(
                "Unsupported YAML root type: expected DictConfig or ListConfig"
            )
        self._config: DictConfig | ListConfig = config
        self._context: Optional[BrowserContext] = None
        self._token: Optional[str] = None

    async def read_config(self, path_to_config: str) -> dict[str, Any]:
        async with aiofiles.open(path_to_config) as f:
            content = await f.read()
            loaded = yaml.safe_load(content)
            return dict(loaded) if isinstance(loaded, dict) else {}

    @property
    def context(self) -> BrowserContext:
        if self._context is None:
            raise ValueError("Browser context has not been set.")
        return self._context

    @context.setter
    def context(self, value: BrowserContext) -> None:
        self._context = value

    @property
    def token(self) -> str:
        if self._token is None:
            raise ValueError("Token has not been set.")
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        self._token = value

    @property
    def env(self) -> str:
        return str(self._config.env)

    @property
    def base_url(self) -> str:
        return str(self._config.base_url)

    @property
    def cli_login_url(self) -> str:
        return str(self._config.cli_login_url)

    @property
    def auth(self) -> DictConfig:
        return DictConfig(self._config.auth)

    @property
    def project(self) -> DictConfig:
        return DictConfig(self._config.project)

    @property
    def endpoints(self) -> DictConfig:
        return DictConfig(self._config.endpoints)

    def get_template_url(
        self, organization: Optional[str] = None, project_name: Optional[str] = None
    ) -> str:
        project_cfg = DictConfig(self._config.project)
        organization = organization if organization else str(project_cfg.organization)
        project_name = project_name if project_name else str(project_cfg.name)
        return str(self.endpoints.templates).format(
            organization=organization, project=project_name
        )
