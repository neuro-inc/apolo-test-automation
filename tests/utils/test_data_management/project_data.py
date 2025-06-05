import random
import string
from tests.utils.test_data_management.job_data import JobData


class ProjectData:
    def __init__(self, gherkin_name, project_name=None):
        self.__gherkin_name = gherkin_name
        self.__project_name = project_name or self.generate_random_name()
        self.__jobs: dict[str, JobData] = {}

    def __repr__(self):
        return f"Project(project_name={self.__project_name}, gherkin_name={self.__gherkin_name})"

    @staticmethod
    def generate_random_name(prefix="regression-proj-", length=10):
        characters = string.ascii_lowercase + string.digits
        return f"{prefix}{''.join(random.choices(characters, k=length))}"

    @property
    def project_name(self):
        return self.__project_name

    @property
    def gherkin_name(self):
        return self.__gherkin_name

    def add_job(self, gherkin_name, job_name=None, image_name="ubuntu", command=""):
        if gherkin_name in [job.gherkin_name for job in self.__jobs.values()]:
            raise ValueError(
                f"Job with gherkin_name '{gherkin_name}' already exists in project '{self.__project_name}'"
            )
        job = JobData(gherkin_name, job_name, image_name, command)
        self.__jobs[job.job_name] = job
        return job

    def get_job(self, job_name):
        return self.__jobs.get(job_name)

    def get_job_by_name(self, job_name):
        return next(
            (job for job in self.__jobs.values() if job.job_name == job_name), None
        )

    def get_job_by_gherkin_name(self, gherkin_name):
        return next(
            (job for job in self.__jobs.values() if job.gherkin_name == gherkin_name),
            None,
        )

    def get_all_jobs(self):
        return list(self.__jobs.values())
