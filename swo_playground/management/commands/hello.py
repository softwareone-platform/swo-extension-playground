from typing import Any

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Noop command."""

    help = "Hello world"

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: WPS110
        """Run command."""
        self.stdout.write("Hello world!!!", ending="\n")
