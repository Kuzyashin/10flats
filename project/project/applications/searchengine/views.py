import ast
import json
import os
import logging

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from .tasks import prepare_final_json

from django.db.models import Max, Min
from django.utils import timezone
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from core.utils import TomTom
from core.serializers import TomTomDistanceMatrixSerializer

from properites.models import Area
from properites.serializers import AreaSerializer

from realty.models import RealtyObject
from realty.serializers import RealtyObjectShortSerializer

from .models import DistanceChoose, RequestViewing
from .models import PercentPass, SearchV2, SearchV2step, TravelType
from .serializers import DistanceChooseSerializer, TravelTypeSerializer

logger = logging.getLogger(__name__)
maps = TomTom.TomTom(token=os.environ['TOMTOM_API_KEY'])


class TrackViewingViewSet(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data
        user_id = data.get('user_id')
        realty_object = data.get('realty_object')
        search_hashed = data.get('search_hashed', None)
        if search_hashed:
            RequestViewing.objects.create(
                user_identify=user_id,
                search=SearchV2.objects.get(hashed_id=search_hashed),
                realty_object=RealtyObject.objects.get(pk=realty_object),
                created_at=timezone.now()
            )
        else:
            RequestViewing.objects.create(
                user_identify=user_id,
                realty_object=RealtyObject.objects.get(pk=realty_object),
                created_at=timezone.now()
            )
        return Response(data="OK", status=200)


class SearchV2GetViewSet(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, search_hashed):
        search = get_object_or_404(SearchV2, hashed_id=search_hashed)
        resp_data = {
            "result": json.loads(search.result),
            "search_id": search.pk,
            "search_start": search.created_at,
            "search_finish": search.finished_at
        }
        return Response(data=resp_data, status=200)

    def post(self, request, search_hashed):
        search = get_object_or_404(SearchV2, hashed_id=search_hashed)
        resp_data = {
            "result": json.loads(search.result),
            "search_id": search.pk,
            "search_start": search.created_at,
            "search_finish": search.finished_at
        }
        return Response(data=resp_data, status=200)


def get_or_create_step(search, step_pos):
    try:
        step = SearchV2step.objects.get(search=search, step_pos=step_pos)
        return step
    except SearchV2step.DoesNotExist:
        step = SearchV2step.objects.create(
            search=search,
            step_pos=step_pos,
            created_at=timezone.now()
        )
        return step


class SearchV2ViewSet(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    """
    _step_1 - Выбор районов
    _step_2 - Выбор работы и времени в пути
    _step_3 - Выбор кол-ва комнат
    _step_4 - Выбор мин/макс суммы
    _step_5 - Школы
    _step_6 - парки
    _step_7 - Супермаркеты
    _step_8 - Аптеки
    _step_9 - Ночная жизнь
    _step_10 - Спортзалы
    """

    def post(self, request, format=None):
        data = request.data
        user_id = data.get('user_id')

        if data.get('step') == '0' or data.get('step') == 0:
            search = SearchV2.objects.create(
                user_identify=user_id,
                created_at=timezone.now(),
                last_step=1
            )
            search.save()
            area_list = Area.objects.all()
            serialized = AreaSerializer(area_list, many=True)
            resp_data = {"step": 1,
                         "template": "step_1",
                         "answers": serialized.data,
                         "count": RealtyObject.objects.all().count()}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '1' or data.get('step') == 1:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            try:
                areas_pk = ast.literal_eval(data.get('data'))
            except ValueError:
                areas_pk = data.get('data')
            search.last_step = 2
            search.save()
            realty_objects = RealtyObject.objects.filter(realty_complex__area_id__in=areas_pk,
                                                         realty_complex__lat__isnull=False,
                                                         realty_complex__lng__isnull=False)
            count = realty_objects.count()
            step_1 = get_or_create_step(search=search, step_pos=1)
            step_1.answer = areas_pk
            step_1.result = [realty_object.pk for realty_object in realty_objects]
            step_1.save()
            travel_types = TravelType.objects.filter(is_active=True)
            serialized = TravelTypeSerializer(travel_types, many=True)
            bounds_data = {
                "topLeft": [59.509087, 24.527257],
                "btmRight": [59.353837, 24.945407]
            }
            resp_data = {"step": 2,
                         "template": "step_2",
                         "answers": serialized.data,
                         "bounds": bounds_data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '2' or data.get('step') == 2:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            try:
                place_data = ast.literal_eval(data.get('data'))
            except ValueError:
                place_data = data.get('data')
            search.last_step = 2
            search.save()
            step_2 = get_or_create_step(search=search, step_pos=2)
            step_2.answer = place_data
            step_2.result = get_or_create_step(search=search, step_pos=1).result
            step_2.save()
            realty_objects = RealtyObject.objects.filter(pk__in=ast.literal_eval(
                get_or_create_step(search=search, step_pos=2).result))
            count = realty_objects.count()
            step_2.result = [realty_object.pk for realty_object in realty_objects]
            step_2.save()
            room_list = realty_objects.distinct('rooms_count').values('rooms_count')
            resp_data = {"step": 3,
                         "template": "step_3",
                         "answers": room_list,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '3' or data.get('step') == 3:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            try:
                rooms_count = ast.literal_eval(data.get('data'))
            except ValueError:
                rooms_count = data.get('data')
            search.last_step = 4
            search.save()
            min_room = rooms_count[0]
            max_room = rooms_count[1]
            step_3 = get_or_create_step(search=search, step_pos=3)
            step_3.answer = rooms_count
            step_3.created_at = timezone.now()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=2).result),
                rooms_count__range=(min_room, max_room))
            step_3.result = [realty_object.pk for realty_object in realty_objects]
            step_3.save()
            count = realty_objects.count()
            min_price = realty_objects.aggregate(Min('rent_price_eur'))
            max_price = realty_objects.aggregate(Max('rent_price_eur'))
            resp_data = {"step": 4,
                         "template": "step_4",
                         "answers": {"min_price": min_price, "max_price": max_price},
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '4' or data.get('step') == 4:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            try:
                min_max_price = ast.literal_eval(data.get('data'))
            except ValueError:
                min_max_price = data.get('data')
            search.last_step = 5
            search.save()
            step_4 = get_or_create_step(search=search, step_pos=4)
            min_price = min_max_price[0]
            max_price = min_max_price[1]
            step_4.answer = min_max_price
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=3).result),
                rent_price_eur__range=(min_price, max_price)
            )
            step_4.result = [realty_object.pk for realty_object in realty_objects]
            step_4.save()
            count = realty_objects.count()
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 5,
                         "template": "step_5",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '5' or data.get('step') == 5:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            step_5 = get_or_create_step(search=search, step_pos=5)
            step_5.answer = data.get('data')[0]
            search.last_step = 6
            search.save()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=4).result),
            )
            _school_distance = DistanceChoose.objects.get(pk=int(step_5.answer))
            percent = PercentPass.objects.last().percent
            if _school_distance.distance > 0:
                step_5.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_school__distance__lte=
                                                       _school_distance.distance / percent * 100)]
            elif _school_distance.distance < 0:
                step_5.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(
                                     realty_complex__nearest_school__distance__gte=
                                     (-_school_distance.distance) / percent * 100)]
            else:
                step_5.result = ast.literal_eval(get_or_create_step(search=search, step_pos=4).result)
            step_5.save()
            count = len(step_5.result)
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 6,
                         "template": "step_6",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '6' or data.get('step') == 6:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            step_6 = get_or_create_step(search=search, step_pos=6)
            step_6.answer = data.get('data')[0]
            step_6.save()
            search.last_step = 7
            search.save()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=5).result),
            )
            _park_distance = DistanceChoose.objects.get(pk=int(step_6.answer))
            percent = PercentPass.objects.last().percent
            if _park_distance.distance > 0:
                step_6.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_park__distance__lte=
                                                       _park_distance.distance / percent * 100)]
            elif _park_distance.distance < 0:
                step_6.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_park__distance__lte=(
                                 -_park_distance.distance) / percent * 100)]
            else:
                step_6.result = ast.literal_eval(get_or_create_step(search=search, step_pos=5).result)
            step_6.save()
            count = len(step_6.result)
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 7,
                         "template": "step_7",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '7' or data.get('step') == 7:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            step_7 = get_or_create_step(search=search, step_pos=7)
            step_7.answer = data.get('data')[0]
            search.last_step = 8
            search.save()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=6).result),
            )
            _market_distance = DistanceChoose.objects.get(pk=int(step_7.answer))
            percent = PercentPass.objects.last().percent
            if _market_distance.distance > 0:
                step_7.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_market__distance__lte=
                                                       _market_distance.distance / percent * 100)]
            elif _market_distance.distance < 0:
                step_7.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_market__distance__lte=(
                                 -_market_distance.distance) / percent * 100)]
            else:
                step_7.result = ast.literal_eval(get_or_create_step(search=search, step_pos=6).result)
            step_7.save()
            count = len(step_7.result)
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 8,
                         "template": "step_8",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '8' or data.get('step') == 8:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            step_8 = get_or_create_step(search=search, step_pos=8)
            step_8.answer = data.get('data')[0]
            search.last_step = 9
            search.save()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=7).result),
            )
            _pharmacy_distance = DistanceChoose.objects.get(pk=int(step_8.answer))
            percent = PercentPass.objects.last().percent
            if _pharmacy_distance.distance > 0:
                step_8.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_pharmacy__distance__lte=
                                                       _pharmacy_distance.distance / percent * 100)]
            elif _pharmacy_distance.distance < 0:
                step_8.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_pharmacy__distance__lte=(
                                 -_pharmacy_distance.distance) / percent * 100)]
            else:
                step_8.result = ast.literal_eval(get_or_create_step(search=search, step_pos=7).result)
            step_8.save()
            count = len(step_8.result)
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 9,
                         "template": "step_9",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '9' or data.get('step') == 9:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            step_9 = get_or_create_step(search=search, step_pos=9)
            step_9.answer = data.get('data')[0]
            search.last_step = 10
            search.save()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=8).result),
            )
            _night_distance = DistanceChoose.objects.get(pk=int(step_9.answer))
            percent = PercentPass.objects.last().percent
            if _night_distance.distance > 0:
                step_9.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_nightclub__distance__lte=
                                                       _night_distance.distance / percent * 100)]
            elif _night_distance.distance < 0:
                step_9.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_nightclub__distance__lte=(
                                 -_night_distance.distance) / percent * 100)]
            else:
                step_9.result = ast.literal_eval(get_or_create_step(search=search, step_pos=8).result)
            step_9.save()
            count = len(step_9.result)
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 10,
                         "template": "step_10",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '10' or data.get('step') == 10:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            step_10 = get_or_create_step(search=search, step_pos=10)
            step_10.answer = data.get('data')[0]
            search.last_step = 11
            search.save()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=9).result),
            )
            _gym_distance = DistanceChoose.objects.get(pk=int(step_10.answer))
            percent = PercentPass.objects.last().percent
            if _gym_distance.distance > 0:
                step_10.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_gym__distance__lte=
                                                       _gym_distance.distance / percent * 100)]
            elif _gym_distance.distance < 0:
                step_10.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_gym__distance__lte=(
                                 -_gym_distance.distance) / percent * 100)]
            else:
                step_10.result = ast.literal_eval(get_or_create_step(search=search, step_pos=9).result)
            step_10.save()
            """
            _step_1 - Выбор районов
            _step_2 - Выбор кол-ва комнат
            _step_3 - Выбор мин/макс суммы
            _step_4 - Школы
            _step_5 - парки
            _step_6 - Супермаркеты
            _step_7 - Аптеки
            _step_8 - Ночная жизнь
            _step_9 - Спортзалы
            """
            favorite_place_data = ast.literal_eval(get_or_create_step(search=search, step_pos=2).answer)
            favorite_lat = favorite_place_data[0]
            favorite_lng = favorite_place_data[1]
            favorite_type_pk = favorite_place_data[2]
            favorite_minutes = favorite_place_data[3]
            favorite_type = TravelType.objects.get(pk=int(favorite_type_pk)).tomtom_type
            range_data = maps.get_range(favorite_lat, favorite_lng, favorite_type, favorite_minutes)
            logger.info(range_data)
            range_data = range_data.get('reachableRange').get('boundary')
            logger.info(range_data)
            prepared_polygon = []
            for point_bound in range_data:
                prepared_polygon.append((point_bound.get('latitude'), point_bound.get('longitude')))
            polygon = Polygon(prepared_polygon)
            realty_objects = realty_objects.filter(pk__in=step_10.result)
            realty_objects_pk = []
            for realty_object in realty_objects:
                if polygon.contains(Point(float(realty_object.realty_complex.lat),
                                          float(realty_object.realty_complex.lng))):
                    realty_objects_pk.append(realty_object.pk)
            realty_objects = RealtyObject.objects.filter(pk__in=realty_objects_pk)
            _school_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 5).answer))
            _park_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 6).answer))
            _pharmacy_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 8).answer))
            _night_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 9).answer))
            _market_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 7).answer))
            _gym_distance = DistanceChoose.objects.get(pk=int(get_or_create_step(search, 10).answer))
            _school_percent_list = dict()
            _park_percent_list = dict()
            _pharmacy_percent_list = dict()
            _nightclub_percent_list = dict()
            _market_percent_list = dict()
            _gym_percent_list = dict()
            for realty_object in realty_objects:
                try:
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
                    logger.warning(
                        'Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                  realty_object.realty_complex.tom_school_dist, e))
                    _gym_json = {realty_object.pk: 0}
                    _gym_percent_list.update(_gym_json)
                    ##

                try:
                    if _pharmacy_distance.distance == 0:
                        _percent = 100
                    elif _pharmacy_distance.distance > 0:
                        _distance = realty_object.realty_complex.tom_pharmacy_dist.distance
                        if _pharmacy_distance.distance > _distance:
                            _percent = 100
                        else:
                            _percent = 100 - (_distance - _pharmacy_distance.distance) / \
                                       _pharmacy_distance.distance * 100
                            if _percent < 0:
                                _percent = 0
                    else:
                        _distance = realty_object.realty_complex.tom_pharmacy_dist.distance
                        if -_pharmacy_distance.distance < _distance:
                            _percent = 100
                        else:
                            _percent = 100 - (- _pharmacy_distance.distance - _distance) / \
                                       - _pharmacy_distance.distance * 100
                            if _percent < 0:
                                _percent = 0
                    _pharmacy_json = {realty_object.pk: _percent}
                    _pharmacy_percent_list.update(_pharmacy_json)
                except AttributeError as e:
                    logger.warning(
                        'Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                  realty_object.realty_complex.tom_pharmacy_dist, e))
                    _pharmacy_json = {realty_object.pk: 0}
                    _pharmacy_percent_list.update(_pharmacy_json)

                    ##

                try:
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
                    logger.warning(
                        'Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                  realty_object.realty_complex.tom_nightclub_dist, e))
                    _nightclub_json = {realty_object.pk: 0}
                    _nightclub_percent_list.update(_nightclub_json)

                    ##

                try:
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
                            _percent = 100 - \
                                       (- _market_distance.distance - _distance) / - _market_distance.distance * 100
                            if _percent < 0:
                                _percent = 0
                    _market_json = {realty_object.pk: _percent}
                    _market_percent_list.update(_market_json)
                except AttributeError as e:
                    logger.warning(
                        'Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                  realty_object.realty_complex.tom_market_dist, e))
                    _market_json = {realty_object.pk: 0}
                    _market_percent_list.update(_market_json)

                try:
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
                    logger.warning(
                        'Problem for complex {}\n\n{}\n{}'.format(realty_object,
                                                                  realty_object.realty_complex.tom_park_dist, e))
                    _park_json = {realty_object.pk: 0}
                    _park_percent_list.update(_park_json)

            _final_list = []
            for realty_object in realty_objects:
                try:
                    _object_json = {
                        "object_id": realty_object.pk,
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
                        }, }
                    _final_list.append(_object_json)
                except Exception as e:
                    logger.warning('Some shit happens \n{}'.format(e))

            def extract_score(json):
                try:
                    return int(json['scoring']['total'])
                except KeyError:
                    return 0

            _final_list.sort(key=extract_score, reverse=True)
            _short_list = _final_list[:10]
            for i in _short_list:
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
            search.result = json.dumps(_short_list)
            search.save()
            search.result_full = json.dumps(_final_list)
            search.save()
            prepare_final_json.apply_async(args=[search.pk])
            resp_data = {"step": 11,
                         "template": "step_final",
                         "search_id": search.hashed_id,
                         "count": realty_objects.count()}
            return Response(data=resp_data, status=200)
        else:
            return Response(request.data)
