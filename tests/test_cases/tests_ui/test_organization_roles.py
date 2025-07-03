import pytest

from tests.reporting_hooks.reporting import async_suite, async_title
from tests.test_cases.steps.ui_steps.ui_steps import UISteps
from tests.test_cases.tests_ui.base_ui_test import BaseUITest


@async_suite("UI Organization Roles")
class TestUIOrganizationStructureSetup(BaseUITest):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        """
        Initialize shared resources for the test methods.
        """
        steps = await self.init_test_steps()
        self._steps: UISteps = steps
        self._user = self._users_manager.default_user

    @async_title("Verify invited User permissions")
    async def test_invited_user_permissions(self) -> None:
        """
        Verify that invited member with USER role:
            - Cannot access organization Settings
            - Cannot access organization Billing
            - Cannot invite member to organization
            - Cannot delete members from organization
            - Cannot edit organization members
        """

        user = self._user
        steps = self._steps
        add_steps = await self.init_test_steps()
        self.log("User1 login")
        await steps.ui_login(
            email=user.email,
            password=user.password,
        )
        self.log("User1 pass new user onboarding and create organization")
        await steps.ui_pass_new_user_onboarding(
            gherkin_name="Default-organization",
        )

        self.log("User2 Login")
        add_user = await add_steps.ui_signup_new_user_ver_link()
        self.log("User2 password new user onboarding and create organization")
        await add_steps.ui_pass_new_user_onboarding(gherkin_name="new-organization")

        self.log("User1 invite User2 to organization")
        await steps.ui_invite_user_to_org(
            email=user.email, username=user.username, add_user_email=add_user.email
        )

        self.log("User2 reload page")
        await add_steps.ui_reload_page()
        org = self._data_manager.get_organization_by_gherkin_name(
            gherkin_name="Default-organization"
        )
        self.log("User2 accepts invitation to organization")
        await add_steps.ui_accept_invite_to_org(
            org_name=org.org_name, email=add_user.email, role="User"
        )
