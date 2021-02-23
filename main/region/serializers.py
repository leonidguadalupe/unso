from flask_restful import fields


region_schema = {
    'slug': fields.String,
    'parent_slug': fields.String,
    'name': fields.String
}


port_schema = {
    'name': fields.String,
    'parent_slug': fields.String,
    'code': fields.String
}
