from copy import deepcopy

from mpt_extension_sdk.flows.context import Context
from mpt_extension_sdk.flows.pipeline import Step, Pipeline, NextStep
import logging

from mpt_extension_sdk.mpt_http.base import MPTClient
from mpt_extension_sdk.mpt_http.mpt import complete_order, create_subscription
from mpt_extension_sdk.mpt_http.wrap_http_error import MPTAPIError

logger = logging.getLogger(__name__)


class NoopStep(Step):
    def __call__(
        self,
        client: MPTClient,
        context: Context,
        next_step: NextStep,
    ) -> None:
        logger.info(f"{context.order_id} - No operation step executed.")
        next_step(client, context)

class CreateSubscriptionStep(Step):
    def __call__(
        self,
        client: MPTClient,
        context: Context,
        next_step: NextStep,
    ) -> None:
        # Here you would implement the logic to create a subscription
        # For demonstration, we will just log the action
        subscription = {
            "name": f"Dummy subscription",
            "autoRenew": True,
            "lines": [{"id": order_line["id"]} for order_line in context.order["lines"]],
        }
        try:
            create_subscription(client, context.order_id, subscription)
            logger.info(f"{context.order_id} - Subscription created successfully.")
        except Exception as e:
            logger.error(f"{context.order_id} - Failed to create subscription: {e}")
        next_step(client, context)

class CompleteOrderStep(Step):
    def __call__(
        self,
        client: MPTClient,
        context: Context,
        next_step: NextStep,
    ) -> None:
        try:
            context.order = complete_order(
                client,
                context.order_id,
                template=None,
                parameters=context.order["parameters"]
            )
        except MPTAPIError as e:
            logger.error(f"{context.order_id} - Failed to complete order: {e}")
        logger.info(f"{context.order_id} - Order completed successfully.")
        next_step(client, context)


purchase_pipeline = Pipeline(
    NoopStep(),
    CreateSubscriptionStep(),
    CompleteOrderStep(),
)