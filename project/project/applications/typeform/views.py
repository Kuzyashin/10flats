from rest_framework import views, permissions
from .serializers import ResultSerializer
from django.utils import timezone
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import logging
import json

# Create your views here.
logger = logging.getLogger(__name__)


class TypeformViewSet(views.APIView):
    permission_classes = (permissions.AllowAny,)
    entity = None

    @csrf_exempt
    def post(self, request):
        try:
            data = request.data

            event_id = data.get('event_id')
            event_type = data.get('event_type')
            form_data = data.get('form_response')

            logger.info(
                "Got new typeform result with:\n"
                "-id: {0}\n-type: {1}\n".format(event_id, event_type)
            )

            hidden = form_data.get('hidden')
            hidden_id = hidden.get('id') if hidden is not None else None
            serializer = ResultSerializer(data={
                'score': int(form_data.get('calculated', {}).get('score', 0)),
                'submitted_at': form_data.get('submitted_at'),
                'created_at': timezone.now(),
                'hidden_id': hidden_id,
                'hidden_data': json.dumps(hidden),
                'content': json.dumps(form_data),
                'name': form_data.get('definition', {}).get('title', '')})
            if serializer.is_valid():
                self.entity = serializer.save()
            else:
                logger.warning('Serializer not valid')
                logger.info(serializer.errors)
        except KeyError as e:
            logger.exception(
                "Error saving typeform result, "
                "we did not found needed data in request: {0}", e)
        except Exception as e:
            logger.exception('Error saving typeform result: {0}', e)
        finally:
            return Response(status=200)
