from tests.utils.test_data_management.job_data import JobData
from tests.utils.test_data_management.schema_data import SchemaData


class TestDataManager:
    """
    Container for test-related components managers for JSON schemas and Apolo jobs.
    """

    def __init__(self, schemas_path):
        """
        Initialize the TestDataManager with a schema handler.
        """
        self.schema_manager = SchemaData(schemas_path)


