import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате:\
\n<имя валюты, цену которой надо узнать> \
\n<имя валюты, в которой нужно узнать цену первой валюты> \
\n <количество первой валюты> \
\n <Список доступных валют: /values>'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for kye in keys.keys():
        text = '\n'.join((text,kye, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Ошибка: Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Возникла ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Простите, команда не обрабатывается\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()

if __name__ == "__main__":
    app()