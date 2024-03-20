import ckan.plugins as plugins
import ckan.plugins.toolkit as tk


@tk.blanket.actions
@tk.blanket.validators
@tk.blanket.helpers
class OndcPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
