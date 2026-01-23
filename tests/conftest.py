import pytest


@pytest.fixture(autouse=True)
def settings_configuration(settings):
    settings.INSTALLED_APPS += ["swo_playground.apps.ExtensionConfig"]
