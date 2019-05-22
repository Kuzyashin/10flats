import ast
import json
import os
import logging

from .tasks import prepare_final_json, prepare_final_json_v2

from django.db.models import Max, Min
from django.utils import timezone
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from core.utils import TomTom
from core.models import DistanceMatrix
from properites.models import Area
from properites.serializers import AreaSerializer
from realty.models import RealtyObject
from realty.serializers import RealtyObjectShortSerializer
from .models import DistanceChoose, RequestViewing
from .models import Search, PercentPass, SearchV2, SearchV2step
from .serializers import DistanceChooseSerializer
from core.serializers import TomTomDistanceMatrixSerializer

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


class SearchGetViewSet(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, search_hashed):
        search = get_object_or_404(Search, hashed_id=search_hashed)
        resp_data = {
            "result": json.loads(search.result),
            "search_id": search.hashed_id,
            "search_start": search.created_at,
            "search_finish": search.finished_at
        }
        return Response(data=resp_data, status=200)

    def post(self, request, search_hashed):
        search = get_object_or_404(Search, hashed_id=search_hashed)
        resp_data = {
            "result": json.loads(search.result),
            "search_id": search.hashed_id,
            "search_start": search.created_at,
            "search_finish": search.finished_at
        }
        return Response(data=resp_data, status=200)


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


