import json
import requests
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str,  amount: str):
        if quote == base:
            raise APIException(f'Ошибка: Нельзя перевести в одинаковую валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise (f'Неудалось обработать валюту: {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise (f'Неудалось обработать валюту: {base}')

        try:
            f_amount = float(amount)
        except ValueError:
            raise (f'Неудалось обработать колличество: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base * f_amount
