from django.core.management.base import BaseCommand
from realty.models import RealtyComplex


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for realty_complex in RealtyComplex.objects.all():
            market = realty_complex.tom_market_dist
            gym = realty_complex.tom_gym_dist
            nightclub = realty_complex.tom_nightclub_dist
            pharmacy = realty_complex.tom_pharmacy_dist
            school = realty_complex.tom_school_dist
            park = realty_complex.tom_park_dist
            realty_complex.nearest_market = market
            realty_complex.nearest_gym = gym
            realty_complex.nearest_nightclub = nightclub
            realty_complex.nearest_pharmacy = pharmacy
            realty_complex.nearest_school = school
            realty_complex.nearest_park = park
            realty_complex.save()
