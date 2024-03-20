import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
from ckan.types import Schema


class OndcDatasetsExamplePlugin(plugins.SingletonPlugin, tk.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")

    # IDatasetForm

    def _modify_package_schema(self, schema: Schema) -> Schema:
        schema.update(
            {
                "identifier": [
                    tk.get_validator("not_empty"),
                    tk.get_validator("ondc_length_validator")(200),
                    tk.get_validator("convert_to_extras"),
                ],
                "title": [
                    tk.get_validator("if_empty_same_as")("name"),
                    tk.get_validator("not_empty"),
                    tk.get_validator("not_empty"),
                    tk.get_validator("ondc_length_validator")(200),
                    tk.get_validator("convert_to_extras"),
                ],
                "description": [
                    tk.get_validator("not_empty"),
                    tk.get_validator("ondc_length_validator")(500),
                    tk.get_validator("ondc_copy_to")("notes"),
                    tk.get_validator("convert_to_extras"),
                ],
                "data_custodian": [
                    tk.get_validator("not_empty"),
                    tk.get_validator("convert_to_extras"),
                ],
                "point_of_contact": [
                    tk.get_validator("not_empty"),
                    tk.get_validator("ondc_url_or_email_validator"),
                    tk.get_validator("convert_to_extras"),
                ],
                "access_rights": [
                    tk.get_validator("not_empty"),
                    tk.get_validator("ondc_choices"),
                    tk.get_validator("convert_to_extras"),
                ],
                "security_classification": [
                    tk.get_validator("not_empty"),
                    tk.get_validator("ondc_choices"),
                    tk.get_validator("convert_to_extras"),
                ],
                "keyword": [
                    tk.get_validator("not_empty"),
                    tk.get_validator("tag_string_convert"),
                    tk.get_validator("ondc_copy_to")("tag_string"),
                    tk.get_validator("convert_to_extras"),
                ],
                "resource_type": [
                    tk.get_validator("not_empty"),
                    tk.get_validator("ondc_choices"),
                    tk.get_validator("convert_to_extras"),
                ],
                "date_modified": [
                    tk.get_validator("not_empty"),
                    tk.get_validator("ondc_date_parser"),
                    tk.get_validator("ondc_convert_to_json_if_datetime"),
                    tk.get_validator("convert_to_extras"),
                ],
                "access_url": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("url_validator"),
                    tk.get_validator("convert_to_extras"),
                ],
                "temporal_coverage_from": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("ondc_date_parser"),
                    tk.get_validator("ondc_convert_to_json_if_datetime"),
                    tk.get_validator("convert_to_extras"),
                ],
                "temporal_coverage_to": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("ondc_date_parser"),
                    tk.get_validator("ondc_convert_to_json_if_datetime"),
                    tk.get_validator("convert_to_extras"),
                ],
                "update_frequency": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("ondc_choices"),
                    tk.get_validator("convert_to_extras"),
                ],
                "publish_date": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("ondc_date_parser"),
                    tk.get_validator("ondc_convert_to_json_if_datetime"),
                    tk.get_validator("convert_to_extras"),
                ],
                "purpose": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("ondc_length_validator")(500),
                    tk.get_validator("convert_to_extras"),
                ],
                "location": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("ondc_choices"),
                    tk.get_validator("convert_to_extras"),
                ],
                "sensitive_data": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("ondc_choices"),
                    tk.get_validator("convert_to_extras"),
                ],
                "file_size": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("convert_to_extras"),
                ],
                "format": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("convert_to_extras"),
                ],
                "language": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("convert_to_extras"),
                ],
                "legal_authority": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("ondc_length_validator")(200),
                    tk.get_validator("convert_to_extras"),
                ],
                "licence": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("ondc_copy_to")("license_id"),
                    tk.get_validator("convert_to_extras"),
                ],
                "disposal": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("convert_to_extras"),
                ],
                "data_status": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("ondc_choices"),
                    tk.get_validator("convert_to_extras"),
                ],
                "publisher": [
                    tk.get_validator("ignore_missing"),
                    tk.get_validator("convert_to_extras"),
                ],
            }
        )
        return schema

    def create_package_schema(self):
        schema = super(OndcDatasetsExamplePlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(OndcDatasetsExamplePlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(OndcDatasetsExamplePlugin, self).show_package_schema()
        schema.update(
            {
                "identifier": [
                    tk.get_validator("convert_from_extras"),
                ],
                "title": [
                    tk.get_validator("convert_from_extras"),
                ],
                "description": [
                    tk.get_validator("convert_from_extras"),
                ],
                "data_custodian": [
                    tk.get_validator("convert_from_extras"),
                ],
                "point_of_contact": [
                    tk.get_validator("convert_from_extras"),
                ],
                "access_rights": [
                    tk.get_validator("convert_from_extras"),
                ],
                "security_classification": [
                    tk.get_validator("convert_from_extras"),
                ],
                "keyword": [
                    tk.get_validator("convert_from_extras"),
                ],
                "resource_type": [
                    tk.get_validator("convert_from_extras"),
                ],
                "date_modified": [
                    tk.get_validator("convert_from_extras"),
                ],
                "access_url": [
                    tk.get_validator("convert_from_extras"),
                ],
                "temporal_coverage_from": [
                    tk.get_validator("convert_from_extras"),
                ],
                "temporal_coverage_to": [
                    tk.get_validator("convert_from_extras"),
                ],
                "update_frequency": [
                    tk.get_validator("convert_from_extras"),
                ],
                "publish_date": [
                    tk.get_validator("convert_from_extras"),
                ],
                "purpose": [
                    tk.get_validator("convert_from_extras"),
                ],
                "location": [
                    tk.get_validator("convert_from_extras"),
                ],
                "sensitive_data": [
                    tk.get_validator("convert_from_extras"),
                ],
                "file_size": [
                    tk.get_validator("convert_from_extras"),
                ],
                "format": [
                    tk.get_validator("convert_from_extras"),
                ],
                "language": [
                    tk.get_validator("convert_from_extras"),
                ],
                "legal_authority": [
                    tk.get_validator("convert_from_extras"),
                ],
                "licence": [
                    tk.get_validator("convert_from_extras"),
                ],
                "disposal": [
                    tk.get_validator("convert_from_extras"),
                ],
                "data_status": [
                    tk.get_validator("convert_from_extras"),
                ],
                "publisher": [
                    tk.get_validator("convert_from_extras"),
                ],
            }
        )
        return schema

    def is_fallback(self):
        return True
