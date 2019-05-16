from django.core.management.base import BaseCommand
from environment.models import Place
from realty.models import RealtyComplex
from core.models import DistanceMatrix
import googlemaps
import os


class Command(BaseCommand):
    help = 'Create google places'

    def add_arguments(self, parser):
        parser.add_argument('complex_pk')
        parser.add_argument('complex_pk_end')

    def handle(self, *args, **options):
        token = os.environ['GOOGLE_API_KEY']
        complex_pk = options['complex_pk']
        gmaps = googlemaps.Client(key=token)
        for ids in range(options['complex_id'], options['complex_id_end']):
            i=0
            compl = RealtyComplex.objects.get(pk=int(complex_pk))
            places_count = Place.objects.all().count()
            for place in Place.objects.all():
                i += 1
                try:
                    DistanceMatrix.objects.get(place=place, complex=compl)
                except DistanceMatrix.MultipleObjectsReturned:
                    print('Need to FIX THIS SHEET', DistanceMatrix.objects.filter(place=place, complex=compl))
                except DistanceMatrix.DoesNotExist:
                    result = gmaps.distance_matrix(
                        origins=(compl.lat, compl.lng),
                        destinations=(place.lat, place.lng),
                        mode='walking',
                        units='metric'
                    )
                    DistanceMatrix.objects.create(
                        complex=compl,
                        place=place,
                        distance=result.get('rows')[0].get('elements')[0].get('distance').get('value'),
                        duration=result.get('rows')[0].get('elements')[0].get('duration').get('value'),
                    )
                print('Current {} / Total {} / {}'.format(i, places_count, compl.pk))

