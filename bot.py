
import telebot

# Твой токен
TOKEN = '7207526455:AAHAtsEaW3nZyn4BrbxJhDCKnlcjB3lMQwM'

bot = telebot.TeleBot(TOKEN)

# Ответ на команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я твой бот трейдер!")

# Обработка всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я пока учусь! Но скоро буду подсказывать, когда покупать и продавать!")

# Запуск бота
print("Бот запущен...")
bot.infinity_polling()
