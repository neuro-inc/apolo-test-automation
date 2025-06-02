import string
import random

class JobData:

    def __init__(self, gherkin_name, job_name=None, image_name="ubuntu", command=""):
        self.__gherkin_name = gherkin_name
        self.__job_name = job_name or self.generate_random_name()
        self.__image_name = image_name
        self.__command = command
        self.__job_id = None  # Initialize as None

    def __repr__(self):
        return (f"JobData(gherkin_name={self.__gherkin_name}, "
                f"job_name={self.__job_name}, "
                f"job_id={self.__job_id}, "
                f"image_name={self.__image_name}, "
                f"command={self.__command})")

    @staticmethod
    def generate_random_name(prefix="regression-job-", length=10):
        characters = string.ascii_lowercase + string.digits
        return f"{prefix}{''.join(random.choices(characters, k=length))}"

    @property
    def job_name(self):
        return self.__job_name

    @property
    def gherkin_name(self):
        return self.__gherkin_name

    @property
    def image_name(self):
        return self.__image_name

    @property
    def command(self):
        return self.__command

    @property
    def job_id(self):
        return self.__job_id

    @job_id.setter
    def job_id(self, value):
        # Optional: Add validation
        if not isinstance(value, str) and value is not None:
            raise ValueError("job_id must be a string or None.")
        self.__job_id = value
