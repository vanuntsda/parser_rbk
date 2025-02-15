import telebot
import feedparser
import time
import os

# Загружаем переменные окружения
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
RSS_FEED = os.getenv("RSS_FEED")

bot = telebot.TeleBot(BOT_TOKEN)

def get_news():
    """Функция для парсинга новостей из RSS-ленты"""
    feed = feedparser.parse(RSS_FEED)
    if "entries" in feed:
        news_list = []
        for entry in feed.entries[:5]:  # Берем 5 последних новостей
            title = entry.title
            link = entry.link
            summary = entry.summary if hasattr(entry, "summary") else "Без описания"
            message = f"📰 *{title}*\n\n_{summary}_\n\n[Читать полностью]({link})"
            news_list.append(message)
        return news_list
    return []

def send_news():
    """Функция отправки новостей в Telegram-канал"""
    news = get_news()
    for item in news:
        bot.send_message(CHANNEL_ID, item, parse_mode="Markdown", disable_web_page_preview=False)

if __name__ == "__main__":
    while True:
        send_news()
        time.sleep(3600)  # Проверять новости каждый час
