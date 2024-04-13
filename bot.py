from telebot import types
import telebot
import json
with open('settings.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
with open('test.json', 'r', encoding='utf-8') as f:
    test = json.load(f)
bot = telebot.TeleBot(data['TOKEN'])
@bot.message_handler(commands = ['start'])
def index(message):
    global var
    var = []
    st = test[f'questions_{len(var) + 1}']['question']
    answers = ''
    for x in test[f'questions_{len(var) + 1}']['answers']:
        answers += f"{x}: {test[f'questions_' + str(len(var) + 1)]['answers'][x]}\n"
    markup = types.InlineKeyboardMarkup(row_width = 4)
    A_button = types.InlineKeyboardButton(text = 'A', callback_data = 'A')
    B_button = types.InlineKeyboardButton(text = 'B', callback_data = 'B')
    C_button = types.InlineKeyboardButton(text = 'C', callback_data = 'C')
    D_button = types.InlineKeyboardButton(text = 'D', callback_data = 'D')
    markup.add(A_button, B_button, C_button, D_button)
    bot.send_message(message.chat.id, text = f'{len(var) + 1}: {st}\n{answers}', reply_markup = markup)
@bot.callback_query_handler(func = lambda call: True)
def buttons(call):
    var.append(call.data)
    if len(var) != 10:
        st = test[f'questions_{len(var) + 1}']['question']
        answers = ''
        for x in test[f'questions_{len(var) + 1}']['answers']:
            answers += f"{x}: {test['questions_' + str(len(var) + 1)]['answers'][x]}\n"
        markup = types.InlineKeyboardMarkup(row_width = 4)
        A_button = types.InlineKeyboardButton(text = 'A', callback_data = 'A')
        B_button = types.InlineKeyboardButton(text = 'B', callback_data = 'B')
        C_button = types.InlineKeyboardButton(text = 'C', callback_data = 'C')
        D_button = types.InlineKeyboardButton(text = 'D', callback_data = 'D')
        markup.add(A_button, B_button, C_button, D_button)
        bot.send_message(call.message.chat.id, text = f'{len(var) + 1}: {st}\n{answers}', reply_markup = markup)
    else:
        cortAns = 0
        s = 1
        for x in var:
            if (test[f'questions_{s}']['answers'][x] == test[f'questions_{s}']['correctAnswer']):
                cortAns += 1
            s += 1
        bot.send_message(call.message.chat.id, text = f'Правельных ответов {cortAns}/10')
@bot.message_handler(content_types= ['text'])
def texting(message):
    bot.send_message(message.chat.id, text = 'Используйте кнопки чтобы отвечать на вопросы')
bot.infinity_polling()
