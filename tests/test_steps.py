import pytest
from mpt_extension_sdk.flows.context import Context  # type: ignore[import-untyped]

from swo_playground.steps import NoopStep


@pytest.fixture
def client(mocker):
    return mocker.MagicMock()


@pytest.fixture
def next_step(mocker):
    return mocker.MagicMock()


@pytest.fixture
def context():
    return Context({})


def test_noops(mocker, client, context, next_step):
    step = NoopStep()

    step(client, context, next_step)

    next_step.assert_called()
