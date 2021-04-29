import telebot
from telebot import types
import config
import sqlighter
import battle
import sqlite3

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    video = open('static/jack.mp4', 'rb')
    bot.send_animation(message.chat.id, video)
    bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}!'
                     f'\nЕсли есть вопросы жми /help')
    sqlighter.new_user(message.from_user.id, message.from_user.first_name)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('С ботом 🤖', callback_data='bots')
    item2 = types.InlineKeyboardButton('С другом 👬', callback_data='friends')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, f'Битвы уже ждут тебя! С кем ты хочешь сыграть?', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_message(message):
    markup = types.InlineKeyboardMarkup(row_width=4)
    item1 = types.InlineKeyboardButton('Мои друзья 👬', callback_data='my_friends')
    item2 = types.InlineKeyboardButton('Мои победы 👍', callback_data='my_wins')
    item3 = types.InlineKeyboardButton('Мои поражения 👎', callback_data='my_loses')
    item4 = types.InlineKeyboardButton('Вернуться в бой 👊', callback_data='fight')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, f'Это Бот для игры в морской бой.\nты можешь играть как'
                                      f' с друзьями(если они у тебя есть), так и в одиночку с ботом.'
                                      f'\nДля начала игры нажми /start. Для конца игры нажми /stop .\n')
    bot.send_message(message.chat.id, 'Твои действия?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def answer(message):
    bot.send_message(message.chat.id, 'Я вас не понимаю.')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data == 'bots':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=None, text='Хорошо!')

            bot.send_message(call.message.chat.id, f'Ваше поле:\n'
                                                   f'    A   B   C   D   E   F   G   H   I   J\n'
                                                   f'1  {" ".join(battle.enemy_ships1[0])}\n'
                                                    f'2  {" ".join(battle.enemy_ships1[1])}\n'
                                                   f'3  {" ".join(battle.enemy_ships1[2])}\n'
                                                   f'4  {" ".join(battle.enemy_ships1[3])}\n'
                                                   f'5  {" ".join(battle.enemy_ships1[4])}\n'
                                                   f'6  {" ".join(battle.enemy_ships1[5])}\n'
                                                   f'7  {" ".join(battle.enemy_ships1[6])}\n'
                                                   f'8  {" ".join(battle.enemy_ships1[7])}\n'
                                                   f'9  {" ".join(battle.enemy_ships1[8])}\n'
                                                   f'10{" ".join(battle.enemy_ships1[9])}\n')
        elif call.data == 'friends':
            bot.send_message(call.message.chat.id, 'Данный режим еще не достпен.')
        elif call.data == 'my_friends':
            bot.send_message(call.message.chat.id, 'Данный режим еще не достпен.')
        elif call.data == 'my_wins':
            bot.send_message(call.message.chat.id, 'Данный режим еще не достпен.')
        elif call.data == 'my_loses':
            bot.send_message(call.message.chat.id, 'Данный режим еще не достпен.')
        elif call.data == 'fight':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('С ботом 🤖', callback_data='bots')
            item2 = types.InlineKeyboardButton('С другом 👬', callback_data='friends')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, f'Битвы уже ждут тебя! С кем ты хочешь сыграть?', reply_markup=markup)
    except Exception as e:
        pass


if __name__ == '__main__':
    bot.infinity_polling()
