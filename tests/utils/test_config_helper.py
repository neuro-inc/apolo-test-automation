from typing import Optional

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
        if not isinstance(config, DictConfig):
            raise ValueError("Config root must be a DictConfig (mapping), not a list.")

        # Perform manual interpolation
        base_api_url = str(config.get("base_api_url", ""))

        if "cli_login_url" in config:
            config.cli_login_url = str(config.cli_login_url).replace(
                "${base_api_url}", base_api_url
            )

        if "endpoints" in config:
            for key, value in config.endpoints.items():
                if isinstance(value, str) and "${base_api_url}" in value:
                    config.endpoints[key] = value.replace(
                        "${base_api_url}", base_api_url
                    )

        self._config: DictConfig | ListConfig = config
        self._context: Optional[BrowserContext] = None
        self._token: Optional[str] = None
        self._clean_up_token: Optional[str] = None

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
        if not self._token:
            self._token = value

    @property
    def cleanup_token(self) -> str:
        if self._clean_up_token is None:
            raise ValueError("Clean up token has not been set.")
        return self._clean_up_token

    @cleanup_token.setter
    def cleanup_token(self, value: str) -> None:
        if not self._clean_up_token:
            self._clean_up_token = value

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
    def _endpoints(self) -> DictConfig:
        return DictConfig(self._config.endpoints)

    def get_template_url(self, organization: str, project_name: str) -> str:
        return str(self._endpoints.templates).format(
            organization=organization, project=project_name
        )

    def get_signup_status_url(self, email: str) -> str:
        return str(self._endpoints.signup_status).format(email=email)

    def get_file_upload_url(
        self, organization: str, project_name: str, file_name: str
    ) -> str:
        return str(self._endpoints.file_upload).format(
            organization=organization, project=project_name, file_name=file_name
        )

    def get_orgs_url(self) -> str:
        return str(self._endpoints.get_orgs)

    def get_delete_org_url(self, org_name: str) -> str:
        return str(self._endpoints.delete_org).format(org_name=org_name)

    def get_add_user_to_org_url(self, org_name: str) -> str:
        return str(self._endpoints.add_user_to_org).format(org_name=org_name)

    def get_add_org_url(self) -> str:
        return str(self._endpoints.add_org)

    def get_add_proj_url(self, org_name: str) -> str:
        return str(self._endpoints.add_proj).format(org_name=org_name)

    def get_app_output_url(self, org_name: str, proj_name: str, app_id: str) -> str:
        return str(self._endpoints.app_output).format(
            org_name=org_name, proj_name=proj_name, app_id=app_id
        )

    def get_app_events_url(self, org_name: str, proj_name: str, app_id: str) -> str:
        return str(self._endpoints.app_events).format(
            org_name=org_name, proj_name=proj_name, app_id=app_id
        )

    def get_instances_url(self, org_name: str, proj_name: str) -> str:
        return str(self._endpoints.instances).format(
            org_name=org_name, proj_name=proj_name
        )
