import requests
import json
from config import currency


class APIException(Exception):
    pass


class CryptoHandler:
    def get_price(base=str, quote=str, amount=str):
        if base == quote:
            raise APIException(
                f"Невозможно перевести одинаковые валюты. {currency[base]} в {currency[quote]}."
                f" (для помощи нажмите /help)")
        try:
            first = currency[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту '{base}'. "
                               f"(для помощи нажмите /help)")

        try:
            second = currency[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту '{quote}'. "
                               f"(для помощи нажмите /help)")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Введите колличество валюты ввиде цифр. (для помощи нажмите /help)")

        request = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={first}&tsyms={second}")
        text = float(amount) * json.loads(request.content)[currency[quote]]

        return text
