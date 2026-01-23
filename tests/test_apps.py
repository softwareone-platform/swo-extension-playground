from mpt_extension_sdk.core.extension import Extension

from swo_playground.apps import ExtensionConfig


def test_apps():
    result = ExtensionConfig

    assert result.name == "swo_playground"
    assert result.verbose_name == "SWO Playground Extension"
    assert isinstance(result.extension, Extension)
