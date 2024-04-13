from django.core.management.base import BaseCommand
from rich import print
from rich.console import Console
from rich.table import Table

class Command(BaseCommand):
    help = 'Description of your command'

    def handle(self, *args, **options):
        console = Console()

        # Example usage of rich.print
        print("[bold magenta]Welcome to the Django management command![/bold magenta]")

        # Example usage of rich.table
        table = Table(title="Sample Table")
        table.add_column("Column 1", justify="right", style="cyan", no_wrap=True)
        table.add_column("Column 2", style="magenta")
        table.add_row("Hello", "World")
        table.add_row("Django", "Rich")

        console.print(table)

        # Your command logic here
        # Use console.print(), print(), or other rich features for output
