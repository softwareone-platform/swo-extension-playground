import logging
from collections.abc import Mapping
from pprint import pformat
from typing import Annotated, Any, Literal

from django.conf import settings
from django.http import HttpRequest
from mpt_extension_sdk.core.extension import Extension  # type: ignore[import-untyped]
from mpt_extension_sdk.core.security import JWTAuth  # type: ignore[import-untyped]
from mpt_extension_sdk.flows.context import Context  # type: ignore[import-untyped]
from mpt_extension_sdk.mpt_http.base import MPTClient  # type: ignore[import-untyped]
from mpt_extension_sdk.mpt_http.mpt import get_webhook  # type: ignore[import-untyped]
from mpt_extension_sdk.runtime.djapp.conf import get_for_product  # type: ignore[import-untyped]
from ninja import Body, Schema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ext = Extension()


class Error(Schema):
    """MPT API error message."""

    id: str
    message: str


Response200 = tuple[Literal[200], dict[str, Any]]
Response400 = tuple[Literal[400], Error]
Response = Response200 | Response400


class ExtensionHttpRequest(HttpRequest):
    """Type for extension http request that adds MPT client throught the middleware."""

    client: MPTClient


def jwt_secret_callback(client: MPTClient, claims: Mapping[str, Any]) -> str:
    """Webhook jwt secret callback."""
    webhook = get_webhook(client, claims["webhook_id"])
    product_id = webhook["criteria"]["product.id"]
    return str(get_for_product(settings, "WEBHOOKS_SECRETS", product_id))


@ext.api.get(
    "/",
    description="Root endpoint.",
    response={
        200: dict,
        400: Error,
    },
)  # type: ignore[misc]
def root(request: ExtensionHttpRequest) -> Response:
    """Root endpoint."""
    return 200, {"message": "Ok"}


@ext.api.get(
    "/healthcheck",
    description="Healthcheck endpoint.",
    response={
        200: dict,
        400: Error,
    },
)  # type: ignore[misc]
def healthcheck(request: ExtensionHttpRequest) -> Response:
    """Returns 200 healthy."""
    return 200, {"status": "Healthy"}


@ext.api.post(
    "/v1/orders/validate",
    response={
        200: dict,
        400: Error,
    },
    auth=JWTAuth(jwt_secret_callback),
)  # type: ignore[misc]
def process_order_validation(
    request: ExtensionHttpRequest,
    order: Annotated[dict[str, Any] | None, Body()] = None,
) -> Response:
    """Process order draft validatin."""
    context = Context(order=order)
    try:
        validated_order = validate_order(request.client, context)
    except Exception as exc:
        logger.exception("Unexpected error during validation")
        return 400, Error(
            id="MPT001",
            message=f"Unexpected error during validation: {exc}.",
        )
    else:
        logger.debug("Validated order: %s", pformat(validated_order))
        return 200, validated_order


def validate_order(mpt_client: MPTClient, context: Context) -> Any:
    """Does nothing, just returns ok."""
    return context.order
