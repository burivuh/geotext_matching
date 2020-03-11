from django.db import models


class Iteration(models.Model):
    """
    A table for iterations of markup. Used to logically separate marked objects.
    """
    create_dt = models.DateTimeField(auto_now_add=True)
    meta = models.TextField()


class MarkedObjects(models.Model):
    """
    A table of marked object pairs.
    Obj_X stands for object (OSM POI) matching to a given group of objects on the map.
    Other_X stands for a group member (Booking hotel) compared to the given object.
    """
    obj_id = models.IntegerField()
    obj_type = models.CharField(max_length=10)
    obj_lat = models.FloatField()
    obj_lon = models.FloatField()
    obj_meta = models.TextField(blank=True, null=True)
    other_id = models.IntegerField()
    other_lat = models.FloatField()
    other_lon = models.FloatField()
    other_meta = models.TextField(blank=True, null=True)
    mark = models.IntegerField()  # In hotels case: 0 - no match, 1 - match, 2 - merge
    iteration = models.ForeignKey(on_delete=models.CASCADE, to=Iteration)
