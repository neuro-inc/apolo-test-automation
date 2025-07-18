from __future__ import annotations

import random
import string
from typing import Optional

from tests.utils.test_data_management.job_data import JobData


class ProjectData:
    def __init__(self, gherkin_name: str, project_name: Optional[str] = None) -> None:
        self._gherkin_name: str = gherkin_name
        self._project_name: str = project_name or self.generate_random_name()
        self._jobs: dict[str, JobData] = {}

    def __repr__(self) -> str:
        return f"Project(project_name={self._project_name}, gherkin_name={self._gherkin_name})"

    @staticmethod
    def generate_random_name(prefix: str = "regression-proj-", length: int = 10) -> str:
        characters = string.ascii_lowercase + string.digits
        return f"{prefix}{''.join(random.choices(characters, k=length))}"

    @property
    def project_name(self) -> str:
        return self._project_name

    @property
    def gherkin_name(self) -> str:
        return self._gherkin_name

    def add_job(
        self,
        gherkin_name: str,
        job_name: Optional[str] = None,
        image_name: str = "ubuntu",
        command: str = "",
    ) -> JobData:
        if gherkin_name in [job.gherkin_name for job in self._jobs.values()]:
            raise ValueError(
                f"Job with gherkin_name '{gherkin_name}' already exists in project '{self._project_name}'"
            )
        job = JobData(gherkin_name, job_name, image_name, command)
        self._jobs[gherkin_name] = job
        return job

    def get_job(self, job_name: str) -> JobData:
        for job in self._jobs.values():
            if job.job_name == job_name:
                return job
        raise ValueError(
            f"Job with name '{job_name}' not found in project '{self._project_name}'"
        )

    def get_job_by_gherkin_name(self, gherkin_name: str) -> JobData:
        if gherkin_name in self._jobs:
            return self._jobs[gherkin_name]
        raise ValueError(
            f"Job with gherkin name '{gherkin_name}' not found in project '{self._project_name}'"
        )

    def get_all_jobs(self) -> list[JobData]:
        return list(self._jobs.values())
