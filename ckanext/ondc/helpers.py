from __future__ import annotations

from typing import Any


def ondc_choices(field: dict[str, Any]) -> list[dict[str, str]]:
    if field["field_name"] == "access_rights":
        return [{"value": choice} for choice in ["Open", "Conditional", "Restricted"]]
    if field["field_name"] == "security_classification":
        return [
            {"value": choice}
            for choice in [
                "UNOFFICIAL",
                "OFFICIAL",
                "OFFICIAL: Sensitive",
                "PROTECTED",
                "SECRET",
                "TOP SECRET",
            ]
        ]

    if field["field_name"] == "resource_type":
        return [
            {"value": choice}
            for choice in [
                "collection",
                "dataset",
                "event",
                "image",
                "interactive resource",
                "model",
                "physical object",
                "party",
                "physical object",
                "place",
                "service",
                "software",
                "sound",
                "text",
            ]
        ]

    if field["field_name"] == "update_frequency":
        return [
            {"value": choice}
            for choice in [
                "Triennial",
                "Biennial",
                "Annual",
                "Semiannual",
                "Three times a year",
                "Quarterly",
                "Bimonthly",
                "Monthly",
                "Semimonthly",
                "Biweekly",
                "Three times a month",
                "Weekly",
                "Semiweekly",
                "Daily",
                "Continuous",
                "Irregular",
            ]
        ]

    if field["field_name"] == "location":
        return [
            {"value": choice}
            for choice in [
                "Australia",
                "New South Wales",
                "Victoria",
                "Queensland",
                "South Australia",
                "Western Australia",
                "Tasmania",
                "Northern Territory",
                "Australian Capital Territory",
                "Other Territories*",
                "International",
            ]
        ]

    if field["field_name"] == "sensitive_data":
        return [
            {"value": choice}
            for choice in [
                "N/A [e.g. open data]",
                "Legislative secrecy",
                "Personal privacy",
                "Legal privilege [including commercial-inconfidence]",
            ]
        ]

    if field["field_name"] == "data_status":
        return [{"value": choice} for choice in ["Under Development", "Completed"]]
