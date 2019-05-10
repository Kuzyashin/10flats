from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseForbidden
from messenegers.telegram.handlers import parse_message
import os


# Create your views here.
class TelegramBotView(View):
    def post(self, request, bot_token):
        if bot_token != os.environ['TG_BOT_TOKEN']:
            return HttpResponseForbidden('Invalid token')
        else:
            parse_message(request)
            return HttpResponse(200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TelegramBotView, self).dispatch(request, *args, **kwargs)


class FacebookBotView(View):
    def post(self, request, bot_token):
        pass


class LineBotView(View):
    def post(self, request, bot_token):
        pass
