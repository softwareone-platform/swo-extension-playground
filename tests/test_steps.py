from collections.abc import Callable

import pytest
from mpt_extension_sdk.flows.context import Context  # type: ignore[import-untyped]

from swo_playground.steps import (
    CompleteOrderStep,
    CreateSubscriptionStep,
    NoopStep,
)


@pytest.fixture
def mock_next_step(mocker):
    return mocker.Mock(spec=Callable)


@pytest.fixture
def context():
    return Context(
        order={
            "id": "ORD-123",
            "parameters": {},
            "lines": [],
        }
    )


def test_noops(context, mock_mpt_client, mock_next_step):
    step = NoopStep()

    step(mock_mpt_client, context, mock_next_step)  # act

    mock_next_step.assert_called()


def test_create_subscription_step(mocker, context, mock_mpt_client, mock_next_step):
    mock_create_subscription = mocker.patch("swo_playground.steps.create_subscription")
    step = CreateSubscriptionStep()

    step(mock_mpt_client, context, mock_next_step)  # act

    expected_subscription = {
        "name": "Dummy subscription",
        "autoRenew": True,
        "lines": [],
    }
    mock_create_subscription.assert_called_once_with(
        mock_mpt_client, "ORD-123", expected_subscription
    )
    mock_next_step.assert_called()


def test_complete_order_step(mocker, context, mock_mpt_client, mock_next_step):
    mock_complete_order = mocker.patch("swo_playground.steps.complete_order")
    step = CompleteOrderStep()

    step(mock_mpt_client, context, mock_next_step)  # act

    mock_complete_order.assert_called_once_with(
        mock_mpt_client, "ORD-123", parameters={}, template=None
    )
    mock_next_step.assert_called()
