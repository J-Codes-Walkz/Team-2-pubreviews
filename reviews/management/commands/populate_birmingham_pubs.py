from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seeds the Birmingham pub directory with clean unreviewed pub listings (no fake reviews or likes)."

    def handle(self, *args, **options):
        call_command("import_all_birmingham_pubs", offline=True)
