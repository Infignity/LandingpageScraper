""" Define all configurations """

import os
from typing import Literal
from pydantic import ConfigDict
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

BASE_DIR = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[:-1])

config = Config(os.path.join(BASE_DIR, ".env"))

def create_path(path_str: str, allow_absolute=False) -> str:
    """Creates a directory in the specified path, if path does not exist, they'll be created"""
    if not allow_absolute:
        full_path = os.path.join(BASE_DIR, path_str)
    else:
        full_path = path_str

    if not os.path.exists(full_path):
        os.makedirs(full_path, exist_ok=True)
    return full_path

ENVIRONMENT: Literal["development", "production", "staging"] = config("ENVIRONMENT")
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_NAME = config("DB_NAME")

def to_camel_case(snake_str: str):
    """
    Converts a string in snake case to camel case
    :param snake_str: A string in snake case
    :return: A string in camel case
    """

    components = snake_str.split("_")
    components = [components[0]] + [x.capitalize() for x in components[1:]]
    camel_case_str = "".join(components)
    return camel_case_str

simple_pydantic_model_config = ConfigDict(
    str_strip_whitespace=True,
    use_enum_values=True,
    alias_generator=to_camel_case,
    populate_by_name=True
)