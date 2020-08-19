from marshmallow import Schema, fields, post_load, pre_load, pre_dump, post_dump
from classes import Location
from bson import ObjectId


class GeodataSchema(Schema):
    latitude = fields.Float()
    longitude = fields.Float()
    type = fields.Str()
    context = fields.List(fields.Str(allow_none=True))
    context_extended = fields.List(fields.Dict())

    @pre_load
    def kill_none(self, data, **kwargs):
        tmp = data['context']
        while data['context'].count(None) >= 1:
            data['context'].remove(None)
        return data

    @post_load
    def add_geodata(self, data, **kwargs):
        return Location.Geodata(**data)


class LocationSchema(Schema):
    _id = fields.Str(required=True)
    archive_name = fields.Str(required=True)
    alias = fields.Str(required=True)
    show_id = fields.List(fields.Dict)
    geodata = fields.Nested(GeodataSchema)
    ggapi_geodata = fields.Dict()

    @post_load
    def add_location(self, data, **kwargs):
        return Location.Location(**data)


class LocationSchemaLite(Schema):
    class Meta:
        ordered = True

    _id = fields.Str(required=True)
    archive_name = fields.Str(required=True)
    alias = fields.Str()
    show_id = fields.List(fields.Dict())
    geo_data = fields.List(fields.Dict())
    wiki_data = fields.Dict()

    @pre_load
    def prepare_date(self, data, **kwargs):
        data['_id'] = str(data['_id'])
        if data['alias'] == '':
            data['alias'] = data['archive_name']
        tmp = [(str(show[0]), show[1]) for show in data['show_id']]
        data['show_id'] = tmp
        return data

    @post_load
    def add_location(self, data, **kwargs):
        return Location.Location(**data)

    @post_dump
    def restore_ids(self, data, **kwargs):
        data['_id'] = ObjectId(data['_id'])
        tmp = [(ObjectId(show[0]), show[1]) for show in data['show_id']]
        data['show_id'] = tmp
        return data
