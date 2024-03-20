from __future__ import annotations

from typing import Any

import ckan.plugins.toolkit as tk
from ckan.logic import validate
from ckan.types import Context, DataDict
from ckan.types.logic import ActionResult

from ckanext.ondc.logic import schema


ONDC_FIELDS = [
    "identifier",
    "title",
    "description",
    "data_custodian",
    "point_of_contact",
    "access_rights",
    "security_classification",
    "keyword",
    "resource_type",
    "date_modified",
    "access_url",
    "temporal_coverage_from",
    "temporal_coverage_to",
    "update_frequency",
    "publish_date",
    "purpose",
    "location",
    "sensitive_data",
    "file_size",
    "format",
    "language",
    "legal_authority",
    "licence",
    "disposal",
    "data_status",
    "publisher",
]


@tk.side_effect_free
def ondc_package_show(
    context: Context, data_dict: DataDict
) -> ActionResult.PackageShow:
    """Show a package by its identifier. Show only the fields that are part of the
    ONDC"""
    tk.check_access("package_show", context, data_dict)
    pkg_id = data_dict["id"]
    pkg_dict: dict[str, Any] = tk.get_action("package_show")(context, {"id": pkg_id})
    _clean_ondc_schema(pkg_dict)
    return pkg_dict


@tk.side_effect_free
def ondc_package_search(
    context: Context, data_dict: DataDict
) -> ActionResult.PackageSearch:
    """Search for packages. Show only the fields that are part of the ONDC."""
    tk.check_access("package_search", context, data_dict)
    search_results = tk.get_action("package_search")(context, data_dict)
    for pkg_dict in search_results["results"]:
        _clean_ondc_schema(pkg_dict)
    return search_results


def _clean_ondc_schema(pkg_dict: DataDict) -> None:
    """Remove fields from the package dictionary that are not part of the ONDC
    schema."""
    if "scheming_datasets" in tk.g.plugins:
        dataset_fields: list[dict[str, Any]] = tk.h.scheming_dataset_schemas(
            pkg_dict["type"]
        )["dataset"]["dataset_fields"]
        dataset_fields_dict = {
            field["field_name"]: field
            for field in dataset_fields
            if field.get("ondc_field") is True
        }

        keys_to_delete = [
            field for field in list(pkg_dict.keys()) if field not in dataset_fields_dict
        ]
        for key in keys_to_delete:
            del pkg_dict[key]
    else:
        keys_to_delete = [field for field in list(pkg_dict.keys()) if field not in ONDC_FIELDS]
        for key in keys_to_delete:
            del pkg_dict[key]
