# clearcache.py
from django.core.management.base import BaseCommand
from middleware.models import CacheItem
from pokeapi.pokemon_v2.models import Language

language = Language.objects.get(name='fr')

class Command(BaseCommand):
    help = 'Clear cache'
    def handle(self, *args, **kwargs):
        deleted_count, _ = CacheItem.objects.all().delete()
        self.stdout.write(f"{deleted_count} cache item(s) deleted")
