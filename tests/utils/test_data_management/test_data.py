from tests.utils.test_data_management.organization_data import OrganizationData


class DataManager:
    def __init__(self):
        self.__organizations: dict[str, OrganizationData] = {}
        self.__default_organization = None

    def __repr__(self):
        return f"DataManager(organizations={list(self.__organizations.keys())})"

    @property
    def default_organization(self):
        return self.__default_organization

    def add_organization(self, gherkin_name, org_name=None):
        if gherkin_name in [org.gherkin_name for org in self.__organizations.values()]:
            raise ValueError(
                f"Organization with gherkin_name '{gherkin_name}' already exists."
            )
        org = OrganizationData(gherkin_name, org_name)
        self.__organizations[org.org_name] = org
        if self.__default_organization is None:
            self.__default_organization = org
        return org

    def get_organization(self, org_name):
        return self.__organizations.get(org_name)

    def get_organization_by_name(self, org_name):
        return next(
            (org for org in self.__organizations.values() if org.org_name == org_name),
            None,
        )

    def get_organization_by_gherkin_name(self, gherkin_name):
        return next(
            (
                org
                for org in self.__organizations.values()
                if org.gherkin_name == gherkin_name
            ),
            None,
        )

    def get_all_organizations(self):
        return list(self.__organizations.values())

    def remove_organization(self, org_name):
        if org_name in self.__organizations:
            del self.__organizations[org_name]

    def get_job_from_default_project(self, gherkin_name):
        if self.__default_organization is None:
            raise AssertionError("No default organization created!!!")
        elif self.__default_organization.default_project is None:
            raise AssertionError("No default project created!!!")
        else:
            return self.__default_organization.default_project.get_job_by_gherkin_name(
                gherkin_name
            )
