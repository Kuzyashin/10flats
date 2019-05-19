from django.core.management.base import BaseCommand
from properites.models import TomTomPOI, TomTomSynonym, TomTomChildPOI
from core.utils.TomTom import TomTom
from realty.models import RealtyComplex
import os
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create tomtom places'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        maps = TomTom(token=os.environ['TOMTOM_API_KEY'])
        start_cat_list = [7372, 9362, 7332, ]
        for realty_complex in RealtyComplex.objects.all():
            maps.default_radius = 2000
            places = maps.get_nearby(
                lat=realty_complex.lat,
                lng=realty_complex.lng,
                category='',
                offset=0
            )