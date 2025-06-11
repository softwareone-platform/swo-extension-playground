from mpt_extension_sdk.flows.context import Context

from swo_playground.api import logger
from swo_playground.extension import ext
from swo_playground.purchase import purchase_pipeline


@ext.events.listener("orders")
def process_order_fulfillment(client, event):

    context = event.data  # type: Context
    logger.info(f"{context.order_id} - Order fulfilling...")

    purchase_pipeline.run(client, context)
    logger.info(f"{context.order_id} - Order fulfilled.")
