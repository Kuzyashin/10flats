import googlemaps
import time
from django.core.management.base import BaseCommand

from environment.models import Place
from properites.models import PlaceType
from realty.models import RealtyComplex
import os


class Command(BaseCommand):
    help = 'Create google places'

    def add_arguments(self, parser):
        parser.add_argument('complex_id')

    def get_places(self, token, next_token, place_type, lat, lng):
        time.sleep(3)
        gmaps = googlemaps.Client(key=token)
        try:
            places = gmaps.places_nearby(
                location=(lat, lng),
                radius=5000,
                type=place_type,
                page_token=next_token
            )
            next_page_token = places.get('next_page_token', None)
            print(next_page_token)
            results = places.get('results')
            if results:
                for place in results:
                    try:
                        Place.objects.get(google_place_id=place.get('place_id'))
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
            if next_page_token:
                self.get_places(token, next_page_token, place_type, lat, lng)
        except Exception as e:
            print(e)

    def handle(self, *args, **options):
        token = os.environ['GOOGLE_API_KEY']
        types = PlaceType.objects.all()
        realty_complex = RealtyComplex.objects.get(pk=options['complex_id'])
        gmaps = googlemaps.Client(key=token)

        for place_type in types:
            places = gmaps.places_nearby(
                location=(realty_complex.lat, realty_complex.lng),
                radius=5000,
                type=place_type
            )
            next_page_token = places.get('next_page_token', None)
            print(next_page_token)
            results = places.get('results')
            if results:
                for place in results:
                    try:
                        Place.objects.get(google_place_id=place.get('place_id'))
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
            if next_page_token:
                self.get_places(token, next_page_token, place_type, realty_complex.lat, realty_complex.lng)
