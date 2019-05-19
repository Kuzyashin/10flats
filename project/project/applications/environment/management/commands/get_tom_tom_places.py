from django.core.management.base import BaseCommand
from properites.models import TomTomPOI, TomTomChildPOI
from environment.models import TomTomPlace
from core.utils.TomTom import TomTom
from realty.models import RealtyComplex
import os
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create tomtom places'

    def add_arguments(self, parser):
        pass

    def get_more_places(self, places_on_page, current_offset):
        maps = TomTom(token=os.environ['TOMTOM_API_KEY'])
        start_cat_list = [7372, 9362, 7332, 9361051, 9376, 7320002]
        for realty_complex in RealtyComplex.objects.all():
            maps.default_radius = '2000'
            places_data = maps.get_nearby(
                lat=realty_complex.lat,
                lng=realty_complex.lng,
                category='7372,9362,7332,9361051,9376,7320002',
                offset='{}'.format(places_on_page+current_offset)
            )
            places_total = places_data.get('summary').get('totalResults')
            places_on_page = places_data.get('summary').get('numResults')
            current_offset = places_data.get('summary').get('offset')
            raw_places = places_data.get('results')
            for raw_place in raw_places:
                try:
                    TomTomPlace.objects.get(tomtom_place_id=raw_place.get('id'))
                except TomTomPlace.DoesNotExist:
                    tom_place = TomTomPlace.objects.create(
                        name=raw_place.get('poi').get('name'),
                        address=raw_place.get('address'),
                        lat=raw_place.get('position').get('lat'),
                        lng=raw_place.get('position').get('lon'),
                        tomtom_place_id=raw_place.get('id')
                    )
                    for raw_category in raw_place.get('poi').get('categorySet'):
                        try:
                            category = TomTomPOI.objects.get(tom_id=str(raw_category.get('id')))
                        except TomTomPOI.DoesNotExist:
                            child = TomTomChildPOI.objects.get(tom_id=str(raw_category.get('id')))
                            category = TomTomPOI.objects.get(childCategory=child)
                        tom_place.childCategory.add(category)
                    tom_place.save()
            if places_total > places_on_page + current_offset:
                self.get_more_places( places_on_page, current_offset)

    def handle(self, *args, **options):
        maps = TomTom(token=os.environ['TOMTOM_API_KEY'])
        start_cat_list = [7372, 9362, 7332, 9361051, 9376, 7320002]
        for realty_complex in RealtyComplex.objects.all():
            maps.default_radius = '2000'
            places_data = maps.get_nearby(
                lat=realty_complex.lat,
                lng=realty_complex.lng,
                category='7372,9362,7332,9361051,9376,7320002',
                offset='0'
            )
            places_total = places_data.get('summary').get('totalResults')
            places_on_page = places_data.get('summary').get('numResults')
            current_offset = places_data.get('summary').get('offset')
            raw_places = places_data.get('results')
            for raw_place in raw_places:
                try:
                    TomTomPlace.objects.get(tomtom_place_id=raw_place.get('id'))
                except TomTomPlace.DoesNotExist:
                    tom_place = TomTomPlace.objects.create(
                        name=raw_place.get('poi').get('name'),
                        address=raw_place.get('address'),
                        lat=raw_place.get('position').get('lat'),
                        lng=raw_place.get('position').get('lon'),
                        tomtom_place_id=raw_place.get('id')
                    )
                    for raw_category in raw_place.get('poi').get('categorySet'):
                        try:
                            category = TomTomPOI.objects.get(tom_id=str(raw_category.get('id')))
                        except TomTomPOI.DoesNotExist:
                            child = TomTomChildPOI.objects.get(tom_id=str(raw_category.get('id')))
                            category = TomTomPOI.objects.get(childCategory=child)
                        tom_place.childCategory.add(category)
                    tom_place.save()
            if places_total > places_on_page + current_offset:
                self.get_more_places(places_on_page, current_offset)
