#все импорты
import base64, binascii
from main import Text2ImageAPI
import telebot
from googletrans import Translator

#список пока человек в списке его запросы не принимают чтобы не нагружать ИИ
list_users = []

# Замените 'YOUR_API_KEY' на ваш реальный API ключ Telegram Bot
with open('info.txt', 'r', encoding='utf-8') as file:
    token = file.read()
    print(token)

API_KEY = token
bot = telebot.TeleBot(API_KEY)

#Приветвенная функция
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! я бот для генерации картинок вот вес команды 1 /start показывает список команд 2 /generate генерирует картинку")

#основная функция
@bot.message_handler(func=lambda message: True)
def generate(message):
    user_id = message.from_user.id
    #если человек уже послал запрос то игнорурует
    #чтобы 1 человек моменте не нагружал программу
    if user_id in list_users:
        bot.reply_to(message,"ваш запрос уже в обработке  ")
    else:
        list_users.append(user_id)
        bot.register_next_step_handler(message, generate_step2)
        bot.reply_to(message, "введите описание фото")

def generate_step2(message):
    text = (message.text,'en', 'ru')
    print(f"для дебага {text}")
    user_id = message.from_user.id
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'API',
                        'sicret API')
    model_id = api.get_model()
    uuid = api.generate(text, model_id)
    images1 = api.check_generation(uuid)
    if isinstance(images1, list):
        images1 = ''.join(images1)

    try:
        image = base64.b64decode(images1, validate=True)
        file_path = f"D:\\windos_custom\\cd_todu\\images\\{user_id}.png"
        with open(file_path, "wb") as f:
            f.write(image)
            print("good")
    except binascii.Error as e:
        print(e)
    # Отправка изображения
    with open(file_path, 'rb') as photo:
        bot.send_photo(user_id, photo, "Вот ваша картинка!")
        list_users.remove(user_id)

bot.polling(True)