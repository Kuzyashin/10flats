# -*- coding: utf-8 -*-
# Create your views here.
import logging
import json

from django.views.decorators.http import require_GET
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework import decorators
from .models import ShortUrl, UserData

logger = logging.getLogger(__name__)


class HttpRedirectResponseTgExtended(HttpResponseRedirect):
    allowed_schemes = ['http', 'https', 'ftp', 'tg']
    status_code = 302


@require_GET
def redirect_original(request, short_id):
    try:
        url = ShortUrl.objects.get(short_id=short_id)
        url.count += 1
        url.last_click = timezone.now()
        url.save()
        user_data = UserData(click_time=timezone.now(),
                             user_data=request.META.get('HTTP_USER_AGENT'),
                             user_ip=request.META.get('HTTP_X_REAL_IP'),
                             short_url=url)

        user_data.save()
        logger.info('New URL click: ' + str(short_id))
        return HttpRedirectResponseTgExtended(url.basic_url)
    except ShortUrl.DoesNotExist:
        return HttpRedirectResponseTgExtended('http://taskquiz.com')


@decorators.api_view(['POST'])
@decorators.authentication_classes((TokenAuthentication,))
@decorators.permission_classes((IsAuthenticated,))
def shorten(request):
    data = json.loads(request.body)
    url = data.get('url')

    shortened = ShortUrl()
    shortened.pub_date = timezone.now()
    shortened.basic_url = url
    shortened.save()

    result = {
      'success': True,
      'result': shortened.compile()
    }

    return HttpResponse(json.dumps(result), content_type='application/json')
