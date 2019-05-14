from django.views.generic import View
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseForbidden

# Create your views here.


class SearchView(View):
    _step_1 = {}
    _step_2 = {}
    _step_3 = {}

    def get(self, request):
        pass

    def post(self, request):
        pass
