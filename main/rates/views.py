# -*- coding: utf-8 -*-
from datetime import datetime
import simplejson as json

from datetime import timedelta
from flask import Blueprint
from flask_restful import reqparse, marshal_with

from ..extensions import db
from ..exceptions import InvalidTransaction
from ..utils import ExchangeRates
from .models import Price
from .queries import build_prices_query
from .serializers import prices_schema

blueprint = Blueprint('rates', __name__)

# Rates

parser = reqparse.RequestParser()
parser.add_argument('date_from', type=str, location='args')
parser.add_argument('date_to', type=str, location='args')
parser.add_argument('origin', type=str, location='args')
parser.add_argument('destination', type=str, location='args')

parser_for_post = reqparse.RequestParser()
parser_for_post.add_argument('date_from', type=str)
parser_for_post.add_argument('date_to', type=str)
parser_for_post.add_argument('origin', type=str)
parser_for_post.add_argument('destination', type=str)
parser_for_post.add_argument('currency', type=str)
parser_for_post.add_argument('price', type=float)


@blueprint.route('/rates', methods=('GET',))
def get_prices():
    args = parser.parse_args()
    date_from = args.get('date_from', None)
    date_to = args.get('date_to', None)
    origin = args.get('origin', None)
    destination = args.get('destination', None)

    if not date_from or not date_to or not origin or not destination:
        raise InvalidTransaction.missing_kwargs()

    if not date_from.replace('-', '').replace('_', '').isalnum()\
       or not date_to.replace('-', '').replace('_', '').isalnum()\
       or not origin.replace('-', '').replace('_', '').isalnum()\
       or not destination.replace('-', '').replace('_', '').isalnum():
        raise InvalidTransaction.incorrect_input_format()

    a = []
    with db.engine.connect() as con:
        rs = con.execute(build_prices_query(
            origin, destination, date_from, date_to, False))
        for row in rs:
            a.append({
                'day': row[0].isoformat(),
                'average_price': float(row[1]) if row[1] is not None else None
            })

    return json.dumps(a)


@blueprint.route('/rates_null', methods=('GET',))
def get_prices_null():
    args = parser.parse_args()
    date_from = args.get('date_from', None)
    date_to = args.get('date_to', None)
    origin = args.get('origin', None)
    destination = args.get('destination', None)

    if not date_from or not date_to or not origin or not destination:
        raise InvalidTransaction.missing_kwargs()

    if not date_from.replace('-', '').replace('_', '').isalnum()\
       or not date_to.replace('-', '').replace('_', '').isalnum()\
       or not origin.replace('-', '').replace('_', '').isalnum()\
       or not destination.replace('-', '').replace('_', '').isalnum():
        raise InvalidTransaction.incorrect_input_format()

    a = []
    with db.engine.connect() as con:
        rs = con.execute(build_prices_query(
            origin, destination, date_from, date_to, True))
        for row in rs:
            a.append({
                'day': row[0].isoformat(),
                'average_price': float(row[1]) if row[1] is not None else None
            })

    return json.dumps(a)


@blueprint.route('/prices', methods=['POST'])
@marshal_with(prices_schema)
def create_price():
    args = parser_for_post.parse_args()
    date_from = args.get('date_from', None)
    date_to = args.get('date_to', None)
    origin = args.get('origin', None)
    destination = args.get('destination', None)
    price = args.get('price', None)
    currency = args.get('currency', None)
    date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
    date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()

    if not date_from or not date_to or not origin\
       or not destination or not price:
        raise InvalidTransaction.missing_kwargs()

    if currency is not None:
        temp = ExchangeRates()
        price = temp.convert_to_usd(price, currency)

    delta = date_to_obj - date_from_obj
    for i in range(delta.days + 1):
        day = date_from_obj + timedelta(days=i)
        price = Price(
                      orig_code=origin,
                      dest_code=destination,
                      price=price, day=day)
        try:
            price.save()
        except:
            raise InvalidTransaction.input_not_found()

    price.day = str(price.day)
    return price
