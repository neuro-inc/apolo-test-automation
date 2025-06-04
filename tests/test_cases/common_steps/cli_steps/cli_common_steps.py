from tests.reporting_hooks.reporting import async_step


class CLICommonSteps:
    def __init__(self, test_config, apolo_cli, data_manager):
        self.__test_config = test_config
        self.__apolo_cli = apolo_cli
        self.__data_manager = data_manager

    @async_step("Login to apolo CLI with access token")
    async def cli_login_with_token(self):
        token = self.__test_config.auth.token
        url = self.__test_config.cli_login_url
        await self.__apolo_cli.login_with_token(token, url)
        assert self.__apolo_cli.login_successful

    @async_step("Verify Apolo CLI client is installed")
    async def verify_cli_client_installed(self):
        assert await self.__apolo_cli.is_cli_installed()

    @async_step("Verify organization_count")
    async def verify_cli_organization_count(self, count):
        organizations = await self.__apolo_cli.get_organizations()
        assert len(organizations) == 0, f"Expected {count} organizations, got {len(organizations)}"

    @async_step("Add new organization via apolo CLI")
    async def cli_add_new_organization(self, gherkin_name):
        organization = self.__data_manager.add_organization(gherkin_name=gherkin_name)
        await self.__apolo_cli.create_organization(org_name=organization.org_name)

    @async_step("Verify organization is listed in the CLI output")
    async def verify_cli_organization_listed(self, gherkin_name):
        created_organizations = await self.__data_manager.get_all_organizations()
        org = next((o for o in created_organizations if o.gherkin_name == gherkin_name), None)
        assert org is not None, f"No organization found with gherkin_name '{gherkin_name}'"

        assert org.org_name in self.__apolo_cli.parsed_get_orgs_output, (
            f"Organization '{org.org_name}' (for gherkin_name '{gherkin_name}') "
            f"not found in CLI output: {self.__apolo_cli.parsed_get_orgs_output}"
        )