import logging

from mpt_extension_sdk.flows.context import Context
from mpt_extension_sdk.flows.pipeline import (
    NextStep,
    Pipeline,
    Step,
)
from mpt_extension_sdk.mpt_http.base import MPTClient
from mpt_extension_sdk.mpt_http.mpt import complete_order, create_subscription
from mpt_extension_sdk.mpt_http.wrap_http_error import MPTAPIError

logger = logging.getLogger(__name__)


class NoopStep(Step):  # type: ignore[misc]
    """
    Empty step.

    It actually does nothing, but useful to put your logic here.
    """

    def __call__(self, client: MPTClient, context: Context, next_step: NextStep) -> None:
        """Exectute step."""
        logger.info("%s - No operation step executed.", context.order_id)
        next_step(client, context)


class CreateSubscriptionStep(Step):  # type: ignore[misc]
    """Create subscription for all the Order lines."""

    def __call__(self, client: MPTClient, context: Context, next_step: NextStep) -> None:
        """Execute step."""
        subscription = {
            "name": "Dummy subscription",
            "autoRenew": True,
            "lines": [{"id": order_line["id"]} for order_line in context.order["lines"]],
        }
        try:
            create_subscription(client, context.order_id, subscription)
        except Exception:
            logger.exception("%s - Failed to create subscription.", context.order_id)
        logger.info("%s - Subscription created successfully.", context.order_id)
        next_step(client, context)


class CompleteOrderStep(Step):  # type: ignore[misc]
    """Complete order."""

    def __call__(self, client: MPTClient, context: Context, next_step: NextStep) -> None:
        """Execute step."""
        try:
            context.order = complete_order(
                client, context.order_id, template=None, parameters=context.order["parameters"]
            )
        except MPTAPIError:
            logger.exception("%s - Failed to complete order.", context.order_id)
        logger.info("%s - Order completed successfully.", context.order_id)
        next_step(client, context)


purchase_pipeline = Pipeline(
    NoopStep(),
    CreateSubscriptionStep(),
    CompleteOrderStep(),
)
