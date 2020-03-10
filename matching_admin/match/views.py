import json
import random

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View, TemplateView

from matching_admin import settings
from .models import Iteration, MarkedObjects


class IndexView(TemplateView):
    template_name = 'index.html'


class RandomRowView(View):
    def get(self, *args, **kwargs):
        iteration = Iteration.objects.all().order_by('-id')[0]
        while True:
            lineno = random.randint(1, len(settings.dataset))
            row = settings.dataset[lineno: lineno + 1].to_dict(orient='records')[0]
            if float(row['dist_1']) > 0.02:  # ~3km
                continue
            obj_exists = MarkedObjects.objects.filter(
                iteration=iteration,
                obj_id=row['id'],
                obj_type=row['type']
            ).exists()
            if not obj_exists:
                break
        row['obj_lat'], row['obj_lon'] = map(
            float,
            row.pop('geometry').replace('POINT (', '').replace(')', '').split()
        )  # "POINT (43.70663164823837 10.4331211631345)"
        row['obj_id'] = row.pop('type') + '/' + str(row.pop('id'))
        row['obj_name'] = row.pop('name')
        row['others'] = []
        i = 1
        while True:
            other_obj = {}
            try:
                for k in ('other_id', 'other_lat', 'other_lon', 'other_name', 'dist'):
                    other_obj['num'] = i
                    other_obj[k] = row.pop(k + '_' + str(i))
            except KeyError:
                break
            row['others'].append(other_obj)
            i += 1
        return JsonResponse(data=row, safe=False)


class MarkedObjectsView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        data['iteration'] = Iteration.objects.all().order_by('-id')[0]
        MarkedObjects(**data).save()
        return JsonResponse(data={'ok': 'ok'})
