import requests


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
        return data.json()

    def get_nearby(self, lat, lng, category, offset):
        url = self.base_url + '/search/2/nearbySearch/.' + self.default_format + '?lat=' + lat + '&lon=' + lng + \
            '&limit=' + self.default_limit + '&categorySet' + str(category) + '&ofs=' + str(offset) + '&radius=' \
              + self.default_radius + '&idxSet=POI' + \
            '&key=' + self.token
        data = requests.get(url)
        return data.json()
