from tests.components.ui.pages.auth_page import AuthPage
from tests.components.ui.pages.jobs_page import JobsPage
from tests.components.ui.pages.onboarding_pages.join_organization_page import (
    JoinOrganizationPage,
)
from tests.components.ui.pages.login_page import LoginPage
from tests.components.ui.pages.main_page import MainPage
from tests.components.ui.pages.onboarding_pages.name_new_organization_page import (
    NameNewOrganizationPage,
)
from tests.components.ui.pages.onboarding_pages.thats_it_page import ThatsItPage
from tests.components.ui.pages.onboarding_pages.welcome_new_user_page import (
    WelcomeNewUserPage,
)


class PageManager:
    def __init__(self, page, email, username):
        self.page = page

        self.auth_page = AuthPage(page)
        self.login_page = LoginPage(page)
        self.main_page = MainPage(page)
        self.jobs_page = JobsPage(page)
        self.welcome_new_user_page = WelcomeNewUserPage(page, email)
        self.join_organization_page = JoinOrganizationPage(page, username)
        self.name_your_organization_page = NameNewOrganizationPage(page)
        self.thats_it_page = ThatsItPage(page)
