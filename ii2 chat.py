import telebot
from telebot import types
from aiogram.utils.markdown import hlink


   

bot = telebot.TeleBot('7434516076:AAHy8lJtgHvHkrxomrVjwPmTOyxojrsRg8I')
@bot.message_handler(func=lambda message: message.text == 'Поговорить с асистентом')        
def asis(message):
    if message.text == 'Поговорить с асистентом':
        bot.send_message(message.chat.id, 'Сейчас обед))')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn4 = types.KeyboardButton('назад')
    btn1 = types.KeyboardButton('Вычеслить имт')
    btn2 = types.KeyboardButton('Узнать свою норму калорий')
    btn3 = types.KeyboardButton('Поговорить с асистентом')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Ваша поддержка в трудные времена", url='https://citaty.info/topic/urodstvo')
    markup.add(button1)
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на кнопку и перейди на сайт)".format(message.from_user), reply_markup=markup)
@bot.message_handler(func=lambda message: message.text == 'Вычеслить имт')
def rost(message):
    bot.send_message(message.chat.id, 'Напишите рост')
    bot.register_next_step_handler(message, get_height)

def get_height(message):
    if message.text == 'назад':
        start(message)
        return

    try:
        height = float(message.text)
        if height <= 0:
            raise ValueError
        bot.send_message(message.chat.id, 'Введите ваш вес:')
        bot.register_next_step_handler(message, get_weight, height)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное число для роста.')
        bot.register_next_step_handler(message, get_height)

def get_weight(message, height):
    if message.text == 'назад':
        start(message)
        return

    try:
        weight = float(message.text)
        if weight <= 0:
            raise ValueError
        imt = weight / (height / 100) ** 2

        if imt < 18.5:
            bot.send_message(message.chat.id, f"Ваш ИМТ: {imt:.2f}. Дефицит массы тела.")
        elif 18.5 <= imt < 25:
            bot.send_message(message.chat.id, f"Ваш ИМТ: {imt:.2f}. Норма.")
        else:
            bot.send_message(message.chat.id, f"Ваш ИМТ: {imt:.2f}. Жирдяй ебанный.")
        
        # Кнопка "назад" после результата ИМТ
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Вычеслить имт')
        btn2 = types.KeyboardButton('Узнать свою норму калорий')
        btn3 = types.KeyboardButton('Поговорить с асистентом')
        btn4 = types.KeyboardButton('назад')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
        
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное число для веса.')
        bot.register_next_step_handler(message, get_weight, height)

@bot.message_handler(func=lambda message: message.text == 'назад')
def back(message):
    start(message)
    
@bot.message_handler(func=lambda message: message.text == 'Узнать свою норму калорий')
def reg(message):

        bot.send_message(message.chat.id, "Введите ваш пол (МУЖИК/ЖЕНЩИНА):")
        bot.register_next_step_handler(message, process_sex)


                    
def process_sex(message):
    try:    
        sex = message.text
        bot.send_message(message.chat.id, "Введите ваш возраст в годах:")
        bot.register_next_step_handler(message, process_age, sex)
    except ValueError:
        bot.send_message(message.chat.id, 'Не коректные значеня')
            

def process_age(message, sex):
    try:
        age = int(message.text)
        bot.send_message(message.chat.id, "Введите ваш вес:")
        bot.register_next_step_handler(message, process_weight, sex, age)
    except ValueError:
        bot.send_message(message.chat.id, 'Не коректные значеня')
def process_weight(message, sex, age):
    try:
        weight = float(message.text)
        bot.send_message(message.chat.id, "Введите ваш рост:")
        bot.register_next_step_handler(message, process_height, sex, age, weight)
    except ValueError:
        bot.send_message(message.chat.id, 'Не коректные значеня')
def process_height(message, sex, age, weight):

    height = float(message.text)
    try:
        if sex == 'МУЖИК':
            BMR = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif sex == 'ЖЕНЩИНА':
            BMR = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        bot.send_message(message.chat.id, f"Ваш базальный метаболический расход (BMR): {BMR:.2f} ккал")
    except UnboundLocalError:
        bot.send_message(message.chat.id, 'Не коректные значеня')

bot.polling(none_stop=True)