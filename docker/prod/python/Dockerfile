FROM python:3.5
MAINTAINER Alexey Kuzyashin <terr.kuzyashin@gmail.com>

COPY ./project /project

WORKDIR /project
RUN rm pids/celer*

RUN pip install -r requirements.txt


COPY ./docker/prod/python/entrypoint.sh /entrypoint.sh


RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
