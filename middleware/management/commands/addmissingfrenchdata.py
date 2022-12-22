from django.core.management.base import BaseCommand
from middleware.loader.french import frenchdataloader

class Command(BaseCommand):
    help = 'add missing french data'

    def handle(self, *args, **kwargs):
        frenchdataloader.loadermissingfrenchdata()
