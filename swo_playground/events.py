from mpt_extension_sdk.core.events.dataclasses import Event
from mpt_extension_sdk.mpt_http.base import MPTClient

from swo_playground.api import ext, logger
from swo_playground.steps import purchase_pipeline


@ext.events.listener("orders")  # type: ignore[untyped-decorator]
def process_order_fulfillment(client: MPTClient, event: Event) -> None:
    """Event handler for FF orders."""
    context = event.data
    logger.info(f"{context.order_id} - Order fulfilling...")

    purchase_pipeline.run(client, context)
    logger.info(f"{context.order_id} - Order fulfilled.")
