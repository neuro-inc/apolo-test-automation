import random
import string
from typing import Optional


class JobData:
    def __init__(
        self,
        gherkin_name: str,
        job_name: Optional[str] = None,
        image_name: str = "ubuntu",
        command: str = "",
    ) -> None:
        self.__gherkin_name: str = gherkin_name
        self.__job_name: str = job_name or self.generate_random_name()
        self.__image_name: str = image_name
        self.__command: str = command
        self.__job_id: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"JobData(gherkin_name={self.__gherkin_name}, "
            f"job_name={self.__job_name}, "
            f"job_id={self.__job_id}, "
            f"image_name={self.__image_name}, "
            f"command={self.__command})"
        )

    @staticmethod
    def generate_random_name(prefix: str = "regression-job-", length: int = 10) -> str:
        characters = string.ascii_lowercase + string.digits
        return f"{prefix}{''.join(random.choices(characters, k=length))}"

    @property
    def job_name(self) -> str:
        return self.__job_name

    @property
    def gherkin_name(self) -> str:
        return self.__gherkin_name

    @property
    def image_name(self) -> str:
        return self.__image_name

    @property
    def command(self) -> str:
        return self.__command

    @property
    def job_id(self) -> Optional[str]:
        return self.__job_id

    @job_id.setter
    def job_id(self, value: Optional[str]) -> None:
        if not isinstance(value, str) and value is not None:
            raise ValueError("job_id must be a string or None.")
        self.__job_id = value
