import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from mpt_extension_sdk.runtime.djapp.apps import DjAppConfig

from swo_playground.api import ext

logger = logging.getLogger(__name__)


class ExtensionConfig(DjAppConfig):  # type: ignore[misc]
    """Extension Django config."""

    name = "swo_playground"
    verbose_name = "SWO Playground Extension"
    extension = ext

    def extension_ready(self) -> None:
        """Checks if webhook and product ids is configured properly."""
        error_msgs = []

        for product_id in settings.MPT_PRODUCTS_IDS:
            if (
                "WEBHOOKS_SECRETS" not in settings.EXTENSION_CONFIG
                or product_id not in settings.EXTENSION_CONFIG["WEBHOOKS_SECRETS"]
            ):
                msg = (
                    f"The webhook secret for {product_id} is not found. "
                    f"Please, specify it in EXT_WEBHOOKS_SECRETS environment variable."
                )
                error_msgs.append(msg)

        if error_msgs:
            raise ImproperlyConfigured("\n".join(error_msgs))

        logger.info("Extension ready.")
