import logging

from tests.utils.cli.apolo_components.apolo_admin import ApoloAdmin
from tests.utils.cli.apolo_components.apolo_config import ApoloConfig
from tests.utils.cli.apolo_components.apolo_disk import ApoloDisk
from tests.utils.cli.apolo_components.apolo_job import ApoloJob
from tests.utils.cli.apolo_components.apolo_runner import ApoloRunner
from tests.utils.cli.apolo_components.apolo_storage import ApoloStorage

logger = logging.getLogger("[🖥apolo_CLI]")


class ApoloCLI:
    def __init__(self) -> None:
        self.runner = ApoloRunner()
        self.admin = ApoloAdmin(runner=self.runner)
        self.config = ApoloConfig(runner=self.runner)
        self.job = ApoloJob(runner=self.runner)
        self.disk = ApoloDisk(runner=self.runner)
        self.storage = ApoloStorage(runner=self.runner)

    @property
    def last_command_output(self) -> str:
        return self.runner.last_command_output

    @property
    def last_command_executed(self) -> str:
        return self.runner.last_command_executed
