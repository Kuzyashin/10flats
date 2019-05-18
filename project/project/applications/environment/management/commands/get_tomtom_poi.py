from django.core.management.base import BaseCommand
from properites.models import TomTomPOI, TomTomSynonym
from core.utils.TomTom import TomTom
import os
import logging


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create google places'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        token = os.environ['TOMTOM_API_KEY']
        provider = TomTom(token)
        poi_list = provider.get_categories()
        for poi in poi_list:
            try:
                point = TomTomPOI.objects.get(tom_id=poi.get('id'))
            except TomTomPOI.DoesNotExist:
                if len(poi.get('childCategoryIds')) > 0:
                    point = TomTomPOI.objects.create(
                        tom_id=poi.get('id'),
                        name=poi.get('name')
                    )
                    point.save()
                    for child_id in poi.get('childCategoryIds'):
                        try:
                            child = TomTomPOI.objects.get(tom_id=child_id)
                            point.childCategory.add(child)
                        except TomTomPOI.DoesNotExist:
                            logger.warning('No data for first run {}'.format(point.pk))
                    for synonim in poi.get('synonyms'):
                        try:
                            syn = TomTomSynonym.objects.get(name=synonim)
                            point.synonyms.add(syn)
                        except TomTomSynonym.DoesNotExist:
                            syn = TomTomSynonym.objects.create(name=synonim)
                            point.synonyms.add(syn)
                    point.save()
