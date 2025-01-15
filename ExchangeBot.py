import telebot
from config import TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

keys = {
    'доллар': 'USD',
    'евро': 'EUR',
    'юань': 'CNY',
    'тенге': 'KZT',
    'рубль': 'RUB',
    'дирхам': 'AED',
    'сумм': 'UZS',
    'лира': 'TRY'
}

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Привет! Я бот для конвертации валют.\n\nДля использования введите команду в формате:\n'
            '<имя валюты> <в какую валюту перевести> <количество>\n\nСписок доступных валют: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for key in keys:
        text += f"{key} \n"
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException("Неверное количество параметров!")

        quote, base, amount = values
        total_base = keys.get(base.lower())
        total_quote = keys.get(quote.lower())

        if total_base == None or total_quote == None:
            raise APIException(f"Не удалось обработать валюту")

        total = Converter.get_price(total_base, total_quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка: {e}")
    except Exception as e:
        bot.reply_to(message, f"Непредвиденная ошибка: {e}")
    else:
        text = f"Цена {amount} {quote} в {base} : {total:.2f}"
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)