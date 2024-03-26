import random

import factory
from pytest_factoryboy import register

from ckan.plugins import toolkit as tk
from ckan.tests import factories


@register(_name="ondc_dataset")
class OndcDatasetFactory(factories.Dataset):
    identifier = factory.Faker("uuid4")
    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    data_custodian = factory.Faker("name")
    point_of_contact = factory.Faker("email")
    access_rights = factory.LazyFunction(
        lambda: random.choice(tk.h.ondc_choices(field={"field_name": "access_rights"}))[
            "value"
        ]
    )
    security_classification = factory.LazyFunction(
        lambda: random.choice(
            tk.h.ondc_choices(field={"field_name": "security_classification"})
        )["value"]
    )
    keyword = factory.Faker("word")
    resource_type = factory.LazyFunction(
        lambda: random.choice(tk.h.ondc_choices(field={"field_name": "resource_type"}))[
            "value"
        ]
    )
    date_modified = factory.Faker("date")
