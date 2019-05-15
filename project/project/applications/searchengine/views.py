from django.utils import timezone
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import views
from django.db.models import Max, Min
import ast

from .models import Search

from realty.models import RealtyObject
from properites.models import Area
from properites.serializers import AreaSerializer
from .models import DistanceChoose
from .serializers import DistanceChooseSerializer

# Create your views here.
import logging

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
                         "answers": serialized.data,
                         "count": RealtyObject.objects.all().count()}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '1' or data.get('step') == 1:
            search = Search.objects.filter(
                user_identify=user_id,
                last_step=1
            ).last()
            areas_pk = ast.literal_eval(data.get('data'))
            search.step_1 = areas_pk
            search.last_step = 2
            search.save()
            realty_objects = RealtyObject.objects.filter(realty_complex__area_id__in=areas_pk)
            count = realty_objects.count()
            room_list = realty_objects.distinct('rooms_count').values('rooms_count')
            resp_data = {"step": 2,
                         "answers": room_list,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '2' or data.get('step') == 2:
            search = Search.objects.filter(
                user_identify=user_id,
                last_step=2
            ).last()
            rooms_count = ast.literal_eval(data.get('data'))
            search.step_2 = rooms_count
            search.last_step = 3
            search.save()
            realty_objects = RealtyObject.objects.filter(
                realty_complex__area_id__in=ast.literal_eval(search.step_1),
                rooms_count__in=rooms_count
            )
            count = realty_objects.count()
            min_price = realty_objects.aggregate(Min('rent_price_eur'))
            max_price = realty_objects.aggregate(Max('rent_price_eur'))
            resp_data = {"step": 3,
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
            search.step_3 = {"min_price": min_price, "max_price": max_price}
            search.last_step = 4
            search.save()
            realty_objects = RealtyObject.objects.filter(
                realty_complex__area_id__in=ast.literal_eval(search.step_1),
                rooms_count__in=ast.literal_eval(search.step_2),
                rent_price_eur__gte=min_price,
                rent_price_eur__lte=max_price
            )
            count = realty_objects.count()
            choices_list = DistanceChooseSerializer(DistanceChoose.objects.all())
            resp_data = {"step": 4,
                         "answers": choices_list.data,
                         "count": count}
            return Response(data=resp_data, status=200)
        elif data.get('step') == '4' or data.get('step') == 4:
            pass
        elif data.get('step') == '5' or data.get('step') == 5:
            pass
        elif data.get('step') == '6' or data.get('step') == 6:
            pass
        elif data.get('step') == '7' or data.get('step') == 7:
            pass
        elif data.get('step') == '8' or data.get('step') == 8:
            pass
        elif data.get('step') == '9' or data.get('step') == 9:
            pass
        else:
            return Response(request.data)
