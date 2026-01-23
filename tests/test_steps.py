import pytest
from mpt_extension_sdk.flows.context import Context  # type: ignore[import-untyped]

from swo_playground.steps import (
    CompleteOrderStep,
    CreateSubscriptionStep,
    NoopStep,
)


@pytest.fixture
def client(mocker):
    return mocker.MagicMock()


@pytest.fixture
def next_step(mocker):
    return mocker.MagicMock()


@pytest.fixture
def context():
    return Context({
        "id": "ORD-123",
        "parameters": {},
        "lines": [],
    })


def test_noops(client, context, next_step):
    step = NoopStep()

    step(client, context, next_step)  # act

    next_step.assert_called()


def test_create_subscription_step(mocker, client, context, next_step):
    mock_create_subscription = mocker.patch("swo_playground.steps.create_subscription")
    step = CreateSubscriptionStep()

    step(client, context, next_step)  # act

    expected_subscription = {
        "name": "Dummy subscription",
        "autoRenew": True,
        "lines": [],
    }
    mock_create_subscription.assert_called_once_with(client, "ORD-123", expected_subscription)
    next_step.assert_called()


def test_complete_order_step(mocker, client, context, next_step):
    mock_complete_order = mocker.patch("swo_playground.steps.complete_order")
    step = CompleteOrderStep()

    step(client, context, next_step)  # act

    mock_complete_order.assert_called_once_with(client, "ORD-123", parameters={}, template=None)
    next_step.assert_called()
