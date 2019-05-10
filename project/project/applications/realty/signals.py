from django.db.models.signals import post_save
from django.dispatch import receiver
import re
import requests
from .models import RealtyComplex
from .tasks import new_complex


@receiver(post_save, sender=RealtyComplex)
def save_lat_lng(sender, instance, created, **kwargs):
    if instance.google_maps_url:
        if not instance.lat and not instance.lng:
            try:
                data = re.search(r'(\d+\.\d+)!4d(\d+\.\d+)', requests.get(instance.google_maps_url).url)
                instance.lat = data.group(1)
                instance.lng = data.group(2)
                instance.save()
            except Exception as e:
                print(e)
        if created:
            new_complex().apply_async(kwargs={'complex_pk': instance.pk})