class SearchViewSet(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
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

    def post(self, request, format=None):
        data = request.data
        user_id = data.get('user_id')
        if data.get('step') == '0' or data.get('step') == 0:
            search = Search.objects.create(
                user_identify=user_id,
                created_at=timezone.now(),
                last_step=1,
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
            search = Search.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            try:
                areas_pk = ast.literal_eval(data.get('data'))
            except ValueError:
                areas_pk = data.get('data')
            search.step_1 = areas_pk
            search.last_step = 2
            search.save()
            realty_objects = RealtyObject.objects.filter(realty_complex__area_id__in=areas_pk)
            count = realty_objects.count()
            room_list = realty_objects.distinct('rooms_count').values('rooms_count')
            resp_data = {"step": 2,
                         "template": "step_2",
                         "answers": room_list,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '2' or data.get('step') == 2:
            search = Search.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            try:
                rooms_count = ast.literal_eval(data.get('data'))
            except ValueError:
                rooms_count = data.get('data')
            search.step_2 = rooms_count
            search.last_step = 3
            search.save()
            min_room = search.step_2[0]
            max_room = search.step_2[1]
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__range=(min_room, max_room))
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__range=(min_room, max_room))
            count = realty_objects.count()
            min_price = realty_objects.aggregate(Min('rent_price_eur'))
            max_price = realty_objects.aggregate(Max('rent_price_eur'))
            resp_data = {"step": 3,
                         "template": "step_3",
                         "answers": {"min_price": min_price, "max_price": max_price},
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '3' or data.get('step') == 3:
            search = Search.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            try:
                min_max_price = ast.literal_eval(data.get('data'))
            except ValueError:
                min_max_price = data.get('data')
            search.step_3 = min_max_price
            search.last_step = 4
            search.save()
            min_room = ast.literal_eval(search.step_2)[0]
            max_room = ast.literal_eval(search.step_2)[1]
            min_price = search.step_3[0]
            max_price = search.step_3[1]
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__range=(min_room, max_room),
                    rent_price_eur__range=(min_price, max_price)
                )
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__range=(min_room, max_room),
                    rent_price_eur__range=(min_price, max_price)
                )
            count = realty_objects.count()
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 4,
                         "template": "step_4",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '4' or data.get('step') == 4:
            search = Search.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            search.step_4 = data.get('data')[0]
            search.last_step = 5
            search.save()
            min_room = ast.literal_eval(search.step_2)[0]
            max_room = ast.literal_eval(search.step_2)[1]
            min_price = ast.literal_eval(search.step_3)[0]
            max_price = ast.literal_eval(search.step_3)[1]
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__range=(min_room, max_room),
                    rent_price_eur__range=(min_price, max_price)
                )
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__range=(min_room, max_room),
                    rent_price_eur__range=(min_price, max_price)
                )
            _school_distance = DistanceChoose.objects.get(pk=int(search.step_4))
            percent = PercentPass.objects.last().percent
            search.step_4_data = [r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.school_dist is not None
                        and r_obj.realty_complex.school_dist <= _school_distance.distance / percent * 100]
            search.save()
            realty_objects = realty_objects.filter(pk__in=search.step_4_data)
            count = realty_objects.count()
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 5,
                         "template": "step_5",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '5' or data.get('step') == 5:
            search = Search.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            search.step_5 = data.get('data')[0]
            search.last_step = 6
            search.save()
            realty_objects = RealtyObject.objects.filter(pk__in=ast.literal_eval(search.step_4_data))
            _park_distance = DistanceChoose.objects.get(pk=int(search.step_5))
            percent = PercentPass.objects.last().percent
            search.step_5_data = [r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.park_dist is not None
                        and r_obj.realty_complex.park_dist <= _park_distance.distance / percent * 100]
            search.save()
            realty_objects = realty_objects.filter(pk__in=search.step_5_data)
            count = realty_objects.count()
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 6,
                         "template": "step_6",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '6' or data.get('step') == 6:
            search = Search.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            search.step_6 = data.get('data')[0]
            search.last_step = 7
            search.save()
            realty_objects = RealtyObject.objects.filter(pk__in=ast.literal_eval(search.step_5_data))
            _market_distance = DistanceChoose.objects.get(pk=int(search.step_6))
            percent = PercentPass.objects.last().percent
            search.step_6_data = [r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.market_dist is not None
                        and r_obj.realty_complex.market_dist <= _market_distance.distance / percent * 100]
            search.save()
            realty_objects = realty_objects.filter(pk__in=search.step_6_data)
            count = realty_objects.count()
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 7,
                         "template": "step_7",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '7' or data.get('step') == 7:
            search = Search.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            search.step_7 = data.get('data')[0]
            search.last_step = 8
            search.save()
            realty_objects = RealtyObject.objects.filter(pk__in=ast.literal_eval(search.step_6_data))
            _pharmacy_distance = DistanceChoose.objects.get(pk=int(search.step_7))
            percent = PercentPass.objects.last().percent
            search.step_7_data = [r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.pharmacy_dist is not None
                        and r_obj.realty_complex.pharmacy_dist <= _pharmacy_distance.distance / percent * 100]
            search.save()
            realty_objects = realty_objects.filter(pk__in=search.step_7_data)
            count = realty_objects.count()
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 8,
                         "template": "step_8",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '8' or data.get('step') == 8:
            search = Search.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            search.step_8 = data.get('data')[0]
            search.last_step = 9
            search.save()
            realty_objects = RealtyObject.objects.filter(pk__in=ast.literal_eval(search.step_7_data))
            _night_distance = DistanceChoose.objects.get(pk=int(search.step_8))
            percent = PercentPass.objects.last().percent
            search.step_8_data = [r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.nightclub_dist is not None
                        and r_obj.realty_complex.nightclub_dist <= _night_distance.distance / percent * 100]
            search.save()
            realty_objects = realty_objects.filter(pk__in=search.step_8_data)
            count = realty_objects.count()
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 9,
                         "template": "step_9",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '9' or data.get('step') == 9:
            search = Search.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            search.step_9 = data.get('data')[0]
            search.last_step = 10
            search.finished_at = timezone.now()
            search.save()
            realty_objects = RealtyObject.objects.filter(pk__in=ast.literal_eval(search.step_8_data))
            _gym_distance = DistanceChoose.objects.get(pk=int(search.step_9))
            percent = PercentPass.objects.last().percent
            search.step_9_data = [r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.gym_dist is not None
                        and r_obj.realty_complex.gym_dist <= _gym_distance.distance / percent * 100]
            search.save()
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
            realty_objects = realty_objects.filter(pk__in=search.step_9_data)
            _school_distance = DistanceChoose.objects.get(pk=int(search.step_4))
            _park_distance = DistanceChoose.objects.get(pk=int(search.step_5))
            _pharmacy_distance = DistanceChoose.objects.get(pk=int(search.step_7))
            _night_distance = DistanceChoose.objects.get(pk=int(search.step_8))
            _market_distance = DistanceChoose.objects.get(pk=int(search.step_6))
            _gym_distance = DistanceChoose.objects.get(pk=int(search.step_9))
            _school_percent_list = dict()
            _park_percent_list = dict()
            _pharmacy_percent_list = dict()
            _nightclub_percent_list = dict()
            _market_percent_list = dict()
            _gym_percent_list = dict()

            for realty_object in realty_objects:
                try:
                    _distance = realty_object.realty_complex.gym_dist
                    if _gym_distance.distance > _distance:
                        _percent = 100
                    else:
                        _percent = 100 - (_distance - _gym_distance.distance) / _gym_distance.distance * 100
                        if _percent < 0:
                            _percent = 0
                    _gym_json = {realty_object.pk: _percent}
                    _gym_percent_list.update(_gym_json)
                except DistanceMatrix.DoesNotExist:
                    _gym_json = {realty_object.pk: 0}
                    _gym_percent_list.update(_gym_json)
                try:
                    _distance = realty_object.realty_complex.school_dist
                    if _school_distance.distance > _distance:
                        _percent = 100
                    else:
                        _percent = 100 - (_distance - _school_distance.distance) / _school_distance.distance * 100
                        if _percent < 0:
                            _percent = 0
                    _school_json = {realty_object.pk: _percent}
                    _school_percent_list.update(_school_json)
                except DistanceMatrix.DoesNotExist:
                    _school_json = {realty_object.pk: 0}
                    _school_percent_list.update(_school_json)
                try:
                    _distance = realty_object.realty_complex.park_dist
                    if _park_distance.distance > _distance:
                        _percent = 100
                    else:
                        _percent = 100 - (_distance - _park_distance.distance) / _park_distance.distance * 100
                        if _percent < 0:
                            _percent = 0
                    _park_json = {realty_object.pk: _percent}
                    _park_percent_list.update(_park_json)
                except DistanceMatrix.DoesNotExist:
                    _park_json = {realty_object.pk: 0}
                    _park_percent_list.update(_park_json)
                    ##
                try:
                    _distance = realty_object.realty_complex.pharmacy_dist
                    if _pharmacy_distance.distance > _distance:
                        _percent = 100
                    else:
                        _percent = 100 - (_distance - _pharmacy_distance.distance) / _pharmacy_distance.distance * 100
                        if _percent < 0:
                            _percent = 0
                    _pharmacy_json = {realty_object.pk: _percent}
                    _pharmacy_percent_list.update(_pharmacy_json)
                except DistanceMatrix.DoesNotExist:
                    _pharmacy_json = {realty_object.pk: 0}
                    _pharmacy_percent_list.update(_pharmacy_json)
                    ##
                try:
                    _distance = realty_object.realty_complex.nightclub_dist
                    if _night_distance.distance > _distance:
                        _percent = 100
                    else:
                        _percent = 100 - (_distance - _night_distance.distance) / _night_distance.distance * 100
                        if _percent < 0:
                            _percent = 0
                    _nightclub_json = {realty_object.pk: _percent}
                    _nightclub_percent_list.update(_nightclub_json)
                except DistanceMatrix.DoesNotExist:
                    _nightclub_json = {realty_object.pk: 0}
                    _nightclub_percent_list.update(_nightclub_json)
                    ##
                try:
                    _distance = realty_object.realty_complex.market_dist
                    if _market_distance.distance > _distance:
                        _percent = 100
                    else:
                        _percent = 100 - (_distance - _market_distance.distance) / _market_distance.distance * 100
                        if _percent < 0:
                            _percent = 0
                    _market_json = {realty_object.pk: _percent}
                    _market_percent_list.update(_market_json)
                except DistanceMatrix.DoesNotExist:
                    _market_json = {realty_object.pk: 0}
                    _market_percent_list.update(_market_json)
            _school_percent_list = _school_percent_list
            _park_percent_list = _park_percent_list
            _pharmacy_percent_list = _pharmacy_percent_list
            _nightclub_percent_list = _nightclub_percent_list
            _market_percent_list = _market_percent_list
            _gym_percent_list = _gym_percent_list
            _final_list = []

            for realty_object in realty_objects:
                _object_json = {
                        "scoring": {
                            "gym": int(_gym_percent_list.get(realty_object.pk)),
                            "school": int(_school_percent_list.get(realty_object.pk)),
                            "park": int(_park_percent_list.get(realty_object.pk)),
                            "pharmacy": int(_pharmacy_percent_list.get(realty_object.pk)),
                            "nightclub": int(_nightclub_percent_list.get(realty_object.pk)),
                            "market": int(_market_percent_list.get(realty_object.pk)),
                            "total": (int(_school_percent_list.get(realty_object.pk)) +
                                      int(_park_percent_list.get(realty_object.pk)) +
                                      int(_pharmacy_percent_list.get(realty_object.pk)) +
                                      int(_nightclub_percent_list.get(realty_object.pk)) +
                                      int(_gym_percent_list.get(realty_object.pk)) +
                                      int(_market_percent_list.get(realty_object.pk))) / 6
                        },
                        "info": RealtyObjectShortSerializer(realty_object).data
                }
                _final_list.append(_object_json)

            def extract_score(json):
                try:
                    return int(json['scoring']['total'])
                except KeyError:
                    return 0

            _final_list.sort(key=extract_score, reverse=True)
            search.result = json.dumps(_final_list)
            search.save()
            resp_data = {"step": 10,
                         "template": "step_final",
                         "search_id": search.pk,
                         "count": len(_final_list)}
            return Response(data=resp_data, status=200)
        else:
            return Response(request.data)


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
    _step_2 - Выбор кол-ва комнат
    _step_3 - Выбор мин/макс суммы
    _step_4 - Школы
    _step_5 - парки
    _step_6 - Супермаркеты
    _step_7 - Аптеки
    _step_8 - Ночная жизнь
    _step_9 - Спортзалы
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
            realty_objects = RealtyObject.objects.filter(realty_complex__area_id__in=areas_pk)
            count = realty_objects.count()
            step_1 = get_or_create_step(search=search, step_pos=1)
            step_1.answer = areas_pk
            step_1.result = [realty_object.pk for realty_object in realty_objects]
            step_1.save()
            room_list = realty_objects.distinct('rooms_count').values('rooms_count')
            resp_data = {"step": 2,
                         "template": "step_2",
                         "answers": room_list,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '2' or data.get('step') == 2:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            try:
                rooms_count = ast.literal_eval(data.get('data'))
            except ValueError:
                rooms_count = data.get('data')
            search.last_step = 3
            search.save()
            min_room = rooms_count[0]
            max_room = rooms_count[1]
            step_2 = get_or_create_step(search=search, step_pos=2)
            step_2.answer = rooms_count
            step_2.created_at = timezone.now()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=1).result),
                rooms_count__range=(min_room, max_room))
            step_2.result = [realty_object.pk for realty_object in realty_objects]
            step_2.save()
            count = realty_objects.count()
            min_price = realty_objects.aggregate(Min('rent_price_eur'))
            max_price = realty_objects.aggregate(Max('rent_price_eur'))
            resp_data = {"step": 3,
                         "template": "step_3",
                         "answers": {"min_price": min_price, "max_price": max_price},
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '3' or data.get('step') == 3:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            try:
                min_max_price = ast.literal_eval(data.get('data'))
            except ValueError:
                min_max_price = data.get('data')
            search.last_step = 4
            search.save()
            step_3 = get_or_create_step(search=search, step_pos=3)
            min_price = min_max_price[0]
            max_price = min_max_price[1]
            step_3.answer = min_max_price
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=2).result),
                rent_price_eur__range=(min_price, max_price)
            )
            step_3.result = [realty_object.pk for realty_object in realty_objects]
            step_3.save()
            count = realty_objects.count()
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all(), many=True)
            resp_data = {"step": 4,
                         "template": "step_4",
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '4' or data.get('step') == 4:
            search = SearchV2.objects.filter(
                user_identify=user_id,
                finished_at__isnull=True
            ).last()
            step_4 = get_or_create_step(search=search, step_pos=4)
            step_4.answer = data.get('data')[0]
            search.last_step = 5
            search.save()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=3).result),
            )
            _school_distance = DistanceChoose.objects.get(pk=int(step_4.answer))
            percent = PercentPass.objects.last().percent
            if _school_distance.distance > 0:
                step_4.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_school__distance__lte=_school_distance.distance / percent * 100)]
            elif _school_distance.distance < 0:
                step_4.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_school__distance__gte=(
                                 -_school_distance.distance) / percent * 100)]
            else:
                step_4.result = ast.literal_eval(get_or_create_step(search=search, step_pos=3).result)
            step_4.save()
            count = len(step_4.result)
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
            step_5.save()
            search.last_step = 6
            search.save()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=4).result),
            )
            _park_distance = DistanceChoose.objects.get(pk=int(step_5.answer))
            percent = PercentPass.objects.last().percent
            if _park_distance.distance > 0:
                step_5.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_park__distance__lte=
                                                       _park_distance.distance / percent * 100)]
            elif _park_distance.distance < 0:
                step_5.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_park__distance__lte=(
                                 -_park_distance.distance) / percent * 100)]
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
            search.last_step = 7
            search.save()
            realty_objects = RealtyObject.objects.filter(
                pk__in=ast.literal_eval(get_or_create_step(search=search, step_pos=5).result),
            )
            _market_distance = DistanceChoose.objects.get(pk=int(step_6.answer))
            percent = PercentPass.objects.last().percent
            if _market_distance.distance > 0:
                step_6.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_market__distance__lte=
                                                       _market_distance.distance / percent * 100)]
            elif _market_distance.distance < 0:
                step_6.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_market__distance__lte=(
                                 -_market_distance.distance) / percent * 100)]
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
            _pharmacy_distance = DistanceChoose.objects.get(pk=int(step_7.answer))
            percent = PercentPass.objects.last().percent
            if _pharmacy_distance.distance > 0:
                step_7.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_pharmacy__distance__lte=
                                                       _pharmacy_distance.distance / percent * 100)]
            elif _pharmacy_distance.distance < 0:
                step_7.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_pharmacy__distance__lte=(
                                 -_pharmacy_distance.distance) / percent * 100)]
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
            _night_distance = DistanceChoose.objects.get(pk=int(step_8.answer))
            percent = PercentPass.objects.last().percent
            if _night_distance.distance > 0:
                step_8.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_nightclub__distance__lte=
                                                       _night_distance.distance / percent * 100)]
            elif _night_distance.distance < 0:
                step_8.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_nightclub__distance__lte=(
                                 -_night_distance.distance) / percent * 100)]
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
            _gym_distance = DistanceChoose.objects.get(pk=int(step_9.answer))
            percent = PercentPass.objects.last().percent
            if _gym_distance.distance > 0:
                step_9.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_gym__distance__lte=
                                                       _gym_distance.distance / percent * 100)]
            elif _gym_distance.distance < 0:
                step_9.result = [r_obj.pk for r_obj in
                                 realty_objects.filter(realty_complex__nearest_gym__distance__lte=(
                                 -_gym_distance.distance) / percent * 100)]
            else:
                step_9.result = ast.literal_eval(get_or_create_step(search=search, step_pos=8).result)
            step_9.save()
            prepare_final_json_v2.apply_async(args=[search.pk])
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
            
            realty_objects = realty_objects.filter(pk__in=step_9.result)
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
"""
            resp_data = {"step": 10,
                         "template": "step_final",
                         "search_id": search.hashed_id,
                         "count": realty_objects.count()}
            return Response(data=resp_data, status=200)
        else:
            return Response(request.data)
