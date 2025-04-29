import telebot
from telebot import types
import random

# Токен твоего бота
TOKEN = '7207526455:AAHAtsEaW3nZyn4BrbxJhDCKnlcjB3lMQwM'
bot = telebot.TeleBot(TOKEN)

# Разрешённый Telegram ID (только ты)
AUTHORIZED_USER_ID = 6955280259

# Храним выбранные данные пользователя
user_data = {}

# Команда старт
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != AUTHORIZED_USER_ID:
        bot.send_message(message.chat.id, "⛔️ Доступ запрещён. Вы не авторизованы для использования этого бота.")
        return
    show_main_menu(message)

# Главное меню
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Валютные пары")
    btn2 = types.KeyboardButton("Крипта")
    btn3 = types.KeyboardButton("Акции")
    btn4 = types.KeyboardButton("Индексы")
    btn5 = types.KeyboardButton("Фьючерсы")
    btn6 = types.KeyboardButton("Сырьё")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, "Выбери категорию актива:", reply_markup=markup)

# Обработка выбора категории
@bot.message_handler(func=lambda message: message.text in ["Валютные пары", "Крипта", "Акции", "Индексы", "Фьючерсы", "Сырьё"])
def select_asset_category(message):
    if message.chat.id != AUTHORIZED_USER_ID:
        return
    user_data[message.chat.id] = {'category': message.text}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == "Валютные пары":
        pairs = [
            "EUR/USD", "GBP/USD", "USD/JPY", "EUR/JPY", "AUD/USD", "USD/CHF", "USD/CAD", "NZD/USD",
            "BTC/USD", "ETH/USD", "XRP/USD", "LTC/USD", "SOL/USD",
            "AAPL", "TSLA", "GOOGL", "MSFT", "AMZN",
            "NSRGY", "BAYRY", "TCEHY", "SFTBY", "RYCEY",
            "SP500", "NAS100", "DAX", "FTSE100", "NIKKEI225",
            "SP500_OTC", "DOW_OTC", "NASDAQ_OTC",
            "XAU/USD", "XAG/USD", "WTI", "BRENT", "NGAS",
            "GOLD_OTC", "OIL_OTC", "SILVER_OTC"
        ]

        for pair in pairs:
            markup.add(types.KeyboardButton(pair))
        markup.add(types.KeyboardButton("⬅️ Главное меню"))
        bot.send_message(message.chat.id, "Выбери валютную пару:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Пока доступны только валютные пары для теста.", reply_markup=markup)

# Обработка выбора валютной пары
@bot.message_handler(func=lambda message: message.text in ["EUR/USD", "GBP/USD", "USD/JPY", "EUR/JPY", "AUD/USD"])
def select_pair(message):
    if message.chat.id != AUTHORIZED_USER_ID:
        return
    user_data[message.chat.id]['pair'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    timeframes = ["5s", "10s", "15s", "30s", "1m", "5m", "15m", "30m"]
    for tf in timeframes:
        markup.add(types.KeyboardButton(tf))
    markup.add(types.KeyboardButton("🔙 Главное меню"))
    bot.send_message(message.chat.id, "Выбери таймфрейм сделки:", reply_markup=markup)

# Обработка выбора таймфрейма
@bot.message_handler(func=lambda message: message.text in ["5s", "10s", "15s", "30s", "1m", "5m", "15m", "30m"])
def select_timeframe(message):
    if message.chat.id != AUTHORIZED_USER_ID:
        return
    user_data[message.chat.id]['timeframe'] = message.text
    signal = random.choice(["⬆️ Вверх (CALL)", "⬇️ Вниз (PUT)"])
    probability = random.randint(65, 85)
    pair = user_data[message.chat.id]['pair']
    timeframe = user_data[message.chat.id]['timeframe']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🔙 Главное меню"))
    bot.send_message(
        message.chat.id,
        f"Сигнал для {pair} на {timeframe}: {signal}\nВероятность успеха: {probability}%",
        reply_markup=markup
    )

# Обработка кнопки возврата в главное меню
@bot.message_handler(func=lambda message: message.text == "🔙 Главное меню")
def back_to_main_menu(message):
    if message.chat.id != AUTHORIZED_USER_ID:
        return
    show_main_menu(message)

# Обработка всех других сообщений
@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    if message.chat.id != AUTHORIZED_USER_ID:
        return
    show_main_menu(message)

# Запуск бота
bot.polling(non_stop=True)
