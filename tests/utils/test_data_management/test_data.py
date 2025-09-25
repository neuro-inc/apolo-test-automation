import hashlib
import logging
import os
import random
import string
from typing import Optional

import lorem  # type: ignore

from tests.utils.test_data_management.app_data import AppData
from tests.utils.test_data_management.disk_data import DiskData
from tests.utils.test_data_management.organization_data import OrganizationData
from tests.utils.test_data_management.job_data import JobData

logger = logging.getLogger("[🔧DATA MANAGER]")


class DataManager:
    def __init__(
        self, gen_obj_path: str, download_path: str, output_schemas_path: str
    ) -> None:
        self._gen_obj_path = gen_obj_path
        self._download_path = download_path
        self._app_data = AppData(output_schemas_path)
        self._organizations: dict[str, OrganizationData] = {}
        self._disks: dict[str, DiskData] = {}
        self._default_organization: Optional[OrganizationData] = None

    def __repr__(self) -> str:
        return f"DataManager(organizations={list(self._organizations.keys())})"

    @property
    def default_organization(self) -> OrganizationData:
        if self._default_organization:
            return self._default_organization
        else:
            raise ValueError("Default organization not set")

    @property
    def app_data(self) -> AppData:
        return self._app_data

    @property
    def download_path(self) -> str:
        return self._download_path

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

    def generate_dummy_bin_file(self, size_mb: int = 1) -> tuple[str, str]:
        """Generate a dummy binary file with random content and random name.

        Args:
            size_mb (int): File size in megabytes (default is 1).

        Returns:
            str: Absolute path to the generated file.
        """
        size_bytes = size_mb * 1024 * 1024
        rand_part = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        filename = f"regression-bin-file-{rand_part}.bin"
        full_path = os.path.join(self._gen_obj_path, filename)
        with open(full_path, "wb") as f:
            f.write(os.urandom(size_bytes))
        logger.info(f"Generated dummy bin file: {full_path}")
        return full_path, filename

    def generate_dummy_txt_file(self, size_mb: int = 1) -> tuple[str, str]:
        """Generate a dummy text file with random lorem ipsum content and random name.

        Args:
            size_mb (int): File size in megabytes (default is 1).

        Returns:
            str: Absolute path to the generated file.
        """
        size_bytes = size_mb * 1024 * 1024
        rand_part = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        filename = f"regression-txt-file-{rand_part}.txt"
        full_path = os.path.join(self._gen_obj_path, filename)

        with open(full_path, "w", encoding="utf-8") as f:
            written = 0
            while written < size_bytes:
                paragraph = lorem.paragraph() + "\n"
                encoded = paragraph.encode("utf-8")
                to_write = min(len(encoded), size_bytes - written)
                f.write(paragraph[:to_write])
                written += to_write
        logger.info(f"Generated dummy text file: {full_path}")
        return full_path, filename

    def compare_files_md5(self, file_path_1: str, file_path_2: str) -> bool:
        def file_md5(path: str) -> str:
            hash_md5 = hashlib.md5()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()

        return file_md5(file_path_1) == file_md5(file_path_2)

    def add_disk(
        self,
        gherkin_name: str,
        org_name: str,
        owner: str,
        storage_amount: str,
        proj_name: str = "",
    ) -> DiskData:
        disk = DiskData(
            gherkin_name=gherkin_name,
            owner=owner,
            org_name=org_name,
            proj_name=proj_name,
            storage=storage_amount,
        )
        self._disks[gherkin_name] = disk
        return disk

    def generate_app_instance_name(self, app_name: str) -> str:
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{app_name}-regression-{suffix}"

    def generate_postgres_user_name(self) -> str:
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"psql-regression-user-{suffix}"

    def generate_postgres_user_db_name(self) -> str:
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"psql-db-regression-{suffix}"
