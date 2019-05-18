from django.core.management.base import BaseCommand
from properites.models import Area
import requests


class Command(BaseCommand):
    help = 'Create google places'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        url = 'https://nominatim.openstreetmap.org/search?q=Estonia+Tallinn+{}&polygon_geojson=1&format=json'
        areas = Area.objects.all()
        for area in areas:
            area.geojson = None
            dataz = requests.get(url.format(area.area)).json()
            for data in dataz:
                print(data.get('class'))
                if data.get('class') == 'boundary':
                    try:
                        geojson = data.get('geojson')
                        area.geojson = geojson
                        area.save()
                    except Exception:
                        print('No data for {}'.format(area.area))
            if not area.geojson:
                for data in dataz:
                    print(data.get('class'))
                    if data.get('class') == 'point':
                        try:
                            data = data.json()
                            geojson = data.get('geojson')
                            area.geojson = geojson
                            area.save()
                        except Exception:
                            print('No data for {}'.format(area.area))
