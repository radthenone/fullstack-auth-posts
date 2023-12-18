import json
from config.env import BASE_DIR

SCHEMAS_DIR = BASE_DIR / "schemas"


def get_schema(file_name: str) -> dict:
    schema_json = open(f"{SCHEMAS_DIR}/{file_name}.json")
    schema = json.loads(schema_json.read())
    return schema
