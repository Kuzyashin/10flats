from django.core.management.base import BaseCommand
from realty.models import RealtyComplex


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for realty_complex in RealtyComplex.objects.all():
            realty_complex.region = None
            realty_complex.city = None
            realty_complex.area = None
            realty_complex.save()
