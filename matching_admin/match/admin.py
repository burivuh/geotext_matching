import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Iteration, MarkedObjects


def download_data(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/csv")
    response['Content-Disposition'] = 'attachment; filename="dataset.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'obj_type', 'obj_id', 'obj_lat',
        'obj_lon', 'obj_meta', 'other_id',
        'other_lat', 'other_lon', 'other_meta',
        'iteration', 'mark',
    ])
    for obj in queryset:
        writer.writerow([
            obj.obj_type, obj.obj_id, obj.obj_lat,
            obj.obj_lon, obj.obj_meta, obj.other_id,
            obj.other_lat, obj.other_lon, obj.other_meta,
            obj.iteration.pk, obj.mark,
        ])
    return response


download_data.short_description = "Download data"


@admin.register(Iteration)
class IterationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'meta', 'create_dt',)


@admin.register(MarkedObjects)
class MarkedObjectsAdmin(admin.ModelAdmin):
    list_display = (
        'obj_meta', 'obj_type', 'obj_id',
        'other_meta', 'other_id', 'mark',
        'iteration',
    )
    actions = [download_data, ]
    list_filter = ('mark', 'iteration', )
