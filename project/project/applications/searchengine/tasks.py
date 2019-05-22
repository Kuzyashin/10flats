from celery.task import task
from .models import DistanceChoose, SearchV2
from .views import get_or_create_step
from realty.models import RealtyObject
from realty.serializers import RealtyObjectShortSerializer
from core.serializers import TomTomDistanceMatrixSerializer
import logging
import json
import ast

logger = logging.getLogger(__name__)

@task
def prepafe_final_json(search_pk):
    search = SearchV2.objects.get(pk=search_pk)
    realty_objects = RealtyObject.objects.filter(pk__in=ast.literal_eval(get_or_create_step(search, 9).result))
    _school_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 4).answer))
    _park_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 5).answer))
    _pharmacy_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 7).answer))
    _night_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 8).answer))
    _market_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 6).answer))
    _gym_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 9).answer))
    _school_percent_list = dict()
    _park_percent_list = dict()
    _pharmacy_percent_list = dict()
    _nightclub_percent_list = dict()
    _market_percent_list = dict()
    _gym_percent_list = dict()
    logger.info('Start calculating percent list')
    for realty_object in realty_objects:
        logger.info('Object {}'.format(realty_object))
        try:
            logger.info('Object {} GYM'.format(realty_object))
            if _gym_distance.distance == 0:
                _percent = 100
            elif _gym_distance.distance > 0:
                _distance = realty_object.realty_complex.tom_gym_dist.distance
                if _gym_distance.distance > _distance:
                    _percent = 100
                else:
                    _percent = 100 - (_distance - _gym_distance.distance) / _gym_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            else:
                _distance = realty_object.realty_complex.tom_gym_dist.distance
                if -_gym_distance.distance < _distance:
                    _percent = 100
                else:
                    _percent = 100 - (- _gym_distance.distance - _distance) / - _gym_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            _gym_json = {realty_object.pk: _percent}
            _gym_percent_list.update(_gym_json)
        except AttributeError as e:
            logger.warning('Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                     realty_object.realty_complex.tom_gym_dist,
                                                                     e))
            _gym_json = {realty_object.pk: 0}
            _gym_percent_list.update(_gym_json)

        try:
            logger.info('Object {} SCHOOL'.format(realty_object))
            if _school_distance.distance == 0:
                _percent = 100
            elif _school_distance.distance > 0:
                _distance = realty_object.realty_complex.tom_school_dist.distance
                if _school_distance.distance > _distance:
                    _percent = 100
                else:
                    _percent = 100 - (_distance - _school_distance.distance) / _school_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            else:
                _distance = realty_object.realty_complex.tom_school_dist.distance
                if -_school_distance.distance < _distance:
                    _percent = 100
                else:
                    _percent = 100 - (-_school_distance.distance - _distance) / -_school_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            _school_json = {realty_object.pk: _percent}
            _school_percent_list.update(_school_json)
        except AttributeError as e:
            logger.warning('Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                     realty_object.realty_complex.tom_school_dist,
                                                                     e))
            _gym_json = {realty_object.pk: 0}
            _gym_percent_list.update(_gym_json)
            ##

        try:
            logger.info('Object {} PHARMACY'.format(realty_object))
            if _pharmacy_distance.distance == 0:
                _percent = 100
            elif _pharmacy_distance.distance > 0:
                _distance = realty_object.realty_complex.tom_pharmacy_dist.distance
                if _pharmacy_distance.distance > _distance:
                    _percent = 100
                else:
                    _percent = 100 - (_distance - _pharmacy_distance.distance) / _pharmacy_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            else:
                _distance = realty_object.realty_complex.tom_pharmacy_dist.distance
                if -_pharmacy_distance.distance < _distance:
                    _percent = 100
                else:
                    _percent = 100 - (- _pharmacy_distance.distance - _distance) / - _pharmacy_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            _pharmacy_json = {realty_object.pk: _percent}
            _pharmacy_percent_list.update(_pharmacy_json)
        except AttributeError as e:
            logger.warning('Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                     realty_object.realty_complex.tom_pharmacy_dist,
                                                                     e))
            _pharmacy_json = {realty_object.pk: 0}
            _pharmacy_percent_list.update(_pharmacy_json)

            ##

        try:
            logger.info('Object {} NIGHT'.format(realty_object))
            if _night_distance.distance == 0:
                _percent = 100
            elif _night_distance.distance > 0:
                _distance = realty_object.realty_complex.tom_nightclub_dist.distance
                if _night_distance.distance > _distance:
                    _percent = 100
                else:
                    _percent = 100 - (_distance - _night_distance.distance) / _night_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            else:
                _distance = realty_object.realty_complex.tom_nightclub_dist.distance
                if -_night_distance.distance < _distance:
                    _percent = 100
                else:
                    _distance = realty_object.realty_complex.tom_nightclub_dist.distance
                    _percent = 100 - (- _night_distance.distance - _distance) / - _night_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            _nightclub_json = {realty_object.pk: _percent}
            _nightclub_percent_list.update(_nightclub_json)
        except AttributeError as e:
            logger.warning('Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                     realty_object.realty_complex.tom_nightclub_dist,
                                                                     e))
            _nightclub_json = {realty_object.pk: 0}
            _nightclub_percent_list.update(_nightclub_json)

            ##

        try:
            logger.info('Object {} MARKET'.format(realty_object))
            if _market_distance.distance == 0:
                _percent = 100
            elif _market_distance.distance > 0:
                _distance = realty_object.realty_complex.tom_market_dist.distance
                if _market_distance.distance > _distance:
                    _percent = 100
                else:
                    _percent = 100 - (_distance - _market_distance.distance) / _market_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            else:
                _distance = realty_object.realty_complex.tom_market_dist.distance
                if -_market_distance.distance < _distance:
                    _percent = 100
                else:
                    _percent = 100 - (- _market_distance.distance - _distance) / - _market_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            _market_json = {realty_object.pk: _percent}
            _market_percent_list.update(_market_json)
        except AttributeError as e:
            logger.warning('Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                     realty_object.realty_complex.tom_market_dist,
                                                                     e))
            _market_json = {realty_object.pk: 0}
            _market_percent_list.update(_market_json)

        try:
            logger.info('Object {} PARK'.format(realty_object))
            if _park_distance.distance == 0:
                _percent = 100
            elif _park_distance.distance > 0:
                _distance = realty_object.realty_complex.tom_park_dist.distance
                if _park_distance.distance > _distance:
                    _percent = 100
                else:
                    _percent = 100 - (_distance - _park_distance.distance) / _park_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            else:
                _distance = realty_object.realty_complex.tom_park_dist.distance
                if -_park_distance.distance < _distance:
                    _percent = 100
                else:
                    _percent = 100 - (- _park_distance.distance - _distance) / - _park_distance.distance * 100
                    if _percent < 0:
                        _percent = 0
            _park_json = {realty_object.pk: _percent}
            _park_percent_list.update(_park_json)
        except AttributeError as e:
            logger.warning('Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                     realty_object.realty_complex.tom_park_dist,
                                                                     e))
            _park_json = {realty_object.pk: 0}
            _park_percent_list.update(_park_json)

    _final_list = []
    logger.info('Calculate completed. Preparing final JSON')
    for realty_object in realty_objects:
        try:
            logger.info('Preparing final JSON for {}'.format(realty_object.pk))
            _object_json = {
                "scoring": {
                    "gym": int(_gym_percent_list.get(realty_object.pk)),
                    "school": int(_school_percent_list.get(realty_object.pk)),
                    "park": int(_park_percent_list.get(realty_object.pk)),
                    "pharmacy": int(_pharmacy_percent_list.get(realty_object.pk)),
                    "cafe": int(_nightclub_percent_list.get(realty_object.pk)),
                    "market": int(_market_percent_list.get(realty_object.pk)),
                    "total": (int(_school_percent_list.get(realty_object.pk)) +
                              int(_park_percent_list.get(realty_object.pk)) +
                              int(_pharmacy_percent_list.get(realty_object.pk)) +
                              int(_nightclub_percent_list.get(realty_object.pk)) +
                              int(_gym_percent_list.get(realty_object.pk)) +
                              int(_market_percent_list.get(realty_object.pk))) / 6
                },
                "info": RealtyObjectShortSerializer(realty_object).data,
                "nearby": {
                    "school": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_school_dist).data,
                    "gym": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_gym_dist).data,
                    "park": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_park_dist).data,
                    "pharmacy": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_pharmacy_dist).data,
                    "cafe": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_nightclub_dist).data,
                    "market": TomTomDistanceMatrixSerializer(realty_object.realty_complex.tom_market_dist).data,
                }
            }
            _final_list.append(_object_json)
        except Exception as e:
            logger.warning('Some shit happens \n{}'.format(e))
    logger.info('JSON prepared. Start SORT')

    def extract_score(json):
        try:
            return int(json['scoring']['total'])
        except KeyError:
            return 0

    _final_list.sort(key=extract_score, reverse=True)
    logger.info('JSON Sorted. Save')
    search.result_full = json.dumps(_final_list)
    logger.info('Full Saved')
    search.result = json.dumps(_final_list[:10])
    search.save()
    logger.info('Short saved')