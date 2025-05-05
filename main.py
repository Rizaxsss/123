import os
import telebot
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-3.5-turbo"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Здравствуйте, мы готовы вам помочь с короткими текстами всего за полчашки кофе!")

@bot.message_handler(func=lambda message: True)
def generate_text(message):
    prompt = message.text.strip()
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://t.me/YOUR_BOT_USERNAME",  # замените на ваше имя бота
        "X-Title": "SnappyTextBot"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, "❌ Не удалось сгенерировать текст. Попробуйте позже.")
        print(f"Error: {e}")

bot.polling()