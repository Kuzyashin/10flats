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

    def get_dist(self, place_pk, complex_pk, ti, tt):
        token = os.environ['GOOGLE_API_KEY']
        gmaps = googlemaps.Client(key=token)
        compl = RealtyComplex.objects.get(pk=complex_pk)
        place = Place.objects.get(pk=place_pk)
        try:
            DistanceMatrix.objects.get(place=place, complex=compl)
            print('Skipped place {} / complex {} / {} / {}'.format(place.pk, compl.pk, ti, tt))
        except DistanceMatrix.MultipleObjectsReturned:
            print('Need to FIX THIS SHEET',
                  DistanceMatrix.objects.filter(place=place, complex=compl))
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
            print('Created place {} / complex {} / {} / {}'.format(place.pk, compl.pk, ti, tt))

    def get_places(self, token, next_token, place_type, lat, lng, complex_pk, ti, tt):
        time.sleep(3)
        gmaps = googlemaps.Client(key=token)
        try:
            places = gmaps.places_nearby(
                location=(lat, lng),
                radius=3000,
                type=place_type,
                page_token=next_token
            )
            next_page_token = places.get('next_page_token', None)
            results = places.get('results')
            if results:
                for place in results:
                    try:
                        Place.objects.get(google_place_id=place.get('place_id'))
                        self.get_dist(Place.objects.get(google_place_id=place.get('place_id')).pk, complex_pk, ti, tt)
                    except Place.DoesNotExist:
                        if place.get('plus_code'):
                            new_place = Place.objects.create(
                                name=place.get('name'),
                                lat=place.get('geometry').get('location').get('lat'),
                                lng=place.get('geometry').get('location').get('lng'),
                                google_place_id=place.get('place_id', None),
                                google_plus_code=place.get('plus_code').get('compound_code', None),
                                address=place.get('vicinity', None),
                            )
                        else:
                            new_place = Place.objects.create(
                                name=place.get('name'),
                                lat=place.get('geometry').get('location').get('lat'),
                                lng=place.get('geometry').get('location').get('lng'),
                                google_place_id=place.get('place_id', None),
                                address=place.get('vicinity', None),
                            )
                        for pl_type in place.get('types'):
                            try:
                                new_place.place_type.add(PlaceType.objects.get(type=pl_type))
                            except PlaceType.DoesNotExist:
                                new_type = PlaceType.objects.create(type=pl_type)
                                new_type.save()
                                new_place.place_type.add(PlaceType.objects.get(type=pl_type))
                        new_place.save()
                        self.get_dist(new_place.pk, complex_pk, ti, tt)
            if next_page_token:
                self.get_places(token, next_page_token, place_type, lat, lng, complex_pk, ti , tt)
        except Exception as e:
            print(e)

    def handle(self, *args, **options):
        token = os.environ['GOOGLE_API_KEY']
        types = PlaceType.objects.all()
        gmaps = googlemaps.Client(key=token)

        for i in range(int(options['complex_id']), int(options['complex_id_end'])):
            realty_complex = RealtyComplex.objects.get(pk=options['complex_id'])
            count_types = types.count()
            ti = 0
            for place_type in types:
                ti += 1
                places = gmaps.places_nearby(
                    location=(realty_complex.lat, realty_complex.lng),
                    radius=3000,
                    type=place_type
                )
                next_page_token = places.get('next_page_token', None)
                results = places.get('results')
                if results:
                    for place in results:
                        try:
                            Place.objects.get(google_place_id=place.get('place_id'))
                            self.get_dist(Place.objects.get(google_place_id=place.get('place_id')).pk, realty_complex.pk, ti, count_types)
                        except Place.DoesNotExist:
                            if place.get('plus_code'):
                                new_place = Place.objects.create(
                                    name=place.get('name'),
                                    lat=place.get('geometry').get('location').get('lat'),
                                    lng=place.get('geometry').get('location').get('lng'),
                                    google_place_id=place.get('place_id', None),
                                    google_plus_code=place.get('plus_code').get('compound_code', None),
                                    address=place.get('vicinity', None),
                                )
                            else:
                                new_place = Place.objects.create(
                                    name=place.get('name'),
                                    lat=place.get('geometry').get('location').get('lat'),
                                    lng=place.get('geometry').get('location').get('lng'),
                                    google_place_id=place.get('place_id', None),
                                    address=place.get('vicinity', None),
                                )
                            for pl_type in place.get('types'):
                                try:
                                    new_place.place_type.add(PlaceType.objects.get(type=pl_type))
                                except PlaceType.DoesNotExist:
                                    new_type = PlaceType.objects.create(type=pl_type)
                                    new_type.save()
                                    new_place.place_type.add(PlaceType.objects.get(type=pl_type))
                            new_place.save()
                            self.get_dist(new_place.pk, realty_complex.pk, ti, count_types)
                if next_page_token:
                    self.get_places(token, next_page_token, place_type, realty_complex.lat, realty_complex.lng, realty_complex.pk, ti , count_types)
