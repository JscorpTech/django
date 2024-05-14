"""
Clear cache command
"""
from django.core.cache import cache
from django.core.management import BaseCommand

from core.utils import console


class Command(BaseCommand):
    help = "Clear all caches"

    def handle(self, *args, **options):
        cache.clear()
        console.Console.success("Cache cleared successfully")
