#все импорты
import base64, binascii
from main import Text2ImageAPI
import telebot
from googletrans import Translator

#список пока человек в списке его запросы не принимают чтобы не нагружать ИИ
list_users = []
styles = ["ANIME","DEFAULT","UHD","KANDINSKY"]

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
@bot.message_handler(commands=['generate'])
def generate(message):
    try:
        user_id = message.from_user.id
    except:
        print("проблема повторите ещё раз")
    #если человек уже послал запрос то игнорурует
    #чтобы 1 человек моменте не нагружал программу
    if user_id in list_users:
        bot.reply_to(message,"ваш запрос уже в обработке  ")
    else:
        list_users.append(user_id)
        bot.reply_to(message, "введите описание фото")
        bot.register_next_step_handler(message, generate_step2)
        

def generate_step2(message):
    global text
    text = (message.text,'en', 'ru')
    print(f"для дебага {text}")
    bot.reply_to(message, f"введите один из стилей{styles}")
    bot.register_next_step_handler(message, generate_step3)

def generate_step3(message):
    style = message.text
    print(f"для дебага {style}")
    if message.text not in styles:
        bot.reply_to(message,"повторите ещё раз ")
        bot.register_next_step_handler(message,"ошибка")
    else:
        bot.reply_to(message,"отлично")
        user_id = message.from_user.id
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'token1',
                        'token2')
        model_id = api.get_model()
        uuid = api.generate(text, model_id,style=style)
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
