import ckan.plugins as p
import pytest


@pytest.mark.ckan_config("ckan.plugins", "ondc")
@pytest.mark.usefixtures("with_plugins")
def test_plugin():
    assert p.plugin_loaded("ondc")
