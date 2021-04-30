import telebot
from telebot import types
import random
import config
import sqlighter
import battle
import sqlite3

# BattleShipGameBot
# @battleshhipbot

bot = telebot.TeleBot(config.TOKEN)
pole = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
        'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
        'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
        'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
        'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
        'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',
        'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10',
        'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10',
        'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10',
        'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10']
batle = None
points_d = 0
points_u = 0
player_ships = None
enemy_ships = None
enemy_ships2 = None


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


@bot.message_handler(commands=['stop'])
def stop_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Вернуться в бой 👊', callback_data='fight')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Сбросить якорь!!!⚓', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def answer(message):
    global batle, pole
    bot.send_message(message.chat.id, 'Я вас не понимаю.')
    a = False
    print(pole)
    for i in pole:
        if i == message.text:
            a = True
    print(a, batle)
    if batle and a:
        user_atac(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global batle, points_d, player_ships, enemy_ships, points_u, enemy_ships2
    try:
        if call.data == 'bots':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=None, text='Хорошо!')
            player_ships = battle.enemy_ships1
            enemy_ships = battle.enemy_ships2
            enemy_ships2 = [[' ░ ' for i in range(10)] for j in range(10)]
            bot_atac(call)
            points_d = 0
            points_u = 0
            batle = True
        elif call.data == 'friends':
            bot.send_message(call.message.chat.id, 'Данный режим еще не достпен.')
        elif call.data == 'my_friends':
            bot.send_message(call.message.chat.id, 'Данный режим еще не достпен.')
        elif call.data == 'my_wins':
            bot.send_message(call.message.chat.id, 'Данный режим еще не достпен.')
        elif call.data == 'my_loses':
            bot.send_message(call.message.chat.id, 'Данный режим еще не достпен.')
        elif call.data == 'atac':
            bot.send_message(call.message.chat.id, 'Напишите клетку для отаки')
        elif call.data == 'fight':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('С ботом 🤖', callback_data='bots')
            item2 = types.InlineKeyboardButton('С другом 👬', callback_data='friends')
            markup.add(item1, item2)
            bot.send_message(call.message.chat.id, f'Битвы уже ждут тебя! С кем ты хочешь сыграть?', reply_markup=markup)
    except Exception as e:
        pass


def bot_atac(call):
    global batle, points_d, player_ships, enemy_ships
    a, b = random.randint(0, 9), random.randint(0, 9)
    if player_ships[a][b] == ' ▓ ':
        points_d += 1
        player_ships[a][b] = ' ▒ '
    else:
        player_ships[a][b] = '×'
    if points_d == 20:
        bot.send_message(call.message.chat.id, 'Вы проиграли')
        sqlighter.lose(call.message.from_user.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Отаковать в ответ 👊', callback_data='atac')
    markup.add(item1)
    bot.send_message(call.message.chat.id, f'Ваше поле:\n'
                                           f'     A    B    C    D    E    F    G    H    I    J\n'
                                           f'1  {" ".join(player_ships[0])}\n'
                                           f'2  {" ".join(player_ships[1])}\n'
                                           f'3  {" ".join(player_ships[2])}\n'
                                           f'4  {" ".join(player_ships[3])}\n'
                                           f'5  {" ".join(player_ships[4])}\n'
                                           f'6  {" ".join(player_ships[5])}\n'
                                           f'7  {" ".join(player_ships[6])}\n'
                                           f'8  {" ".join(player_ships[7])}\n'
                                           f'9  {" ".join(player_ships[8])}\n'
                                           f'10{" ".join(player_ships[9])}\n'
                                           f'Вас отаковали: {chr(b + 97)}{a + 1}', reply_markup=markup)


def user_atac(message):
    global batle, points_d, player_ships, enemy_ships
    a = int(message.text[1])
    b = message.text[0]
    print(a, b)
    a, b = random.randint(0, 9), random.randint(0, 9)
    if player_ships[a][b] == ' ▓ ':
        points_d += 1
        player_ships[a][b] = '❌'
    else:
        player_ships[a][b] = '×'
    if points_u == 20:
        bot.send_message(message.chat.id, 'Вы выиграли!')
        batle = False
        # sqlighter.lose(message.from_user.id)

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Отакаовать в ответ 👊', callback_data='atac')
    markup.add(item1)
    bot.send_message(message.chat.id, f'Ваше поле:\n'
                                           f'    A   B   C   D   E   F   G   H   I   J\n'
                                           f'1  {" ".join(enemy_ships2[0])}\n'
                                           f'2  {" ".join(enemy_ships2[1])}\n'
                                           f'3  {" ".join(enemy_ships2[2])}\n'
                                           f'4  {" ".join(enemy_ships2[3])}\n'
                                           f'5  {" ".join(enemy_ships2[4])}\n'
                                           f'6  {" ".join(enemy_ships2[5])}\n'
                                           f'7  {" ".join(enemy_ships2[6])}\n'
                                           f'8  {" ".join(enemy_ships2[7])}\n'
                                           f'9  {" ".join(enemy_ships2[8])}\n'
                                           f'10{" ".join(enemy_ships2[9])}\n'
                                           f'Вас отаковали: {chr(b + 97)}{a + 1}❌', reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling()
