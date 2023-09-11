"""Bot to introduce the creator (me, hehehe)."""
import logging
import os

from dotenv import load_dotenv
from random import choice
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler


logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(message)s'
)
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FILE_PATH = os.getenv('FILE_PATH')
GIT = 'https://github.com/Glownts/introduce_bot'


def start(update, context):
    """Bot activation."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([
        ['Что умеет бот'],
        ['Рассказать о GPT для бабушки'],
        ['Объяснить разницу между SQL и noSQL'],
        ['Рассказать историю любви'],
        ['Ссылка на репу']
    ], resize_keyboard=True)
    try:
        context.bot.send_message(
            chat_id=chat.id,
            text=f'Приветсвую Вас, {name}! Что вы хотите узнать или увидеть?',
            reply_markup=buttons
        )
        logging.info('Message sent')
    except Exception:
        logging.info('Message not sent')


def text(update, context):
    """Sends info about bot: functionality or a link to the repo."""
    chat = update.effective_chat
    text = open(
        FILE_PATH + 'texts\\about.txt',
        encoding='utf-8',
        mode='r'
    ).read()
    if update.message.text == 'Ссылка на репу':
        text = GIT
    if update.message.text == 'Расскажи о хобби':
        text = open(
            FILE_PATH + 'texts\\hobby.txt',
            encoding='utf-8',
            mode='r'
        ).read()
    try:
        context.bot.send_message(chat_id=chat.id, text=text)
    except Exception:
        logging.info('Message not sent')


def photo(update, context):
    """Send requested photo of the bot creator."""
    chat = update.effective_chat
    path_ = FILE_PATH + 'photo\\'
    if update.message.text == 'Пришли селфи':
        path_ = FILE_PATH + 'selfie\\'
    file = choice(os.listdir(path_))
    try:
        context.bot.send_photo(chat_id=chat.id, photo=open(path_ + file, 'rb'))
        logging.info('Message sent')
    except Exception:
        logging.info('Message not sent')


def talk(update, context):
    """School photo of the bot creator."""
    chat = update.effective_chat
    file = 'love.mp3'
    if update.message.text != 'Рассказать историю любви':
        if update.message.text == 'Рассказать о GPT для бабушки':
            file = 'gpt.mp3'
        else:
            file = 'sql.mp3'
    try:
        context.bot.send_audio(
            chat_id=chat.id,
            audio=open(FILE_PATH + 'audio\\' + file, 'rb')
        )
        logging.info('Message sent')
    except Exception:
        logging.info('Message not sent')


def check():
    """Data integrity check."""
    paths = ('audio\\', 'photo\\', 'selfie\\')
    try:
        for path in paths:
            if os.listdir(FILE_PATH + path):
                logging.info(f'{path} data check complete')
        return True
    except FileNotFoundError:
        logging.error(f'{path} data is corrupted or missing ')
        return False


def main():
    """Start app."""
    if check():
        updater = Updater(token=TELEGRAM_TOKEN)
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(MessageHandler(
            Filters.text([
                'Что умеет бот',
                'Ссылка на репу',
                'Расскажи о хобби'
            ]), text)
        )
        updater.dispatcher.add_handler(MessageHandler(
            Filters.text(['Пришли фото', 'Пришли селфи']),
            photo)
        )
        updater.dispatcher.add_handler(MessageHandler(
            Filters.text([
                'Рассказать историю любви',
                'Рассказать о GPT для бабушки',
                'Объяснить разницу между SQL и noSQL'
            ]), talk)
        )
        updater.start_polling(poll_interval=2.0)
        updater.idle()
    else:
        logging.error('Media files not found')
        raise FileNotFoundError('Media files not found')


if __name__ == '__main__':
    main()
