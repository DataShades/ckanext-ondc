import pytest

import ckan.plugins.toolkit as tk


@pytest.mark.usefixtures("with_plugins")
class TestLengthValidator:
    @pytest.mark.parametrize(
        "value",
        [
            "",
            "x",
            "x" * 9,
            "x" * 10,
        ],
    )
    def test_valid_length(self, value):
        validator = tk.get_validator("ondc_length_validator")(10)
        data, error = tk.navl_validate(
            {"value": value},
            {"value": [validator]},
        )
        assert not error
        assert data == {"value": value}

    @pytest.mark.parametrize(
        "value",
        ["x" * 11],
    )
    def test_invalid_length(self, value):
        validator = tk.get_validator("ondc_length_validator")(10)
        data, error = tk.navl_validate(
            {"value": value},
            {"value": [validator]},
        )
        assert error


@pytest.mark.usefixtures("with_plugins")
class TestUrlEmailValidator:
    @pytest.mark.parametrize(
        "value",
        [
            "",
            "http://example.com",
            "t@t.loc",
        ],
    )
    def test_valid_url_email(self, value):
        validator = tk.get_validator("ondc_url_or_email_validator")
        data, error = tk.navl_validate(
            {"value": value},
            {"value": [validator]},
        )
        assert not error
        assert data == {"value": value}

    @pytest.mark.parametrize(
        "value",
        [
            "xxx",
        ],
    )
    def test_invalid_url_email(self, value):
        validator = tk.get_validator("ondc_url_or_email_validator")
        data, error = tk.navl_validate(
            {"value": value},
            {"value": [validator]},
        )
        assert error


@pytest.mark.usefixtures("with_plugins")
class TestCopyToValidator:
    def test_copy_to(self):
        field_from = "xxx"
        field_to = "yyy"
        value = "123"

        validator = tk.get_validator("ondc_copy_to")(field_to)
        data, error = tk.navl_validate(
            {field_from: value},
            {field_from: [validator]},
        )

        assert not error
        assert data == {field_from: value, field_to: value}


@pytest.mark.usefixtures("with_plugins")
class TestDateParser:
    @pytest.mark.parametrize(
        "value, result",
        [
            ("2023-09", "2023-09-01 00:00:00"),
            ("2023-09-17", "2023-09-17 00:00:00"),
            ("2023-09-17T23:20:30", "2023-09-17 23:20:30"),
            ("2023-09-17T23:20:30+04:00", "2023-09-17 23:20:30+04:00"),
        ],
    )
    def test_valid_values(self, value, result):
        assert str(tk.get_validator("ondc_date_parser")(value, {})) == result

    @pytest.mark.parametrize(
        "value",
        [
            "20-02-2024",
        ],
    )
    def test_invalid_values(self, value):
        with pytest.raises(tk.Invalid):
            tk.get_validator("ondc_date_parser")(value, {})


@pytest.mark.usefixtures("with_plugins")
class TestChoicesValidator:
    @pytest.mark.parametrize(
        "field, value",
        [
            ("access_rights", "Open"),
            ("security_classification", "UNOFFICIAL"),
            ("resource_type", "collection"),
            ("update_frequency", "Triennial"),
        ],
    )
    def test_valid_choices(self, field, value):
        validator = tk.get_validator("ondc_choices")
        data, error = tk.navl_validate(
            {field: value},
            {field: [validator]},
        )
        assert not error

    @pytest.mark.parametrize("field, value", [("access_rights", "xxx")])
    def test_invalid_choices(self, field, value):
        validator = tk.get_validator("ondc_choices")
        data, error = tk.navl_validate(
            {field: value},
            {field: [validator]},
        )
        assert error
