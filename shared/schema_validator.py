import os
import json
import jsonschema
from jsonschema.exceptions import ValidationError as JSONSchemaValidationError

class ValidationError(Exception):
    pass

class SchemaValidator:
    def __init__(self, schemas_dir: str = "./schemas/"):
        self.schemas_dir = schemas_dir
        self.schemas = {}

    def _load_schema(self, schema_name: str) -> dict:
        if schema_name in self.schemas:
            return self.schemas[schema_name]
            
        path = os.path.join(self.schemas_dir, schema_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Schema file not found at {path}")
            
        with open(path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
            self.schemas[schema_name] = schema
            return schema

    def validate(self, data: dict, schema_filename: str) -> None:
        """
        Validate data dict against the specified schema JSON file.
        Raises ValidationError with field-level details if invalid.
        """
        schema = self._load_schema(schema_filename)
        
        try:
            jsonschema.validate(instance=data, schema=schema)
        except JSONSchemaValidationError as e:
            # e.path contains the path to the field that failed validation
            path = " -> ".join(str(p) for p in e.path) if e.path else "root"
            raise ValidationError(f"Validation failed at '{path}': {e.message}")
