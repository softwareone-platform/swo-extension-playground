import os
from typing import Any

os.environ.setdefault("MPT_INITIALIZER", "swo_playground.initializer.initialize")
from mpt_extension_sdk.constants import DEFAULT_APP_CONFIG_GROUP, DEFAULT_APP_CONFIG_NAME
from mpt_extension_sdk.runtime.initializer import initialize as sdk_initialize


def initialize(
    options: dict[str, Any],
    group: str = DEFAULT_APP_CONFIG_GROUP,
    name: str = DEFAULT_APP_CONFIG_NAME,
) -> None:
    """Custom initializer of extension."""
    options["django_settings_module"] = "swo_playground.default"
    sdk_initialize(options=options, group=group, name=name)

    import django  # noqa: PLC0415

    django.setup()
