import logging
from pprint import pformat
from typing import Any, Mapping

from django.conf import settings
from mpt_extension_sdk.core.security import JWTAuth
from mpt_extension_sdk.flows.context import Context
from mpt_extension_sdk.mpt_http.base import MPTClient
from mpt_extension_sdk.mpt_http.mpt import get_webhook
from mpt_extension_sdk.runtime.djapp.conf import get_for_product
from ninja import Body, Schema

from swo_playground.extension import ext

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Error(Schema):
    id: str
    message: str

def jwt_secret_callback(client: MPTClient, claims: Mapping[str, Any]) -> str:
    webhook = get_webhook(client, claims["webhook_id"])
    product_id = webhook["criteria"]["product.id"]
    return get_for_product(settings, "WEBHOOKS_SECRETS", product_id)


@ext.api.post(
    "/v1/orders/validate",
    response={
        200: dict,
        400: Error,
    },
    auth=JWTAuth(jwt_secret_callback),
)
def process_order_validation(request, order: dict = Body(None)):
    def validate_order(client: MPTClient, context: Context):
        return context.order
    try:
        context = Context(order=order)
        validated_order = validate_order(request.client, context)
        logger.debug(f"Validated order: {pformat(validated_order)}")
        return 200, validated_order
    except Exception as e:
        logger.exception(f"Unexpected error during validation. Error: {e}",)
        return 400, Error(
            id="AWS001",
            message=f"Unexpected error during validation: {str(e)}.",
        )
