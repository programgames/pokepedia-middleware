# init.py
from django.core.management.base import BaseCommand
from middleware.install import installer

class Command(BaseCommand):
    help = 'Init project'

    def handle(self, *args, **kwargs):
        installer.install()
