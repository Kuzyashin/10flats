import json
from django.utils import timezone
from .models import Search
from properites.models import Area
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import viewsets, views, status
from properites.serializers import AreaSerializer
# Create your views here.


class SearchViewSet(viewsets.ViewSet):
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

    _step_1 = {}
    _step_2 = {}
    _step_3 = {}
    _step_4 = {}
    _step_5 = {}
    _step_6 = {}
    _step_7 = {}
    _step_8 = {}
    _step_9 = {}
    """
    def get(self, request, format=None):
        pass

    def post(self, request, format=None):
        data = request.data
        if data.get('step') == 0:
            user_id = data.get('user_id')
            search = Search.objects.create(
                user_identify=user_id,
                created_at=timezone.now(),
                last_step=0
            )
            search.save()
            area_list = Area.objects.all()
            resp_data = {"step": 1,
                         "answers": AreaSerializer(area_list).data}
            print(resp_data)
            return Response(data=resp_data, status=200)
