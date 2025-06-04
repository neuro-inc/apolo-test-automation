from tests.components.ui.pages.base_element import BaseElement
from tests.components.ui.pages.base_page import BasePage

class JobsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.__create_new_job_button = BaseElement(self.page, 'a:has-text("Create new job")')
        self.__show_all_jobs_button = BaseElement(self.page, 'button:has-text("Show all jobs")')

    async def is_loaded(self):
        """
        Returns True if the page is considered loaded (key elements are visible).
        """
        self.log("Check if page is loaded")
        return await self.__create_new_job_button.expect_to_be_loaded()

    async def click_show_all_jobs_button(self):
        self.log("Click show all jobs button")
        await self.__show_all_jobs_button.click()
        await self.page.wait_for_timeout(2000)

    def _get_job_button(self, job_name):
        return BaseElement(self.page, f'a:has-text("{job_name}")')

    async def is_jobs_button_displayed(self, job_name):
        self.log("Check if jobs button displayed")
        return await self._get_job_button(job_name).is_visible()

    async def click_jobs_button(self, job_name):
        self.log("Click jobs button")
        await self._get_job_button(job_name).click()

    async def is_job_status_successfull(self, job_name):
        self.log("Check if job status successfull")
        row_locator = BaseElement(self.page, f'tr:has(a:has-text("{job_name}"))')
        status_locator = row_locator.locator.locator('div[slot="trigger"] p.capitalize')
        status = await status_locator.inner_text()
        if status.lower() == "succeeded":
            return True
        elif status.lower() == "failed":
            return False
