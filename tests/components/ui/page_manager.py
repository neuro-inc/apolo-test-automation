from playwright.async_api import Page

from tests.components.ui.pages.apps.choose_secret_popup import ChooseSecretPopup
from tests.components.ui.pages.apps.deep_seek_details_page import DeepSeekDetailsPage
from tests.components.ui.pages.apps.deep_seek_install_page import DeepSeekInstallPage
from tests.components.ui.pages.apps.resource_preset_popup import ResourcePresetPopup
from tests.components.ui.pages.apps.shell_app_page import ShellAppPage
from tests.components.ui.pages.apps.shell_install_page import ShellInstallPage
from tests.components.ui.pages.apps.shell_details_page import ShellDetailsPage
from tests.components.ui.pages.apps_page import AppsPage
from tests.components.ui.pages.auth_page import AuthPage
from tests.components.ui.pages.buy_credits_popup import BuyCreditsPopup
from tests.components.ui.pages.create_disk_popup import CreateDiskPopup
from tests.components.ui.pages.create_organization_popup import CreateOrganizationPopup
from tests.components.ui.pages.create_project_popup import CreateProjectPopup
from tests.components.ui.pages.create_secret_popup import CreateSecretPopup
from tests.components.ui.pages.delete_disk_popup import DeleteDiskPopup
from tests.components.ui.pages.delete_file_popup import DeleteFilePopup
from tests.components.ui.pages.delete_secret_popup import DeleteSecretPopup
from tests.components.ui.pages.disks_page import DisksPage
from tests.components.ui.pages.edit_org_user_popup import EditOrgUserPopup
from tests.components.ui.pages.edit_proj_member_popup import EditProjMemberPopup
from tests.components.ui.pages.files_page import FilesPage
from tests.components.ui.pages.invite_org_member_popup import InviteOrgMemberPopup
from tests.components.ui.pages.invite_project_memeber_popup import InviteProjMemberPopup
from tests.components.ui.pages.jobs_page import JobsPage
from tests.components.ui.pages.login_page import LoginPage
from tests.components.ui.pages.main_page import MainPage
from tests.components.ui.pages.new_folder_popup import NewFolderPopup
from tests.components.ui.pages.no_project_popup import NoProjectPopup
from tests.components.ui.pages.onboarding_pages.invited_to_org_page import (
    InvitedToOrgPage,
)
from tests.components.ui.pages.onboarding_pages.join_organization_page import (
    JoinOrganizationPage,
)
from tests.components.ui.pages.onboarding_pages.name_new_organization_page import (
    NameNewOrganizationPage,
)
from tests.components.ui.pages.onboarding_pages.thats_it_page import ThatsItPage
from tests.components.ui.pages.onboarding_pages.welcome_new_user_page import (
    WelcomeNewUserPage,
)
from tests.components.ui.pages.organization_billing_page import OrganizationBillingPage
from tests.components.ui.pages.organization_people_page import OrganizationPeoplePage
from tests.components.ui.pages.organization_settings_page import (
    OrganizationSettingsPage,
)
from tests.components.ui.pages.organization_settings_popup import (
    OrganizationSettingsPopup,
)
from tests.components.ui.pages.payment_page import PaymentPage
from tests.components.ui.pages.project_people_page import ProjectPeoplePage
from tests.components.ui.pages.projects_info_popup import ProjectsInfoPopup
from tests.components.ui.pages.remove_org_user_popup import RemoveOrgUserPopup
from tests.components.ui.pages.remove_proj_member_popup import RemoveProjMemberPopup
from tests.components.ui.pages.rename_file_popup import RenameFilePopup
from tests.components.ui.pages.secrets_page import SecretsPage
from tests.components.ui.pages.signup_page import SignupPage
from tests.components.ui.pages.signup_username_page import SignupUsernamePage


class PageManager:
    def __init__(self, page: Page):
        self.page = page
        self.user_label = (
            "main"  # flag for reporting additional users(new browser context)
        )

        self.auth_page = AuthPage(page)
        self.login_page = LoginPage(page)
        self.signup_page = SignupPage(page)
        self.signup_username_page = SignupUsernamePage(page)
        self.main_page = MainPage(page)
        self.jobs_page = JobsPage(page)
        self.welcome_new_user_page = WelcomeNewUserPage(page)
        self.join_organization_page = JoinOrganizationPage(page)
        self.name_your_organization_page = NameNewOrganizationPage(page)
        self.invited_to_org_page = InvitedToOrgPage(page)
        self.thats_it_page = ThatsItPage(page)
        self.organization_settings_popup = OrganizationSettingsPopup(page)
        self.organization_people_page = OrganizationPeoplePage(page)
        self.invite_org_member_popup = InviteOrgMemberPopup(page)
        self.create_proj_popup = CreateProjectPopup(page)
        self.no_proj_popup = NoProjectPopup(page)
        self.apps_page = AppsPage(page)
        self.projects_info_popup = ProjectsInfoPopup(page)
        self.project_people_page = ProjectPeoplePage(page)
        self.invite_proj_member_popup = InviteProjMemberPopup(page)
        self.organization_settings_page = OrganizationSettingsPage(page)
        self.organization_billing_page = OrganizationBillingPage(page)
        self.edit_org_user_popup = EditOrgUserPopup(page)
        self.remove_org_user_popup = RemoveOrgUserPopup(page)
        self.remove_proj_member_popup = RemoveProjMemberPopup(page)
        self.edit_proj_member_popup = EditProjMemberPopup(page)
        self.files_page = FilesPage(page)
        self.create_org_popup = CreateOrganizationPopup(page)
        self.new_folder_popup = NewFolderPopup(page)
        self.rename_file_popup = RenameFilePopup(page)
        self.delete_file_popup = DeleteFilePopup(page)
        self.buy_credits_popup = BuyCreditsPopup(page)
        self.payment_page = PaymentPage(page)
        self.secrets_page = SecretsPage(page)
        self.create_secret_popup = CreateSecretPopup(page)
        self.delete_secret_popup = DeleteSecretPopup(page)
        self.disks_page = DisksPage(page)
        self.create_disk_popup = CreateDiskPopup(page)
        self.delete_disk_popup = DeleteDiskPopup(page)
        self.resource_preset_popup = ResourcePresetPopup(page)
        self.choose_secret_popup = ChooseSecretPopup(page)
        self.shell_install_page = ShellInstallPage(page)
        self.shell_details_page = ShellDetailsPage(page)
        self.shell_app_page = ShellAppPage(page)
        self.deep_seek_install_page = DeepSeekInstallPage(page)
        self.deep_seek_details_page = DeepSeekDetailsPage(page)
