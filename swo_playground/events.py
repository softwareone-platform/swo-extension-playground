from mpt_extension_sdk.core.events.dataclasse import Event  # type: ignore[import-untyped]
from mpt_extension_sdk.mpt_http.base import MPTClient  # type: ignore[import-untyped]

from swo_playground.api import logger
from swo_playground.apps import ext
from swo_playground.steps import purchase_pipeline


@ext.events.listener("orders")  # type: ignore[misc]
def process_order_fulfillment(client: MPTClient, event: Event) -> None:
    """Event handler for FF orders."""
    context = event.data
    logger.info(f"{context.order_id} - Order fulfilling...")

    purchase_pipeline.run(client, context)
    logger.info(f"{context.order_id} - Order fulfilled.")
