from schemas.LocationSchema import *


class Location(object):

    """location classes"""

    def __init__(self, _id, archive_name, alias, show_id, geo_data):
        self._id = _id
        self.archive_name = archive_name
        self.alias = alias
        self.show_id = show_id
        self.geo_data = geo_data
        self.wiki_data = {'title': '', 'summary': ''}
        # self.ggapi_geodata = dict()


class Geodata(object):

    """Geodata nested classes"""

    def __init__(self, latitude, longitude, type, context, context_extended):

        self.latitude = latitude
        self.longitude = longitude
        self.type = type
        self.context = context
        self.context_extended = context_extended
