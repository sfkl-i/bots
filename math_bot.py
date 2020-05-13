import telebot, datetime, re, time, math
from telebot import types
import numpy as np
from sympy import apart
from sympy.abc import x, y, z
from sympy import init_printing
from sympy import pprint
from sympy import together
from sympy import pi, E
from sympy import Symbol

BOT_TOKEN = '' # Токен Телеграм-бота
#BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)

TIMEOUT_CONNECTION = 5 # Таймаут переподключения

# Сообщение при старте
START_MESSAGE = """Отправь мне выражение, а я тебе скажу ответ."""
# Сообщение поддержки
HELP_MESSAGE = """Мной пользоваться очень просто. Вы мне отправляете выражение, а я вам возвращаю его результат.
***Особые функции***:
	квур а b с - квадратное уровнение с коэффициентами a b c;
    зн a/x+b/y - приведение к общему знаминателю;
    предел x+a b - нахождение предела функции x+a до предела b;
    диф x+ax b - вычисление производной x+ax с порядком b;
    инт x+k - интеграл от x+k; 
    опинт x+k a b - определенный интеграл x+k от a до b;
    0bx - перевести двоичное число х в десятичное;
    0ox - перевести восьмиричное число х в десятичное;
    0xx - перевести шестнадцатиричное число х в десятичное.
***Операторы***:
    + - сложение;
    - - вычитание;
    \* - умножение;
    / - деление;
    \*\* - возведение в степнь.
    
***Функции***:
    cos(x) - косинус x;
    sin(x) - синус x;
    tg(x) - тангенс x;
    fact(x) - факториал x;
    sqrt(x) - квадратный корень х;
    sqr(x) - х в квадрате.
***Логарифмы***:
    log2(x) - логарифм х по основанию 2;
    lg(х) - десятичный логарифм х;
    ln(x) - натуральный логарифм x;
    log(b, х) - логарифм х по основанию b;"""

пи = п = p = pi = 3.141592653589793238462643 # число Пи

# функции sympy
def fact(float_):
    return math.factorial(float_)

def cos(float_):
    return math.cos(float_)

def sin(float_):
    return math.sin(float_)

def tg(float_):
    return math.tan(float_)
    
def tan(float_):
    return math.tan(float_)


def ln(float_):
    return math.log(float_)

def log(base, float_):
    return math.log(float_, base)

def lg(float_):
    return math.log10(float_)

def log2(float_):
    return math.log2(float_)

def exp(float_):
    return math.exp(float_)

# Обработчик сообщений-команд
@bot.message_handler(commands=['start', 'help'])
def send_start(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))

    msg = None

    if message.text.lower() == '/start':
        msg = bot.send_message(message.chat.id, START_MESSAGE, parse_mode='markdown')

    elif message.text.lower() == '/help':
        msg = bot.send_message(message.chat.id, HELP_MESSAGE, parse_mode='markdown')

    if (msg):
        print('Бот: %s'%msg.text)

