from playwright.async_api import Page

from tests.components.ui.pages.auth_page import AuthPage
from tests.components.ui.pages.jobs_page import JobsPage
from tests.components.ui.pages.login_page import LoginPage
from tests.components.ui.pages.main_page import MainPage
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
from tests.components.ui.pages.signup_page import SignupPage
from tests.components.ui.pages.signup_username_page import SignupUsernamePage


class PageManager:
    def __init__(self, page: Page):
        self.page = page

        self.auth_page = AuthPage(page)
        self.login_page = LoginPage(page)
        self.signup_page = SignupPage(page)
        self.signup_username_page = SignupUsernamePage(page)
        self.main_page = MainPage(page)
        self.jobs_page = JobsPage(page)
        self.welcome_new_user_page = WelcomeNewUserPage(page)
        self.join_organization_page = JoinOrganizationPage(page)
        self.name_your_organization_page = NameNewOrganizationPage(page)
        self.thats_it_page = ThatsItPage(page)
