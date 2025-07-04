from tests.components.ui.page_manager import PageManager
from tests.test_cases.steps.ui_steps.page_steps_impl.Invited_to_org_page_steps import (
    InvitedToOrgPageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.auth_page_steps import (
    AuthPageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.apps_page_steps import (
    AppsPageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.create_proj_popup_steps import (
    CreateProjPopupSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.edit_org_user_popup_steps import (
    EditOrgUserPopupSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.invite_org_member_popup_steps import (
    InviteOrgMemberPopupSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.invite_proj_member_popup_steps import (
    InviteProjMemberPopupSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.join_org_page_steps import (
    JoinOrgPageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.main_page_steps import (
    MainPageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.name_org_page_steps import (
    NameOrgPageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.no_proj_popup_steps import (
    NoProjPopupSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.org_billing_page_steps import (
    OrgBillingPageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.org_people_page_steps import (
    OrgPeoplePageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.org_settings_page_steps import (
    OrgSettingsPageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.org_settings_popup_steps import (
    OrgSettingsPopupSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.proj_info_popup_steps import (
    ProjInfoPopupSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.proj_people_page_steps import (
    ProjPeoplePageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.remove_org_user_popup_steps import (
    RemoveOrgUserPopupSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.signup_page_steps import (
    SignupPageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.signup_username_page_steps import (
    SignupUsernamePageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.thats_it_page_steps import (
    ThatsItPageSteps,
)
from tests.test_cases.steps.ui_steps.page_steps_impl.welcome_new_user_page_steps import (
    WelcomeNewUserPageSteps,
)
from tests.utils.test_data_management.test_data import DataManager


class PageSteps:
    def __init__(
        self,
        page_manager: PageManager,
        data_manager: DataManager,
    ) -> None:
        self._pm = page_manager
        self._data_manager = data_manager

        self.apps_page = AppsPageSteps(self._pm)
        self.auth_page = AuthPageSteps(self._pm)
        self.create_proj_popup = CreateProjPopupSteps(self._pm)
        self.invite_org_member_popup = InviteOrgMemberPopupSteps(self._pm)
        self.invite_proj_member_popup = InviteProjMemberPopupSteps(self._pm)
        self.invited_to_org_page = InvitedToOrgPageSteps(self._pm)
        self.join_org_page = JoinOrgPageSteps(self._pm)
        self.main_page = MainPageSteps(self._pm, self._data_manager)
        self.name_org_page = NameOrgPageSteps(self._pm, self._data_manager)
        self.no_proj_popup = NoProjPopupSteps(self._pm)
        self.org_people_page = OrgPeoplePageSteps(self._pm)
        self.org_settings_popup = OrgSettingsPopupSteps(self._pm)
        self.proj_info_popup = ProjInfoPopupSteps(self._pm)
        self.proj_people_page = ProjPeoplePageSteps(self._pm)
        self.signup_page = SignupPageSteps(self._pm)
        self.signup_username_page = SignupUsernamePageSteps(self._pm)
        self.thats_it_page = ThatsItPageSteps(self._pm)
        self.welcome_new_user_page = WelcomeNewUserPageSteps(self._pm)
        self.org_settings_page = OrgSettingsPageSteps(self._pm)
        self.org_billing_page = OrgBillingPageSteps(self._pm)
        self.edit_org_user_popup = EditOrgUserPopupSteps(self._pm)
        self.remove_org_user_popup = RemoveOrgUserPopupSteps(self._pm)
