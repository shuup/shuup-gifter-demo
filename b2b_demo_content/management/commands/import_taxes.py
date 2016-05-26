import os

from django.core.management import BaseCommand
from django.db.transaction import atomic

from b2b_demo_content.importer import import_taxes

from django.utils import translation

class Command(BaseCommand):
    @atomic
    def handle(self, *args, **options):

        this_dir = os.path.dirname(__file__)
        data_path = os.path.realpath(os.path.join(this_dir, "..", "..", "data", "taxes"))

        translation.activate("en")

        import_taxes(data_path)
