import telebot
from config import currency, TOKEN
from extensions import APIException, CryptoHandler

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start_message(message: telebot.types.Message):
    text = "Добро пожаловать в бот для перевода валют. Здесь вы можете перевести валюты. " \
           "Для перевода одной валюты в другую необходимо: " \
           "ввести имя первой валюты - поставить пробел, " \
           "ввести имя второй валюты - поставить пробел, " \
           "ввести количество валюты цифрами. " \
           "Доступные валюты по команде /values"

    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def currency_func(message: telebot.types.Message):
    text = "Доступные валюты: "
    for i in currency.keys():
        text = "\n".join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def handler(message: telebot.types.Message):
    try:
        list_currency = message.text.split(" ")

        if len(list_currency) != 3:
            raise APIException("Введите 3 аргумента "
                               "(для помощи нажмите /help)")

        base, quote, amount = list_currency
        text = CryptoHandler.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n {e}. "
                              f"(для помощи нажмите /help)")
    else:
        final_message = f"ЦЕНА {amount} {currency[base]} в {currency[quote]} состовляет:\n {text}. "
        bot.reply_to(message, final_message)


bot.polling()
