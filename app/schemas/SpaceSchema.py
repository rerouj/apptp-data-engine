from marshmallow import Schema, fields, post_load
from classes import Space as Sp


class SpaceSchema(Schema):

    class Meta:
        ordered = True

    _id = fields.Str()
    show = fields.Str(required=True)
    show_title = fields.Str(required=True)
    space = fields.List(fields.Dict(required=True))
    locality_space = fields.List(fields.Dict())
    region_space = fields.List(fields.Dict())
    country_space = fields.List(fields.Dict())
    locations_name = fields.List(fields.Str())
    distance = fields.Dict()

    @post_load
    def make_space(self, data, **kwargs):
        return Sp.Space(**data)
