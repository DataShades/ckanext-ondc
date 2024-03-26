import pytest

import ckan.plugins.toolkit as tk

from ckanext.ondc.logic.action import ONDC_FIELDS


@pytest.mark.ckan_config("ckan.plugins", "ondc scheming_datasets")
@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("reset_db")
class TestSchemingOndcPackageShow:
    def test_ondc_package_show_include_only_ondc_fields(self, ondc_dataset_factory):
        pkg_id = ondc_dataset_factory()["id"]
        result = tk.get_action("ondc_package_show")(
            {"ignore_auth": True}, {"id": pkg_id}
        )
        assert all(field in ONDC_FIELDS for field in result)


@pytest.mark.ckan_config("ckan.plugins", "ondc ondc_dataset_example")
@pytest.mark.usefixtures("with_plugins")
@pytest.mark.usefixtures("reset_db")
class TestIDatasetFormOndcPackageShow:
    def test_ondc_package_show_include_only_ondc_fields(self, ondc_dataset_factory):
        pkg_id = ondc_dataset_factory()["id"]
        result = tk.get_action("ondc_package_show")(
            {"ignore_auth": True}, {"id": pkg_id}
        )
        assert all(field in ONDC_FIELDS for field in result)
