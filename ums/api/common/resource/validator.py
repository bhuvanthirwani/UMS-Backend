import logging
from flask import request
from marshmallow import Schema

LOGGER = logging.getLogger(__package__)


def parse_rbody(schema: Schema) -> tuple:
    """Validates request based on a given schema.

    Returns:
        tuple: data, error
    """
    try:
        return schema.load(data=request.get_json()), None
    except Exception as e:
        return None, e
