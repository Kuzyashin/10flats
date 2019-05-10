from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Result
from .utils.typeform import parse_typeform_answers


import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Result)
def on_new_typeform(sender, instance, **kwargs):
    if kwargs['created']:
        parse_typeform_answers(instance)


