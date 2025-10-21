import os

os.environ.setdefault("MPT_INITIALIZER", "swo_playground.initializer.initialize")
from mpt_extension_sdk.constants import (  # type: ignore[import-untyped]
    DEFAULT_APP_CONFIG_GROUP,
    DEFAULT_APP_CONFIG_NAME,
)
from mpt_extension_sdk.runtime.initializer import (  # type: ignore[import-untyped]
    initialize as sdk_initialize,
)


def initialize(options, group=DEFAULT_APP_CONFIG_GROUP, name=DEFAULT_APP_CONFIG_NAME):
    """Custom initializaer of extension."""
    options["django_settings_module"] = "swo_playground.default"

    sdk_initialize(
        options=options,
        group=group,
        name=name,
    )

    import django  # noqa: PLC0415

    django.setup()
