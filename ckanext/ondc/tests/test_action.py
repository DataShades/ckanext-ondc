import pytest

from ckan.tests.helpers import call_action

from ckanext.ondc.logic.action import ONDC_FIELDS


@pytest.mark.ckan_config("ckan.plugins", "ondc scheming_datasets")
@pytest.mark.usefixtures("with_plugins", "reset_db")
class TestSchemingOndcPackageShow:
    def test_ondc_package_show_include_only_ondc_fields(self, ondc_dataset_factory):
        pkg_id = ondc_dataset_factory()["id"]
        result = call_action("ondc_package_show", id=pkg_id)
        assert set(result).issubset(ONDC_FIELDS)


@pytest.mark.ckan_config("ckan.plugins", "ondc ondc_dataset_example")
@pytest.mark.usefixtures("with_plugins", "reset_db")
class TestIDatasetFormOndcPackageShow:
    def test_ondc_package_show_include_only_ondc_fields(self, ondc_dataset_factory):
        pkg_id = ondc_dataset_factory()["id"]
        result = call_action("ondc_package_show", id=pkg_id)
        assert set(result).issubset(ONDC_FIELDS)


@pytest.mark.ckan_config("ckan.plugins", "ondc scheming_datasets")
@pytest.mark.usefixtures("with_plugins", "reset_db", "clean_index")
class TestOndcPackageSearch:
    def test_ondc_package_search(self, ondc_dataset_factory):
        pkg_title = ondc_dataset_factory()["title"]
        result = call_action("ondc_package_search", fq=f"title:{pkg_title}")["results"][0]
        assert set(result).issubset(ONDC_FIELDS)
