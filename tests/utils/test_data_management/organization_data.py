from __future__ import annotations

import random
import string
from typing import Optional

from tests.utils.test_data_management.project_data import ProjectData


class OrganizationData:
    def __init__(self, gherkin_name: str, org_name: Optional[str] = None) -> None:
        self.__gherkin_name: str = gherkin_name
        self.__org_name: str = org_name or self.generate_random_name()
        self.__default_project: Optional[ProjectData] = None
        self.__projects: dict[str, ProjectData] = {}

    def __repr__(self) -> str:
        return f"Organization(org_name={self.__org_name}, gherkin_name={self.__gherkin_name})"

    @staticmethod
    def generate_random_name(prefix: str = "regression-org-", length: int = 10) -> str:
        characters = string.ascii_lowercase + string.digits
        return f"{prefix}{''.join(random.choices(characters, k=length))}"

    @property
    def org_name(self) -> str:
        return self.__org_name

    @property
    def gherkin_name(self) -> str:
        return self.__gherkin_name

    @property
    def default_project(self) -> ProjectData:
        if self.__default_project:
            return self.__default_project
        else:
            raise ValueError("Default project not set")

    def add_project(
        self, gherkin_name: str, project_name: Optional[str] = None
    ) -> ProjectData:
        if gherkin_name in [proj.gherkin_name for proj in self.__projects.values()]:
            raise ValueError(
                f"Project with gherkin_name '{gherkin_name}' already exists in organization '{self.__org_name}'"
            )
        project = ProjectData(gherkin_name, project_name)
        self.__projects[project.project_name] = project
        if self.__default_project is None:
            self.__default_project = project
        return project

    def get_project(self, project_name: str) -> ProjectData:
        if project_name in self.__projects:
            return self.__projects[project_name]
        else:
            raise ValueError(f"Project with name '{project_name}' not found.")

    def get_project_by_gherkin_name(self, gherkin_name: str) -> ProjectData:
        project = next(
            (
                proj
                for proj in self.__projects.values()
                if proj.gherkin_name == gherkin_name
            ),
            None,
        )
        if not project:
            raise ValueError(f"Project with gherkin_name '{gherkin_name}' not found.")
        return project

    def get_all_projects(self) -> list[ProjectData]:
        return list(self.__projects.values())
