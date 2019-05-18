import googlemaps
import time
from django.core.management.base import BaseCommand

from environment.models import Place
from core.models import DistanceMatrix
from properites.models import PlaceType
from realty.models import RealtyComplex
import os


class Command(BaseCommand):
    help = 'Create google places'

    def add_arguments(self, parser):
        parser.add_argument('complex_id')
        parser.add_argument('complex_id_end')

    def handle(self, *args, **options):
        token = os.environ['TOMTOM_TOKEN']
        types = PlaceType.objects.all()
        gmaps = googlemaps.Client(key=token)

        for i in range(int(options['complex_id']), int(options['complex_id_end'])):
            realty_complex = RealtyComplex.objects.get(pk=int(i))
