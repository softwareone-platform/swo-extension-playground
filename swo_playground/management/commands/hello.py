from typing import Any, override

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Noop command."""

    help = "Hello world"

    @override
    def handle(self, *args: Any, **options: Any) -> None:  # noqa: WPS110
        """Run command."""
        self.stdout.write("Hello world!!!", ending="\n")
