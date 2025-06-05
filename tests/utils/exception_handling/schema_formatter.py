import re

from jsonschema.exceptions import SchemaError

from .base_formatter import ExceptionFormatter


class JsonSchemaFormatter(ExceptionFormatter):
    VALID_TYPES = ["string", "number", "integer", "boolean", "object", "array", "null"]

    def can_handle(self, exception: Exception) -> bool:
        return isinstance(exception, SchemaError)

    def format(self, exception: Exception, context: str, **kwargs) -> str:
        message = f"[SchemaError] during step: {context}\nMessage: {str(exception)}"
        message += "\nNote: JSON Schema is invalid."

        if "'type'" in str(
            exception
        ) and "not valid under any of the given schemas" in str(exception):
            message += (
                "\n→ The 'type' field likely contains an invalid value. "
                "Valid types are: 'string', 'number', 'integer', 'boolean', 'object', 'array', or 'null'."
            )
            match = re.search(r"On schema\['type'\]:\s+'([^']+)'", str(exception))
            if match:
                message += f"\nInvalid 'type' value: `{match.group(1)}`"
        return message
