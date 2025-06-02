import random
import string
from tests.utils.test_data_management.project_data import ProjectData

class OrganizationData:
    def __init__(self, gherkin_name, org_name=None):
        self.__gherkin_name = gherkin_name
        self.__org_name = org_name or self.generate_random_name()
        self.__default_project = None
        self.__projects: dict[str, ProjectData] = {}

    def __repr__(self):
        return f"Organization(org_name={self.__org_name}, gherkin_name={self.__gherkin_name})"

    @staticmethod
    def generate_random_name(prefix="regression-org-", length=10):
        characters = string.ascii_lowercase + string.digits
        return f"{prefix}{''.join(random.choices(characters, k=length))}"

    @property
    def org_name(self):
        return self.__org_name

    @property
    def gherkin_name(self):
        return self.__gherkin_name

    @property
    def default_project(self):
        return self.__default_project

    def add_project(self, gherkin_name, project_name=None):
        if gherkin_name in [proj.gherkin_name for proj in self.__projects.values()]:
            raise ValueError(f"Project with gherkin_name '{gherkin_name}' already exists in organization '{self.__org_name}'")
        project = ProjectData(gherkin_name, project_name)
        self.__projects[project.project_name] = project
        if self.__default_project is None:
            self.__default_project = project
        return project

    def get_project(self, project_name):
        return self.__projects.get(project_name)

    def get_project_by_name(self, project_name):
        return next((proj for proj in self.__projects.values() if proj.project_name == project_name), None)

    def get_project_by_gherkin_name(self, gherkin_name):
        return next((proj for proj in self.__projects.values() if proj.gherkin_name == gherkin_name), None)

    def get_all_projects(self):
        return list(self.__projects.values())
