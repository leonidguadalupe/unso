import os
import requests


class ExchangeRates(object):
    def __init__(self, source=''):
        app_id = os.environ.get('EXCHANGE_RATE_APP_ID', '')
        self.exchange_rates = requests.get(
            'https://openexchangerates.org/api/latest.json?app_id={}'.format(
                app_id
            ))

    def convert_to_usd(self, value, source):
        json_obj = self.exchange_rates.json()
        try:
            source_rate = json_obj['rates'][source.upper()]
        except KeyError:
            raise KeyError('Currency code not found')
        return value/source_rate
