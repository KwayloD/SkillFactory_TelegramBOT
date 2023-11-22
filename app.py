import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет! Я Бот-Конвертер валют. Я могу: \n- Показать список доступных валют через команду: ' \
           '/values \n- Вывести конвертацию валюты.\n - Узнать, как конвертировать валюту можно через команду: /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def handler_help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите следующий запрос:\n<Имя валюты, цену которой нужно узнать> \
<Имя валюты в которой надо узнать цену первой валюты> \
<Количество первой валюты>\nУвидеть список доступных валют можно с помощью команды: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def handler_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def handler_convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверные параметры запроса.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
