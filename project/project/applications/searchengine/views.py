import ast
import json
# Create your views here.
import logging

from django.db.models import Max, Min
from django.utils import timezone
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response

from core.models import DistanceMatrix
from properites.models import Area
from properites.serializers import AreaSerializer
from realty.models import RealtyObject
from .models import DistanceChoose
from .models import Search, PercentPass
from .serializers import DistanceChooseSerializer

logger = logging.getLogger(__name__)


class SearchViewSet(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    """
    _step_1 - Выбор районов
    _step_2 - Выбор кол-ва комнат
    _step_3 - Выбор мин/макс суммы
    _step_4 - Школы
    _step_5 - Детские парки
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
                last_step=1
            )
            search.save()
            area_list = Area.objects.all()
            serialized = AreaSerializer(area_list, many=True)
            logger.info(serialized.data)
            resp_data = {"step": 1,
                         "template": "step_1",
                         "answers": serialized.data,
                         "count": RealtyObject.objects.all().count()}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '1' or data.get('step') == 1:
            search = Search.objects.filter(
                user_identify=user_id,
                last_step=1
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
                last_step=2
            ).last()
            try:
                rooms_count = ast.literal_eval(data.get('data'))
            except ValueError:
                rooms_count = data.get('data')
            search.step_2 = rooms_count
            search.last_step = 3
            search.save()
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__in=rooms_count
                )
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__in=rooms_count
                )
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
                last_step=3
            ).last()
            min_price = data.get('data').get('min_price')
            max_price = data.get('data').get('max_price')
            search.step_3 = json.dumps({"min_price": min_price, "max_price": max_price})
            search.last_step = 4
            search.save()
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__in=ast.literal_eval(search.step_2),
                    rent_price_eur__gte=min_price,
                    rent_price_eur__lte=max_price
                )
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__in=search.step_2,
                    rent_price_eur__gte=min_price,
                    rent_price_eur__lte=max_price
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
                last_step=4
            ).last()
            search.step_4 = data.get('data')
            search.last_step = 5
            search.save()
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__in=ast.literal_eval(search.step_2),
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__in=search.step_2,
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            _school_distance = DistanceChoose.objects.get(pk=int(search.step_4))
            percent = PercentPass.objects.last().percent
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.school_dist is not None
                        and r_obj.realty_complex.school_dist <= _school_distance.distance / percent * 100])

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
                last_step=5
            ).last()
            search.step_5 = data.get('data')
            search.last_step = 6
            search.save()
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__in=ast.literal_eval(search.step_2),
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__in=search.step_2,
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            _school_distance = DistanceChoose.objects.get(pk=int(search.step_4))
            _park_distance = DistanceChoose.objects.get(pk=int(search.step_5))
            percent = PercentPass.objects.last().percent
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.school_dist is not None
                        and r_obj.realty_complex.school_dist <= _school_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.park_dist is not None
                        and r_obj.realty_complex.park_dist <= _park_distance.distance / percent * 100])
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
                last_step=6
            ).last()
            search.step_6 = data.get('data')
            search.last_step = 7
            search.save()
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__in=ast.literal_eval(search.step_2),
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__in=search.step_2,
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            _school_distance = DistanceChoose.objects.get(pk=int(search.step_4))
            _park_distance = DistanceChoose.objects.get(pk=int(search.step_5))
            _market_distance = DistanceChoose.objects.get(pk=int(search.step_6))
            percent = PercentPass.objects.last().percent
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.school_dist is not None
                        and r_obj.realty_complex.school_dist <= _school_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.park_dist is not None
                        and r_obj.realty_complex.park_dist <= _park_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.market_dist is not None
                        and r_obj.realty_complex.market_dist <= _market_distance.distance / percent * 100])
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
                last_step=7
            ).last()
            search.step_7 = data.get('data')
            search.last_step = 8
            search.save()
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__in=ast.literal_eval(search.step_2),
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__in=search.step_2,
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            _school_distance = DistanceChoose.objects.get(pk=int(search.step_4))
            _park_distance = DistanceChoose.objects.get(pk=int(search.step_5))
            _market_distance = DistanceChoose.objects.get(pk=int(search.step_6))
            _pharmacy_distance = DistanceChoose.objects.get(pk=int(search.step_7))
            percent = PercentPass.objects.last().percent
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.school_dist is not None
                        and r_obj.realty_complex.school_dist <= _school_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.park_dist is not None
                        and r_obj.realty_complex.park_dist <= _park_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.market_dist is not None
                        and r_obj.realty_complex.market_dist <= _market_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.pharmacy_dist is not None
                        and r_obj.realty_complex.pharmacy_dist <= _pharmacy_distance.distance / percent * 100])
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
                last_step=8
            ).last()
            search.step_8 = data.get('data')
            search.last_step = 9
            search.save()
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__in=ast.literal_eval(search.step_2),
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__in=search.step_2,
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            _school_distance = DistanceChoose.objects.get(pk=int(search.step_4))
            _park_distance = DistanceChoose.objects.get(pk=int(search.step_5))
            _market_distance = DistanceChoose.objects.get(pk=int(search.step_6))
            _pharmacy_distance = DistanceChoose.objects.get(pk=int(search.step_7))
            _gym_distance = DistanceChoose.objects.get(pk=int(search.step_8))
            percent = PercentPass.objects.last().percent
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.school_dist is not None
                        and r_obj.realty_complex.school_dist <= _school_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.park_dist is not None
                        and r_obj.realty_complex.park_dist <= _park_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.market_dist is not None
                        and r_obj.realty_complex.market_dist <= _market_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.pharmacy_dist is not None
                        and r_obj.realty_complex.pharmacy_dist <= _pharmacy_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.gym_dist is not None
                        and r_obj.realty_complex.gym_dist <= _gym_distance.distance / percent * 100])
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
                last_step=9
            ).last()
            search.step_9 = data.get('data')
            search.last_step = 10
            search.finished_at = timezone.now()
            search.save()
            try:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=ast.literal_eval(search.step_1),
                    rooms_count__in=ast.literal_eval(search.step_2),
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            except ValueError:
                realty_objects = RealtyObject.objects.filter(
                    realty_complex__area_id__in=search.step_1,
                    rooms_count__in=search.step_2,
                    rent_price_eur__gte=json.loads(search.step_3).get('min_price'),
                    rent_price_eur__lte=json.loads(search.step_3).get('max_price')
                )
            _school_distance = DistanceChoose.objects.get(pk=int(search.step_4))
            _park_distance = DistanceChoose.objects.get(pk=int(search.step_5))
            _market_distance = DistanceChoose.objects.get(pk=int(search.step_6))
            _pharmacy_distance = DistanceChoose.objects.get(pk=int(search.step_7))
            _night_distance = DistanceChoose.objects.get(pk=int(search.step_8))
            _gym_distance = DistanceChoose.objects.get(pk=int(search.step_9))
            percent = PercentPass.objects.last().percent
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.school_dist is not None
                        and r_obj.realty_complex.school_dist <= _school_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.park_dist is not None
                        and r_obj.realty_complex.park_dist <= _park_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.market_dist is not None
                        and r_obj.realty_complex.market_dist <= _market_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.pharmacy_dist is not None
                        and r_obj.realty_complex.pharmacy_dist <= _pharmacy_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.nightclub_dist is not None
                        and r_obj.realty_complex.nightclub_dist <= _night_distance.distance / percent * 100])
            realty_objects = realty_objects.filter(
                pk__in=[r_obj.pk for r_obj in realty_objects
                        if r_obj.realty_complex.gym_dist is not None
                        and r_obj.realty_complex.gym_dist <= _gym_distance.distance / percent * 100])

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
            _final_json = dict()
            for realty_object in realty_objects:
                _object_json = {
                    realty_object.pk: {
                        "gym": _gym_percent_list.get(realty_object.pk),
                        "school": _school_percent_list.get(realty_object.pk),
                        "park": _park_percent_list.get(realty_object.pk),
                        "pharmacy": _pharmacy_percent_list.get(realty_object.pk),
                        "nightclub": _nightclub_percent_list.get(realty_object.pk),
                        "market": _market_percent_list.get(realty_object.pk),
                        "total": (int(_school_percent_list.get(realty_object.pk)) +
                                  int(_park_percent_list.get(realty_object.pk)) +
                                  int(_pharmacy_percent_list.get(realty_object.pk)) +
                                  int(_nightclub_percent_list.get(realty_object.pk)) +
                                  int(_gym_percent_list.get(realty_object.pk)) +
                                  int(_market_percent_list.get(realty_object.pk))) / 6
                    }
                }
                _final_json.update(_object_json)
            return Response(data=_final_json, status=200)
        else:
            return Response(request.data)
