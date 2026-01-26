import pytest
from mpt_extension_sdk.mpt_http.base import MPTClient


@pytest.fixture(autouse=True)
def settings_configuration(settings):
    settings.INSTALLED_APPS = settings.INSTALLED_APPS + ["swo_playground.apps.ExtensionConfig"]  # noqa: PLR6104, RUF005


@pytest.fixture
def mock_mpt_client(mocker):
    return mocker.Mock(spec=MPTClient)
