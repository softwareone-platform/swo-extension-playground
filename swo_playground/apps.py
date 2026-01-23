from mpt_extension_sdk.runtime.djapp.apps import DjAppConfig

from swo_playground.api import ext


class ExtensionConfig(DjAppConfig):  # type: ignore[misc]
    """Extension Django config."""

    name = "swo_playground"
    verbose_name = "SWO Playground Extension"
    extension = ext
