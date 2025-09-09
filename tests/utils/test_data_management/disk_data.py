import random
import string


class DiskData:
    def __init__(
        self,
        owner: str,
        org_name: str,
        storage: str,
        gherkin_name: str | None = None,
        proj_name: str = "",
    ):
        self.gherkin_name = gherkin_name
        self.name = f"regression-disk-{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"
        self.owner = owner
        self.proj_name = proj_name
        self.org_name = org_name
        self.storage = storage

        # Initialize other fields as empty
        self.id = ""
        self.uri = ""

    def __repr__(self) -> str:
        return (
            f"DiskInfo(gherkin_name='{self.gherkin_name}', owner='{self.owner}', "
            f"project_name='{self.proj_name}', org_name='{self.org_name}', id='{self.id}', "
            f"storage='{self.storage}', uri='{self.uri}', name='{self.name}'"
        )
