import pytest
from django.test import override_settings


@pytest.fixture(autouse=True)
def force_test_settings():
    with override_settings(DJANGO_SETTINGS_MODULE="tests.django.settings"):
        yield