# Обработчик всех сообщений
@bot.message_handler(func = lambda message: True)
def answer_to_user(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))
    msg = None

    if message.text.lower() == 'помощь':
        msg = bot.send_message(message.chat.id, HELP_MESSAGE, parse_mode='markdown')
    elif re.search('квур -?\d+ -?\d+ -?\d+', message.text.lower()):
    	str1 = message.text.lower()
    	result = re.findall(r'-?\d+', str1)
    	print(result)
    	try:
    		a,b,c = map(float, result)
    		discr = (b * b) - 4 * a * c
    		if discr > 0:
    			x1 = (-b + math.sqrt(discr)) / (2 * a)
    			x2 = (-b - math.sqrt(discr)) / (2 * a)
    			msg = "x1 = " + str(x1) + "     x2 = " + str(x2)
    			bot.send_message(message.chat.id, msg)
    		elif discr == 0:
    			x = -b / (2 * a)
    			bot.send_message(message.chat.id, "x = " + str(x))
    		else:
    			bot.send_message(message.chat.id, "Корней нет.(D < 0)")
    	except:
    		bot.send_message(message.chat.id, "Что-то не так.Проверьте вводимые данные или напишите /help для помощи.")
    elif re.search('зн -?[0-9?a-z?A-Z?]', message.text.lower()):
        str1 = message.text.lower()
        try:
            result = re.sub(r"зн", "", str1, count=0)
            init_printing(use_unicode=False, wrap_line=False, no_global=True)
            from sympy import Symbol
            x = Symbol('x')
            y = Symbol('y')
            result1 = together(apart(result, x), x)
            bot.send_message(message.chat.id, result1)
        except:
            bot.send_message(message.chat.id, "Что-то не так.Проверьте вводимые данные или напишите /help для помощи.")
    elif re.search('предел -?[0-9?a-z?A-Z?]', message.text.lower()):
        str1 = message.text.lower()
        try:
            result1 = re.sub(r"предел", "", str1, count=0)
            bot.send_message(message.chat.id, "Вы ввели " + result1 + ".    Вычисление...")
            lst = result1.split()
            from sympy import Symbol
            user_func = lst[0]
            seek = lst[1]
            x = Symbol("x")
            y = Symbol("y")
            from sympy import limit
            result = limit(user_func, x, seek)
            bot.send_message(message.chat.id, result)
        except:
            bot.send_message(message.chat.id, "Что-то не так.Проверьте вводимые данные или напишите /help для помощи.")
    elif re.search('диф -?[0-9?a-z?A-Z?]', message.text.lower()):
        str1 = message.text.lower()
        result1 = re.sub(r"диф", "", str1, count=0)
        try:
            lst = result1.split()
            from sympy import Symbol
            x = Symbol('x')
            user_func1 = lst[0]
            order = lst[1]
            from sympy import diff
            res = 'Производная ' + order + '-ого порядка равна: ' 
            result = diff(user_func1, x, order)
            bot.send_message(message.chat.id, res + str(result))
        except:
            bot.send_message(message.chat.id, "Напишите /help для помощи.")
    elif re.search('опинт -?[0-9?a-z?A-Z?]', message.text.lower()):
        str1 = message.text.lower()
        try:
            result1 = re.sub(r"опинт", "", str1, count=0)
            lst = result1.split()
            from sympy import Symbol
            init_printing(use_unicode=False, wrap_line=False, no_global=True)
            x = Symbol('x')
            user_func3 = lst[0]
            a = lst[1]
            b = lst[2]
            from sympy import integrate
            result_2 = integrate(user_func3, (x, a, b))
            bot.send_message(message.chat.id, result_2)
        except:
            bot.send_message(message.chat.id, "Напишите /help для помощи.")
    elif re.search('инт -?[0-9?a-z?A-Z?]', message.text.lower()):
        str1 = message.text.lower()
        try:
            result1 = re.sub(r"инт", "", str1, count=0)
            init_printing(use_unicode=False, wrap_line=False, no_global=True)
            from sympy import Symbol
            x = Symbol('x')
            user_func2 = result1
            from sympy import integrate
            result_2 = integrate(user_func2, x)
            bot.send_message(message.chat.id, result_2)
        except:
            bot.send_message(message.chat.id, "Напишите /help для помощи.")

    try:
        answer = str(eval(message.text.lower().replace(' ', '')))
        msg = bot.send_message(message.chat.id, message.text.lower().replace(' ', '') + ' = ' + answer)
    except SyntaxError:
        msg = bot.send_message(message.chat.id, 'Похоже, что вы написали что-то не так. \nИсравьте ошибку и повторите снова')
    except NameError:
        #msg = bot.send_message(message.chat.id, 'Переменную которую вы спрашиваете я не знаю. \nИсравьте ошибку и повторите снова')
        msg = 1
    except TypeError:
        msg = bot.send_message(message.chat.id, 'Мне кажется, что в выражении присутствует ошибка типов. \nИсравьте ошибку и повторите снова')
    except ZeroDivisionError:
        msg = bot.send_message(message.chat.id, 'В выражении вы делите на ноль. \nИсравьте ошибку и повторите снова')

#    if (msg):
#        print('Бот: %s'%msg.text)

# Обработчик inline-запроса
@bot.inline_handler(func=lambda query: True)
def inline_answer_to_user(inline_query):
    answer = 0
    answer_list = []
    try:
        answer = str(eval(inline_query.query.lower().replace(' ', '')))
        answer_to_send = answer.replace('*', '\*')
        query_to_send = inline_query.query.replace('*', '\*').lower().replace(' ', '')

        answer_list.append(types.InlineQueryResultArticle(
            id = 0,
            title = 'Отправить с выражением',
            description='%s = %s' % (inline_query.query, answer),
            input_message_content = types.InputTextMessageContent(
                message_text = '%s = *%s*' % (query_to_send, answer_to_send),
                parse_mode = 'markdown'),
            thumb_url = WITH_ICON
        ))

        answer_list.append(types.InlineQueryResultArticle(
            id = 1,
            title = 'Отправить без выражения',
            description='%s' % (answer),
            input_message_content = types.InputTextMessageContent(
                message_text = '*%s*' % (answer_to_send),
                parse_mode = 'markdown'),
            thumb_url = WITHOUT_ICON
        ))
            
    except SyntaxError: answer = False
    except NameError: answer = False
    except TypeError: answer = False
    except ZeroDivisionError: answer = False

    if (not answer):    
        answer_list = []
        answer_list.append(types.InlineQueryResultArticle(
            id = 0,
            title = 'Калькулятор',
            description='Чтобы посичтать выражение - введите его.\nЕсли вы хотите просмотреть справку, то перейдите в диалог со мной и напишите \"/help\"',
            input_message_content = types.InputTextMessageContent(message_text = 'Я хотел посчитать выражение, но нажал не туда')
        ))
    
    bot.answer_inline_query(inline_query.id, answer_list)

# Вход в программу
if (__name__ == '__main__'):
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print ('Ошибка подключения. Попытка подключения через %s сек.'%TIMEOUT_CONNECTION)
            time.sleep(TIMEOUT_CONNECTION)