from celery.task import task
from django.core import management


@task
def get_distances(complex_pk):
    management.call_command('get_distances {}'.format(complex_pk))


@task
def get_places(complex_pk):
    management.call_command('get_google_places {}'.format(complex_pk))


@task
def new_complex(complex_pk):
    management.call_command('get_google_places {}'.format(complex_pk))
    management.call_command('get_distances {}'.format(complex_pk))
