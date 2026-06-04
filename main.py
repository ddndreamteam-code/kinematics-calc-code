import telebot
import math
import os
from dotenv import load_dotenv # Вот так правильно

load_dotenv() # Загружаем данные из файла .env
TOKEN = os.getenv('BOT_TOKEN') # Берем токен из скрытого окружения

bot = telebot.TeleBot(TOKEN)
bot = telebot.TeleBot(TOKEN)

# Словарик, чтобы временно хранить данные расчетов для каждого пользователя
user_data = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **Привет! Я бот для расчета прямой кинематики 2D-манипулятора.**\n\n"
        "Я помогу узнать точные координаты конца механической руки (схвата), "
        "зная длины звеньев и углы их поворота.\n\n"
        "Давай начнем! Отправь длину **первого звена L1** (в сантиметрах):"
    )
    # Инициализируем пустой словарь для этого конкретного пользователя
    user_data[message.chat.id] = {}
    
    # Отправляем сообщение и говорим: "следующий ответ юзера отправь в функцию get_l1"
    msg = bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')
    bot.register_next_step_handler(msg, get_l1)

def get_l1(message):
    try:
        l1 = float(message.text) # Проверяем, что ввели число
        user_data[message.chat.id]['l1'] = l1
        
        msg = bot.send_message(message.chat.id, "Отлично. Теперь введи длину **второго звена L2** (в см):", parse_mode='Markdown')
        bot.register_next_step_handler(msg, get_l2)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Ошибка! Введи длину числом (например, 45 или 12.5):")
        bot.register_next_step_handler(msg, get_l1) # Если косяк — спрашиваем заново

def get_l2(message):
    try:
        l2 = float(message.text)
        user_data[message.chat.id]['l2'] = l2
        
        msg = bot.send_message(message.chat.id, "Принято. Введи **угол поворота первого звена α** (в градусах):", parse_mode='Markdown')
        bot.register_next_step_handler(msg, get_alpha)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Ошибка! Введи длину числом:")
        bot.register_next_step_handler(msg, get_l2)

def get_alpha(message):
    try:
        alpha = float(message.text)
        user_data[message.chat.id]['alpha'] = alpha
        
        msg = bot.send_message(message.chat.id, "И последнее: введи **угол поворота второго звена β** относительно первого (в градусах):", parse_mode='Markdown')
        bot.register_next_step_handler(msg, get_beta)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Ошибка! Введи угол числом:")
        bot.register_next_step_handler(msg, get_alpha)

def get_beta(message):
    try:
        beta = float(message.text)
        chat_id = message.chat.id
        
        # Достаем все сохраненные ранее данные юзера
        l1 = user_data[chat_id]['l1']
        l2 = user_data[chat_id]['l2']
        alpha = user_data[chat_id]['alpha']
        
        # Переводим градусы в радианы для математики Python
        alpha_rad = math.radians(alpha)
        beta_rad = math.radians(beta)
        
        # Считаем тригонометрию (Прямая задача кинематики)
        # Формула учитывает, что второй угол считается относительно первого звена
        x = l1 * math.cos(alpha_rad) + l2 * math.cos(alpha_rad + beta_rad)
        y = l1 * math.sin(alpha_rad) + l2 * math.sin(alpha_rad + beta_rad)
        
        # Округляем до 2 знаков после запятой, чтобы было красиво
        x = round(x, 2)
        y = round(y, 2)
        
        # Выдаем финальный результат
        # Выдаем финальный результат (без капризных эмодзи)
        result_text = (
            "=== Расчет кинематики успешно завершен! ===\n\n"
            "Входные данные:\n"
            f" - L1 = {l1} см, L2 = {l2} см\n"
            f" - alpha = {alpha}°, beta = {beta}°\n\n"
            "Координаты рабочей точки (схвата):\n"
            f" X: {x} см\n"
            f" Y: {y} см\n\n"
            "Чтобы сделать новый расчет, нажми /start"
        )
        
        bot.send_message(chat_id, result_text, parse_mode='Markdown')
        
        # Чистим данные за собой, чтобы не засорять память компу
        user_data.pop(chat_id, None)
        
    except ValueError:
        msg = bot.send_message(message.chat.id, "Ошибка! Введи угол числом:")
        bot.register_next_step_handler(msg, get_beta)

print("Робо-бот запущен...")
bot.infinity_polling()