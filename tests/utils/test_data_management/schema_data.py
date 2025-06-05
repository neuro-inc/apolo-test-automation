import json
from pathlib import Path

import aiofiles
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate


class SchemaData:
    """
    Manages expected and actual schemas, performs comparison, and tracks errors.
    """

    def __init__(self, schemas_path):
        self._saved_schemas_path = schemas_path
        self._saved_schema = None
        self._live_schema = None
        self._error = False
        self._error_message = None

    @property
    def saved_schema(self):
        return self._saved_schema

    @property
    def live_schema(self):
        return self._live_schema

    @property
    def error(self):
        return self._error

    @property
    def error_message(self):
        return self._error_message

    async def load_saved_schema(self, app_name):
        """
        Asynchronously loads a saved JSON schema for a given app name from disk.
        """
        schema_path = Path(f"{self._saved_schemas_path}/{app_name}.json")

        if not schema_path.exists():
            raise ValueError(f"Schema file not found: {schema_path}")

        async with aiofiles.open(schema_path) as f:
            content = await f.read()
            self._saved_schema = json.loads(content)

    def parse_live_schema(self, full_schema, app_name: str):
        if not isinstance(full_schema, list) or not all(
            isinstance(item, dict) for item in full_schema
        ):
            raise ValueError("Invalid schema format: expected a list of dictionaries")

        match = next(
            (item for item in full_schema if item.get("name") == app_name), None
        )

        if not match:
            raise ValueError(f"App with name '{app_name}' not found in response")

        self._live_schema = match

    def validate(self):
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
