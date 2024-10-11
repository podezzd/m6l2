import telebot
from logic import Text2ImageAPI
from config import API_TOKEN_tg, API_KEY, SECRET_KEY

API_TOKEN = API_TOKEN_tg

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text

    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images = api.check_generation(uuid)[0]

    file_path = 'generated_image.jpg'
    api.save_image(images, file_path)

    with open(file_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()