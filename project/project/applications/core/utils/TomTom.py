import requests
import logging
import json
import time

logger = logging.getLogger(__name__)

class TomTom:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.tomtom.com'
        self.default_format = 'json'
        self.default_limit = '100'
        self.default_radius = '3000'

        if not self.token:
            raise ValueError('Provide Token!')

    def get_categories(self):
        url = self.base_url + '/search/2/poiCategories.' + self.default_format + '?key=' + self.token
        data = requests.get(url)
        try:
            return data.json()
        except Exception as e:
            time.sleep(1)
            logger.warning(e)
            logger.warning(data)
            try:
                return json.loads(data)
            except Exception as e:
                logger.warning(e)
                time.sleep(3)
                return requests.get(url).json()

    def get_nearby(self, lat, lng, category, offset):
        url = self.base_url + '/search/2/nearbySearch/.' + self.default_format + '?lat={}&lon={}'.format(lat, lng) + \
            '&limit=' + self.default_limit + '&categorySet=' + category + '&ofs={}'.format(offset) + '&radius=' \
              + self.default_radius + '&idxSet=POI' + '&key=' + self.token
        data = requests.get(url)
        try:
            return data.json()
        except Exception as e:
            time.sleep(1)
            logger.warning(e)
            logger.warning(data)
            try:
                return json.loads(data)
            except Exception as e:
                logger.warning(e)
                time.sleep(3)
                return requests.get(url).json()

    def get_route(self, start_lat, start_lng, fnish_lat, fnish_lng):
        url = self.base_url \
              + '/routing/1/calculateRoute/{},{}:{},{}/'.format(start_lat, start_lng, fnish_lat, fnish_lng) \
              + self.default_format + '?travelMode=pedestrian&key=' + self.token
        data = requests.get(url)
        try:
            return data.json()
        except Exception as e:
            time.sleep(1)
            logger.warning(e)
            logger.warning(data)
            try:
                return json.loads(data)
            except Exception as e:
                logger.warning(e)
                time.sleep(3)
                return requests.get(url).json()
