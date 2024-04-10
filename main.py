import telebot
from config import TOKEN
from pars_data import get_headers
from recording_data import write_data

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_support = telebot.types.KeyboardButton(text="Ввести URL")
    keyboard.add(button_support)
    bot.send_message(chat_id,
                     'Добро пожаловать в бота сбора обратной связи',
                     reply_markup=keyboard,
                     )


@bot.message_handler(func=lambda message: message.text == 'Ввести URL')
def write_to_support(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Введите URL')
    bot.register_next_step_handler(message, save_url)


def save_url(message):
    chat_id = message.chat.id
    url = message.text
    message_to_user = 'Заголовки новостей добавлены в таблицу'
    bot.send_message(chat_id, f'Отлично, начался процес сбора заголовков')
    try:
        headers_list = get_headers(url)
        write_data([headers_list])
        bot.register_next_step_handler(message, save_url)
        bot.send_message(chat_id, message_to_user)
    except Exception as e:
        message_to_user = f'Ошибка - {e}'
        bot.register_next_step_handler(message, save_url)
        bot.send_message(chat_id, message_to_user)


def answer_to_user(message, answer):
    chat_id = message.chat.id
    bot.send_message(chat_id, answer)


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
