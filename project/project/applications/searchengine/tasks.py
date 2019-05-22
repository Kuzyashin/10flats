from celery.task import task
from .models import SearchV2, SearchV2step
from realty.models import RealtyObject
from realty.serializers import RealtyObjectShortSerializer
from core.serializers import TomTomDistanceMatrixSerializer
import logging
import json

logger = logging.getLogger(__name__)


def get_or_create_step(search, step_pos):
    try:
        step = SearchV2step.objects.get(search=search, step_pos=step_pos)
        return step
    except SearchV2step.DoesNotExist:
        step = SearchV2step.objects.create(
            search=search,
            step_pos=step_pos,
        )
        return step

@task
def prepare_final_json(search_pk):
    search = SearchV2.objects.get(pk=search_pk)
    _final_list = json.loads(search.result_full)
    for i in _final_list:
        realty_object = RealtyObject.objects.get(pk=i.get('object_id'))
        data = {"info": RealtyObjectShortSerializer(realty_object).data,
                "nearby": {
                    "school": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_school_dist).data,
                    "gym": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_gym_dist).data,
                    "park": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_park_dist).data,
                    "pharmacy": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_pharmacy_dist).data,
                    "cafe": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_nightclub_dist).data,
                    "market": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_market_dist).data,
                }}
        i.update(data)
    search.result_full = json.dumps(_final_list)
    search.save()
    logger.info('Full Saved')

