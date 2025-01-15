import requests
import json

class APIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Converter:
    @staticmethod
    def get_price(base, quote, amount):

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Неверное количество валюты")

        url = f"https://api.exchangerate-api.com/v4/latest/{quote}" # Поменяли местами base и quote
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = json.loads(response.text)
            rates = data['rates']
            result = rates.get(base) # Поменяли местами base и quote


            if result is None:
              raise APIException(f"Не удалось получить курс валют")


            converted_amount = amount * result # Поменяли знак
            return converted_amount
        except requests.exceptions.RequestException as e:
            raise APIException(f"Ошибка API: Не удалось получить данные: {e}")
        except json.JSONDecodeError as e:
            raise APIException(f"Ошибка API: Неверный формат ответа: {e}")
        except KeyError as e:
            raise APIException(f"Ошибка API: Неверный формат ответа: {e}")