from __future__ import annotations

from datetime import datetime
from typing import Any

import ckan.plugins.toolkit as tk
from ckan.types import Context, FlattenDataDict, FlattenErrorDict, FlattenKey, Validator


def ondc_length_validator(max_length: str) -> Validator:
    """Validates if the length of a value exceeds a specified maximum length."""
    try:
        max_length = int(max_length)
    except ValueError:
        max_length = float("inf")

    def validator(value: str, context: Context):
        if value is None or value == "" or value is tk.missing:
            return value
        if len(value) > max_length:
            raise tk.Invalid(f"The value length is too long. Max length: {max_length}")
        return value

    return validator


def ondc_url_or_email_validator(
    key: FlattenKey, data: FlattenDataDict, errors: FlattenErrorDict, context: Context
) -> Any:
    """Validate if the input is a valid email address or URL, returning the input if
    valid."""
    try:
        tk.get_validator("email_validator")(data[key], context)
        return
    except tk.Invalid:
        errors_ = {key: []}
        tk.get_validator("url_validator")(key, data, errors_, context)
        if not errors_[key]:
            return

    errors[key].append("The value should be an email address or a URL")


def ondc_copy_to(field_name: str) -> Validator:
    """Copy value of field to another field."""

    def validator(
        key: FlattenKey,
        data: FlattenDataDict,
        errors: FlattenErrorDict,
        context: Context,
    ):
        data[(field_name,)] = data.get(key)

    return validator


def ondc_date_parser(value: str, context: Context) -> datetime:
    """Add parsing of timezone to the default isodate validator."""
    try:
        return tk.get_validator("isodate")(value, context)
    except tk.Invalid:
        pass

    formats = ["%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%Y-%m"]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    raise tk.Invalid("Date format incorrect")


def ondc_choices(
    key: FlattenKey, data: FlattenDataDict, errors: FlattenErrorDict, context: Context
) -> Any:
    value = data[key]

    if value is tk.missing or not value:
        return value

    try:
        choices = tk.h.ondc_choices({"field_name": key[0]})
    except KeyError:
        raise tk.Invalid("No choices available for this field")

    for choice in choices:
        if value == choice["value"]:
            return value
    raise tk.Invalid(('Unexpected choice "%s"') % value)


def ondc_convert_to_json_if_datetime(date: str, context: Context) -> Any:
    if isinstance(date, datetime):
        return date.isoformat()

    return date
