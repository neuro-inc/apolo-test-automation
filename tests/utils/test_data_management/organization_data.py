from __future__ import annotations

import random
import string
from typing import Optional

from tests.utils.test_data_management.project_data import ProjectData


class OrganizationData:
    def __init__(self, gherkin_name: str, org_name: Optional[str] = None) -> None:
        self._gherkin_name: str = gherkin_name
        self._org_name: str = org_name or self.generate_random_name()
        self._default_project: Optional[ProjectData] = None
        self._projects: dict[str, ProjectData] = {}

    def __repr__(self) -> str:
        return f"Organization(org_name={self._org_name}, gherkin_name={self._gherkin_name})"

    @staticmethod
    def generate_random_name(prefix: str = "regression-org-", length: int = 10) -> str:
        characters = string.ascii_lowercase + string.digits
        return f"{prefix}{''.join(random.choices(characters, k=length))}"

    @property
    def org_name(self) -> str:
        return self._org_name

    @property
    def gherkin_name(self) -> str:
        return self._gherkin_name

    @property
    def default_project(self) -> ProjectData:
        if self._default_project:
            return self._default_project
        else:
            raise ValueError("Default project not set")

    def add_project(
        self, gherkin_name: str, project_name: Optional[str] = None
    ) -> ProjectData:
        if gherkin_name in [proj.gherkin_name for proj in self._projects.values()]:
            raise ValueError(
                f"Project with gherkin_name '{gherkin_name}' already exists in organization '{self._org_name}'"
            )
        project = ProjectData(gherkin_name, project_name)
        self._projects[project.project_name] = project
        if self._default_project is None:
            self._default_project = project
        return project

    def get_project(self, project_name: str) -> ProjectData:
        if project_name in self._projects:
            return self._projects[project_name]
        else:
            raise ValueError(f"Project with name '{project_name}' not found.")

    def get_project_by_gherkin_name(self, gherkin_name: str) -> ProjectData:
        project = next(
            (
                proj
                for proj in self._projects.values()
                if proj.gherkin_name == gherkin_name
            ),
            None,
        )
        if not project:
            raise ValueError(f"Project with gherkin_name '{gherkin_name}' not found.")
        return project

    def get_all_projects(self) -> list[ProjectData]:
        return list(self._projects.values())
