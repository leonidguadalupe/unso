# coding: utf-8

from flask_restful import fields

from ..region.serializers import port_schema


prices_schema = {
    'orig_code': fields.String,
    'dest_code': fields.String,
    'price': fields.Float,
    'day': fields.String
}
