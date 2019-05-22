from django.core.management.base import BaseCommand
from properites.models import TomTomPOI
from environment.models import TomTomPlace
from core.utils.TomTom import TomTom
from core.models import TomTomDistanceMatrix
from realty.models import RealtyComplex
import os
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create min tomtom places'

    def add_arguments(self, parser):
        parser.add_argument('complex_pk')

    def handle(self, *args, **options):
        maps = TomTom(token=os.environ['TOMTOM_API_KEY'])
        complex_pk = options['complex_pk']
        for realty_complex in RealtyComplex.objects.filter(lat__isnull=False, lng__isnull=False, pk__gt=complex_pk):
            logger.info('realty_complex PK = {}'.format(realty_complex.pk))
            maps.default_radius = '2000'
            cat_list = [7372, 9362, 7332, 9376, 7320, 9361051]
            for cat in cat_list:
                places_data = maps.get_nearby(
                    lat=realty_complex.lat,
                    lng=realty_complex.lng,
                    category='{}'.format(cat),
                    offset=0
                )
                raw_places = places_data.get('results')
                for raw_place in raw_places[:3]:
                    try:
                        tom_place = TomTomPlace.objects.get(tomtom_place_id=raw_place.get('id'))
                        try:
                            distm = TomTomDistanceMatrix.objects.get(complex=realty_complex, place=tom_place)
                            if not distm.route:
                                remoteness = maps.get_route(realty_complex.lat, realty_complex.lng, tom_place.lat,
                                                            tom_place.lng)
                                try:
                                    route = remoteness.get('routes')[0]
                                    distm.route = route.get('legs')
                                    distm.save()
                                except Exception as e:
                                    logger.warning('No data for point {} and complex {} with err\n{}'.
                                                   format(tom_place.pk, realty_complex.pk, e))
                        except TomTomDistanceMatrix.DoesNotExist:
                            remoteness = maps.get_route(realty_complex.lat, realty_complex.lng, tom_place.lat, tom_place.lng)
                            try:
                                route = remoteness.get('routes')[0]
                                data = route.get('summary')
                                dist_matrix = TomTomDistanceMatrix.objects.create(
                                    complex=realty_complex,
                                    place=tom_place,
                                    distance=data.get('lengthInMeters'),
                                    duration=data.get('travelTimeInSeconds'),
                                    route=route.get('legs')
                                )
                                dist_matrix.save()
                            except Exception as e:
                                logger.warning('No data for point {} and complex {} with err\n{}'.
                                               format(tom_place.pk, realty_complex.pk, e))
                    except TomTomPlace.DoesNotExist:
                        tom_place = TomTomPlace.objects.create(
                            name=raw_place.get('poi').get('name'),
                            address=raw_place.get('address'),
                            lat=raw_place.get('position').get('lat'),
                            lng=raw_place.get('position').get('lon'),
                            tomtom_place_id=raw_place.get('id')
                        )
                        for raw_category in raw_place.get('poi').get('categorySet'):
                            category = TomTomPOI.objects.get(tom_id=str(raw_category.get('id')))
                            tom_place.place_type.add(category)
                        tom_place.save()
                        try:
                            remoteness = TomTomDistanceMatrix.objects.get(complex=realty_complex, place=tom_place)
                            if not remoteness.route:
                                remoteness = maps.get_route(realty_complex.lat, realty_complex.lng, tom_place.lat,
                                                            tom_place.lng)
                                try:
                                    route = remoteness.get('routes')[0]
                                    data = route.get('summary')
                                    dist_matrix = TomTomDistanceMatrix.objects.create(
                                        complex=realty_complex,
                                        place=tom_place,
                                        distance=data.get('lengthInMeters'),
                                        duration=data.get('travelTimeInSeconds'),
                                        route=route.get('legs')
                                    )
                                    dist_matrix.save()
                                except Exception as e:
                                    logger.warning('No data for point {} and complex {} with err\n{}'.
                                                   format(tom_place.pk, realty_complex.pk, e))
                        except TomTomDistanceMatrix.DoesNotExist:
                            remoteness = maps.get_route(realty_complex.lat, realty_complex.lng, tom_place.lat, tom_place.lng)
                            try:
                                route = remoteness.get('routes')[0]
                                data = route.get('summary')
                                dist_matrix = TomTomDistanceMatrix.objects.create(
                                    complex=realty_complex,
                                    place=tom_place,
                                    distance=data.get('lengthInMeters'),
                                    duration=data.get('travelTimeInSeconds'),
                                    route=route.get('legs')
                                )
                                dist_matrix.save()
                            except Exception as e:
                                logger.warning('No data for point {} and complex {} with err\n{}'.
                                               format(tom_place.pk, realty_complex.pk, e))
