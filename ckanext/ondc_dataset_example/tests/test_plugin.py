import pytest

import ckan.plugins as p


@pytest.mark.ckan_config("ckan.plugins", "ondc_dataset_example")
@pytest.mark.usefixtures("with_plugins")
def test_plugin():
    assert p.plugin_loaded("ondc_dataset_example")
