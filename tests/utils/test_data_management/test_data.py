import logging
from typing import Optional

from tests.utils.test_data_management.organization_data import OrganizationData
from tests.utils.test_data_management.job_data import JobData

logger = logging.getLogger("[🔧DATA MANAGER]")


class DataManager:
    def __init__(self) -> None:
        self._organizations: dict[str, OrganizationData] = {}
        self._default_organization: Optional[OrganizationData] = None

    def __repr__(self) -> str:
        return f"DataManager(organizations={list(self._organizations.keys())})"

    @property
    def default_organization(self) -> OrganizationData:
        if self._default_organization:
            return self._default_organization
        else:
            raise ValueError("Default organization not set")

    def add_organization(
        self, gherkin_name: str, org_name: Optional[str] = None
    ) -> OrganizationData:
        if gherkin_name in [org.gherkin_name for org in self._organizations.values()]:
            raise ValueError(
                f"Organization with gherkin_name '{gherkin_name}' already exists."
            )
        org = OrganizationData(gherkin_name, org_name)
        self._organizations[org.org_name] = org
        logger.info(
            f"Added organization: org_name={org.org_name}, gherkin_name={gherkin_name}"
        )
        if self._default_organization is None:
            self._default_organization = org
        return org

    def get_organization(self, org_name: str) -> Optional[OrganizationData]:
        return self._organizations.get(org_name)

    def get_organization_by_name(self, org_name: str) -> Optional[OrganizationData]:
        return next(
            (org for org in self._organizations.values() if org.org_name == org_name),
            None,
        )

    def get_organization_by_gherkin_name(self, gherkin_name: str) -> OrganizationData:
        org = next(
            (
                org
                for org in self._organizations.values()
                if org.gherkin_name == gherkin_name
            ),
            None,
        )
        if org is None:
            raise ValueError(
                f"No organization found with gherkin_name '{gherkin_name}'"
            )
        return org

    def get_all_organizations(self) -> list[OrganizationData]:
        return list(self._organizations.values())

    def remove_organization(self, org_name: str) -> None:
        if org_name in self._organizations:
            del self._organizations[org_name]

    def get_job_from_default_project(self, gherkin_name: str) -> JobData:
        return self.default_organization.default_project.get_job_by_gherkin_name(
            gherkin_name
        )
