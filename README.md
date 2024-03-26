[![Tests](https://github.com/DataShades/ckanext-ondc/workflows/Tests/badge.svg)](https://github.com/DataShades/ckanext-ondc/actions/workflows/test.yml)

# ckanext-ondc

CKAN extension designed to standardize and facilitate the integration of ONDC metadata
attributes across various CKAN portals. It enables seamless import/export of datasets, ensuring uniformity
and compatibility of metadata fields according to the ONDC guidelines.

## What is ONDC metadata?

The Australian Governement's Office of the National Data Commissioner (ONDC) has developed a set of 26 metadata attributes as a baseline standard for discoverability and reusability of data assets across the Australian Government.

These 26 metadata attributes can be further grouped into:

- 10 core attributes that are critical for data management and discovery, and
- 16 additional attributes that further support discovery and reuse of data assets.

All agencies are advised to include all 26 metadata attributes as best practice to describe their data assets. The 10 core attributes are mandatory for the Australian Government Data Catalogue.

Further information can be found [here](https://www.datacommissioner.gov.au/sites/default/files/2023-12/ONDC-Guide-on-Metadata-Attributes-November-23.pdf) and [here](https://www.datacommissioner.gov.au/sites/default/files/2023-04/ONDC%20Metadata%20Attributes%202023_0.pdf).

## Content

- [ckanext-ondc](#ckanext-ondc)
    - [Content](#content)
    - [ONDC presets](#ondc-presets)
        - [Using ONDC presets with ckanext-scheming](#using-ondc-presets-with-ckanext-scheming)
        - [Customizing Presets](#customizing-presets)
        - [Defining Custom Fields Without Using Scheming](#defining-custom-fields-without-using-scheming)
    - [Examples of import/export the ONDC attributes](#examples-of-importexport-the-ondc-attributes)
        - [Exporting ONDC Attributes of a Dataset](#exporting-ondc-attributes-of-a-dataset)
        - [Searching for Datasets by ONDC Attributes](#searching-for-datasets-by-ondc-attributes)
        - [Creating, Updating, and Patching Datasets with ONDC Attributes](#creating-updating-and-patching-datasets-with-ondc-attributes)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Developer installation](#developer-installation)
    - [Tests](#tests)
    - [License](#license)

## ONDC presets

ckanext-ondc provides
a [set of ONDC presets](https://github.com/DataShades/ckanext-ondc/blob/master/ckanext/ondc/presets.yaml) that can be
used to standardize the metadata fields of a CKAN portal.
Below is a list of ONDC metadata attributes and their corresponding ONDC presets and CKAN machine names:

| ONDC metadata attribute | Preset name                  | CKAN machine name       |
|-------------------------|------------------------------|-------------------------|
| Identifier              | ondc_identifier              | identifier              |
| Title                   | ondc_title                   | title                   |
| Description             | ondc_description             | description             |
| Data Custodian          | ondc_data_custodian          | data_custodian          |
| Point of Contact        | ondc_point_of_contact        | point_of_contact        |
| Access Rights           | ondc_access_rights           | access_rights           |
| Security Classification | ondc_security_classification | security_classification |
| Keyword                 | ondc_keyword                 | keyword                 |
| Resource Type           | ondc_resource_type           | resource_type           |
| Date Modified           | ondc_date_modified           | date_modified           |
| Access URL              | ondc_access_url              | access_url              |
| Temporal coverage from  | ondc_temporal_coverage_from  | temporal_coverage_from  |
| Temporal coverage to    | ondc_temporal_coverage_to    | temporal_coverage_to    |
| Update Frequency        | ondc_update_frequency        | update_frequency        |
| Publish Date            | ondc_publish_date            | publish_date            |
| Purpose                 | ondc_purpose                 | purpose                 |
| Location                | ondc_location                | location                |
| Sensitive Data          | ondc_sensitive_data          | sensitive_data          |
| File size               | ondc_file_size               | file_size               |
| Format                  | ondc_format                  | format                  |
| Language                | ondc_language                | language                |
| Legal Authority         | ondc_legal_authority         | legal_authority         |
| Licence                 | ondc_licence                 | licence                 |
| Disposal                | ondc_disposal                | disposal                |
| Data Status             | ondc_data_status             | data_status             |
| Publisher               | ondc_publisher               | publisher               |

Preset names are used to define the schema for datasets, while CKAN machine names are used to store the metadata in the
database.

Ensure the `ckanext-ondc` extension is installed. Then, integrate ONDC presets into your CKAN portal by adding the
following line to your CKAN configuration file (`ckan.ini` or `production.ini`):

```ini
ckan.plugins = ondc
```

### Using ONDC presets with ckanext-scheming

Using the ONDC presets with ckanext-scheming
requires [installation](https://github.com/ckan/ckanext-scheming?tab=readme-ov-file#installation)
and [configuration](https://github.com/ckan/ckanext-scheming?tab=readme-ov-file#configuration) of the ckanext-scheming
extension. After that add ONDC presets to the CKAN configuration file:

```ini
scheming.presets = ckanext.ondc:presets.yaml
```

Use the ONDC presets to create a new dataset schema:

```yaml
scheming_version: 1
dataset_type: your_dataset_type
about: Description of your dataset
about_url: Your URL here

dataset_fields:
  - preset: ondc_identifier

  - preset: ondc_title

  # Include additional fields as needed, following the same structure.
```

This YAML snippet outlines how to define a schema for your datasets using the ckanext-ondc presets. Replace
`# Include additional fields as needed, following the same structure.` with additional fields as required by
your schema, referencing the provided presets.

[Example of a dataset schema with ONDC presets](https://github.com/DataShades/ckanext-ondc/blob/master/ckanext/ondc/dataset.yaml).

Add your datasets schema to the CKAN configuration file:

```ini
scheming.dataset_schemas = path_to_your_extension:dataset.yaml
```

### Customizing Presets

To tailor presets to your needs, you can override preset values in your schema file. For instance, to use a custom
form snippet for the ondc_title preset:

```yaml
scheming_version: 1
dataset_type: your_dataset_type
about: Description of your dataset
about_url: Your URL here

dataset_fields:
  - preset: ondc_identifier

  - preset: ondc_title
    form_snippet: custom_title.html

  # Include additional fields as needed, following the same structure.
```

Then, create the `templates/scheming/form_snippets/custom_title.html` file incorporating your custom form snippet.

### Defining Custom Fields Without Using Scheming

Even if you're not utilizing ckanext-scheming, the ONDC presets can still be applied to define custom fields in your
CKAN configuration file. This approach involves customizing the dataset schema through the `IDatasetForm` plugin
interface. Within the plugin, you can specify the schema for creating, updating, and displaying datasets. The schema
is represented as a dictionary, where each key is a field name and its value is a list of validators and converters.
For instance, to add a custom text field to the schema:

```python
import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
from ckan.types import Schema


class OndcDatasetsExamplePlugin(plugins.SingletonPlugin, tk.DefaultDatasetForm):
    plugins.implements(plugins.IDatasetForm, inherit=True)

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
                    tk.get_validator("unicode_safe"),
                    tk.get_validator("ondc_length_validator")(200),
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
            }
        )
        return schema

    def is_fallback(self):
        return True
```

The validators used in the `IDatasetForm` plugin's schema are aligned with those specified in the corresponding ONDC
preset. For functions that create (create_package_schema) and update (update_package_schema) package schemas, we
incorporate the convert_to_extras validator. This validator ensures that the field is stored within the dataset's
extras. Conversely, within the show_package_schema function, we utilize the convert_from_extras validator to fetch the
field from the dataset's extras for display.

Following the schema adjustments, it's necessary to adapt the templates to properly render these custom fields. To
achieve this, the plugin must also implement the IConfigurer interface, which facilitates the incorporation of custom
templates and other configuration change

```python
class OndcDatasetsExamplePlugin(plugins.SingletonPlugin, tk.DefaultDatasetForm):
    plugins.implements(plugins.IDatasetForm, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=True)

    # IDatasetForm

    # ...

    # IConfigurer

    def update_config(self, config):
        tk.add_template_directory(config, "templates")
```

To ensure that ONDC fields are properly displayed, you will need to customize some of the templates used by CKAN. A
direct approach involves replacing the `basic_fields` block in the `templates/package/snippets/package_form.html` template with a block dedicated to
rendering custom fields. You can achieve this by creating a new template file within the templates directory of your
extension. The file should be named package/snippets/package_form.html. Inside this file, you will define the structure
and presentation of your custom fields as follows:

```html
{% ckan_extends %}

{% block basic_fields %}
{% snippet "scheming/form_snippets/ondc_identifier.html", data=data, errors=errors %}
{% snippet "scheming/form_snippets/ondc_title.html", data=data, errors=errors %}
{% endblock %}
```

In the provided code example, form snippets correspond to the form_snippet key values defined in the related presets.

To display ONDC fields on the dataset detail page, you will need to override the default rendering of extras. This can
be achieved by creating a new template file in your extension's templates directory. Name this file
`templates/package/snippets/additional_info.html`. This template will specifically handle the presentation of ONDC fields
within the "Additional Information" section of the dataset page. Here's an example of how this could be structured:

```html
{% ckan_extends %}

{% block package_additional_info %}
{% if pkg_dict.identifier %}
<tr>
    <th scope="row" class="dataset-label">{{ _("Identifier") }}</th>
    <td class="dataset-details">{% snippet "scheming/display_snippets/ondc_text.html", field={"field_name":
        "identifier"}, data=pkg_dict %}
    </td>
</tr>
{% endif %}
{% if pkg_dict.title %}
<tr>
    <th scope="row" class="dataset-label">{{ _("Title") }}</th>
    <td class="dataset-details">{% snippet "scheming/display_snippets/ondc_text.html", field={"field_name": "title"},
        data=pkg_dict %}
    </td>
</tr>
{% endif %}
{% endblock %}
```

This extension includes a [practical example]((https://github.com/DataShades/ckanext-ondc/blob/master/ckanext/ondc_dataset_example)), showcasing how to construct a schema for your ONDC fields without relying
on ckanext-scheming. The example is implemented through the ondc_dataset_example plugin.
To activate this plugin, simply append the following line to your CKAN configuration file:

```ini
ckan.plugins = ondc ondc_dataset_example
```

## Examples of import/export the ONDC attributes

The extension introduces specific actions to facilitate working with ONDC attributes within datasets. Here's an overview
of these actions and examples of how to use them through the command-line interface (CLI) via `ckanapi`:

### Exporting ONDC Attributes of a Dataset

- **Action Name:** `ondc_package_show`
- **Purpose:** Returns a dictionary containing only the ONDC attributes of a specified dataset.
- **Required Parameter:** `id` (the ID or name of the dataset)
- **Example Command:**

```bash
ckanapi action ondc_package_show id=<your-dataset-id-or-name>
```

### Searching for Datasets by ONDC Attributes

- **Action Name:** `ondc_package_search`
- **Purpose:** Returns a list of dictionaries, each containing the ONDC attributes of datasets that match the search
  criteria.
- **Required Parameter:** `q` (your search query)
- **Example Command:**

```bash
ckanapi action ondc_package_search q=<your-search-query>
```

### Creating, Updating, and Patching Datasets with ONDC Attributes

For creating, updating, and patching datasets to include ONDC attributes, you can use the standard CKAN actions with
added ONDC fields.

- **Create a Dataset:**

```bash
ckanapi action package_create name=<your-dataset-name> identifier=<your-identifier> title=<your-title>
```

- **Update a Dataset:**

```bash
ckanapi action package_update id=<your-dataset-id-or-name> identifier=<new-identifier> title=<your-title>
```

- **Patch a Dataset:**

```bash
ckanapi action package_patch id=<your-dataset-id-or-name> identifier=<new-identifier>
```

## Requirements

Compatibility with core CKAN versions:

| CKAN version | Compatible? |
|--------------|-------------|
| 2.9          | not tested  |
| 2.10         | yes         |

## Installation

To install ckanext-ondc:

1. Activate your CKAN virtual environment, for example:

   . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

   git clone https://github.com/Data/datashades/ckanext-ondc.git
   cd ckanext-ondc
   pip install -e .
   pip install -r requirements.txt

3. Add `ondc` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

   sudo service apache2 reload

## Config settings

None at present

## Developer installation

To install ckanext-ondc for development, activate your CKAN virtualenv and
do:

    git clone https://github.com//ckanext-ondc.git
    cd ckanext-ondc
    python setup.py develop
    pip install -r dev-requirements.txt

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)