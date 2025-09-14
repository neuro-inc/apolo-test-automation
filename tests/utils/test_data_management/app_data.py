from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Any

import aiofiles
from jsonschema import Draft7Validator, ValidationError


class AppData:
    def __init__(self, schemas_path: str) -> None:
        self._output_schemas_path: str = schemas_path
        self._saved_schema: Optional[dict[str, Any]] = None

    async def load_output_ui_schema(self, app_name: str) -> None:
        schema_path = Path(
            f"{self._output_schemas_path}/{app_name}_output_ui_schema.json"
        )

        if not schema_path.exists():
            raise ValueError(f"Schema file not found: {schema_path}")

        async with aiofiles.open(schema_path, mode="r") as f:
            content = await f.read()
            self._saved_schema = json.loads(content)

    async def load_output_api_schema(self, app_name: str) -> None:
        schema_path = Path(
            f"{self._output_schemas_path}/{app_name}_output_api_schema.json"
        )

        if not schema_path.exists():
            raise ValueError(f"Schema file not found: {schema_path}")

        async with aiofiles.open(schema_path, mode="r") as f:
            content = await f.read()
            self._saved_schema = json.loads(content)

    async def load_compl_schema(self, app_name: str) -> None:
        schema_path = Path(f"{self._output_schemas_path}/{app_name}_compl_schema.json")

        if not schema_path.exists():
            raise ValueError(f"Schema file not found: {schema_path}")

        async with aiofiles.open(schema_path, mode="r") as f:
            content = await f.read()
            self._saved_schema = json.loads(content)

    def validate_api_section_schema(
        self, outputs: list[dict[str, Any]]
    ) -> tuple[bool, str]:
        """
        Validate a list of output dicts against the loaded schema.
        Returns (True, "") if all are valid, else (False, summary of errors).
        """
        if not self._saved_schema:
            raise ValueError("No schema loaded. Call load_output_schema first.")

        validator = Draft7Validator(self._saved_schema)
        errors_summary: list[str] = []

        for idx, section in enumerate(outputs):
            if not isinstance(section, dict):
                errors_summary.append(
                    f"Item at index {idx} is not a dict but {type(section).__name__}: {section!r}"
                )
                continue

            try:
                validator.validate(section)
            except ValidationError as e:
                title = section.get("title", f"<unknown at {idx}>")
                errors_summary.append(f"{title} validation error: {e.message}")

        if errors_summary:
            return False, ";\n ".join(errors_summary)
        return True, ""
