from django.core.management.base import BaseCommand
from properites.models import Area
import requests


class Command(BaseCommand):
    help = 'Create google places'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        url = 'https://nominatim.openstreetmap.org/search?q=Estonia+Tallin+{}+linnaosa&polygon_geojson=1&format=json&type=boundary'
        areas = Area.objects.all()
        for area in areas:
            data = requests.get(url.format(area.area))
            data = data.json()[0]
            geojson = data.get('geojson').get('coordinates')[0]
            area.geojson = geojson
            area.save()
