import json
from pathlib import Path

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate


class SchemaData:
    """
    Manages expected and actual schemas, performs comparison, and tracks errors.
    """

    def __init__(self, schemas_path):
        """
        Initialize SchemaData with empty schemas and no error state.
        """
        self._saved_schemas_path = schemas_path
        self._saved_schema = None
        self._live_schema = None
        self._error = False
        self._error_message = None

    @property
    def saved_schema(self):
        """
        Returns:
            dict or None: The expected schema loaded from file or definition.
        """
        return self._saved_schema

    @property
    def live_schema(self):
        """
        Returns:
            dict or None: The actual schema retrieved from the live API.
        """
        return self._live_schema

    @property
    def error(self):
        """
        Returns:
            bool: True if an error occurred during schema comparison.
        """
        return self._error

    @property
    def error_message(self):
        """
        Returns:
            str or None: Detailed message describing the schema mismatch or issue.
        """
        return self._error_message

    def load_saved_schema(self, app_name):
        """
        Loads a saved JSON schema for a given app name from disk.
        Args:
            app_name (str): The name of the app (used to locate the schema file).
        Raises:
            ValueError: If the expected schema file does not exist.
            json.JSONDecodeError: If the schema file is not valid JSON.
        """
        schema_path = Path(f"{self._saved_schemas_path}/{app_name}.json")

        if not schema_path.exists():
            raise ValueError(f"Schema file not found: {schema_path}")

        with open(schema_path, "r") as f:
            self._saved_schema = json.load(f)

    def parse_live_schema(self, full_schema, app_name: str):
        """
        Extracts the schema for a specific app from a full schema response and stores it.
        Args:
            full_schema (Iterable[dict]): The complete list of app schema definitions returned from the API.
            app_name (str): The name of the application to match.
        Raises:
            ValueError: If the full_schema is invalid or if no app with the given name is found.
        """
        if not isinstance(full_schema, list) or not all(isinstance(item, dict) for item in full_schema):
            raise ValueError("Invalid schema format: expected a list of dictionaries")

        match = next((item for item in full_schema if item.get("name") == app_name), None)

        if not match:
            raise ValueError(f"App with name '{app_name}' not found in response")

        self._live_schema = match

    def validate(self):
        """
        Validates the live components against the saved JSON Schema using jsonschema.
        Returns:
            bool: True if validation succeeds, False if an error is encountered.
        """
        if self._saved_schema is None:
            self._error = True
            self._error_message = "Saved schema is not set."
            return False

        if self._live_schema is None:
            self._error = True
            self._error_message = "Live components is not set."
            return False

        try:
            validate(instance=self._live_schema, schema=self._saved_schema)
            self._error = False
            self._error_message = None
            return True
        except ValidationError as ve:
            self._error = True
            self._error_message = f"Schema validation failed: {ve.message}"
            return False
