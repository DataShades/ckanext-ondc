from __future__ import annotations

import ckan.plugins.toolkit as tk
import ckan.types as types


def ondc_package_show() -> types.Schema:
    not_missing: types.Validator | types.ValidatorFactory = tk.get_validator(
        "not_missing"
    )

    return {
        "identifier": [not_missing],
    }


def ondc_package_update() -> types.Schema:
    not_missing: types.Validator | types.ValidatorFactory = tk.get_validator(
        "not_missing"
    )

    return {
        "identifier": [not_missing],
    }


def ondc_package_patch() -> types.Schema:
    not_missing: types.Validator | types.ValidatorFactory = tk.get_validator(
        "not_missing"
    )

    return {
        "identifier": [not_missing],
    }
