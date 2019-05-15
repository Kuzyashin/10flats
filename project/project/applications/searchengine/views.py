import json
from django.utils import timezone
from .models import Search
from properites.models import Area
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import viewsets, views, status
from rest_framework.decorators import api_view
from properites.serializers import AreaSerializer
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
        if data.get('step') == '0':
            user_id = data.get('user_id')
            search = Search.objects.create(
                user_identify=user_id,
                created_at=timezone.now(),
                last_step=0
            )
            search.save()
            area_list = Area.objects.all()
            logger.info(area_list)
            serialized = AreaSerializer(area_list)
            logger.info(serialized)
            logger.info(serialized.data)
            resp_data = {"step": 1,
                         "answers": serialized}
            return Response(data=resp_data, status=200)
        else:
            return Response(request.data)
