import datetime
import requests
from bs4 import BeautifulSoup
import fake_useragent
import telebot
from telebot import types
import random
from mysql import *
from datetime import date
import os
import zipfile
from db import *
bot = telebot.TeleBot(TOKEN)


anektodes = ['В наших военкоматах завелся Робин Гуд. Он отбирает повестки у богатых и отдает их бедным.', 'Первые 10 человек, которым военкоматы не смогли вручить повестки после объявления очередной мобилизации, объявлены Украиной в международный розыск.',
             '- Если в своем почтовом ящике вы обнаружили письмо, в заголовке которого имеются слова "повестка" и "военкомат" - уничтожьте его не открывая. В нем содержится опасный вирус, который может лишить вас Интернета и компьютера на 2 года!',
             'Ничто так не бодрит с утра, как участковый с повесткой в военкомат.',
             'Винни-пуху и Пяточку пришла повестка из военкомата. Идут они, значится, туда и волнуются очень - будут их наголо брить или не будут. Решили спросить кого-нибудь. \n- Давай вон у той Крысы спросим!\n- Давай!\n- Эй, Крыса! Будут нас в армии наголо брить?\n- Я не крыса, я - ёжик..',
             'Счастье, это когда военкомат выслал тебе повестку, а у тебя мама директор почты.',
             '- Здравия желаю! Вам повестка в военкомат. - Да вы что... какая повестка?! Вы посмотрите на меня, я больной человек, у меня астма, плоскостопие, двое детей в конце концов... - Да мне-то какая разница! - Вы как с женщиной разговариваете?!!!',
             'Звонок в дверь, хозяин идет открывать. - Кто? - Вам повестка. - Так я уже отслужил! - Ну ничего, теперь ещё и отсидишь... ',
             'Если Вы получили письмо со словами "повестка" и "военкомат" разорвите его на месте потому что Вас лишат на 2 года компьютера и Интернета.',
             'Хорошо быть востребованным ... но не повесткой!',
             'Взрослые говорят: "Не матерись, тут дети". А дети говорят: "Не матерись, тут взрослые". ']

@bot.message_handler(commands=['start', 'help'])
def start(message):
    print(datetime.date)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item2 = types.KeyboardButton('👁‍🗨Парсинг товаров')
    item3 = types.KeyboardButton('💸 Махинации с чеком')
    item4 = types.KeyboardButton('🔔 Информация')
    item5 = types.KeyboardButton('⛓ Другое')
    item6 = types.KeyboardButton('Отчёт')

    markup.add(item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, 'Привет,{0.first_name}'.format(message.from_user), reply_markup = markup)

def send_report_money(message):
    try:
        DATE_DAY = (message.text).replace('.', '-').replace('=', '-').replace('/', '-')
        print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
              'Просматривает отчёт продуктов за ', DATE_DAY)
    except:
        print('Error 40')
        return False

    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    cursor.execute(f"SELECT ID, Цена, Наименование, Количество FROM Price WHERE DATE(`created`) = '{DATE_DAY}'")

    print("ID    Цена    Наименование")
    result = cursor.fetchall()
    print("ID    Цена    Наименование")
    bot.send_message(message.chat.id, "ID    Цена    Наименование")
    for row in result:
        print(row['ID'], '    ', row['Цена'], '    ', row['Наименование'])
        products = [(row['ID'], (row['Цена']), row['Наименование'])]
        new_id = row['ID']
        new_price = row['Цена']
        new_name = row['Наименование']
        new_products = str(new_id) + '     ' + str(new_price) + '      ' + str(new_name)
        # Создать 3 новых переменных, создать из них одну STR, выводить её.
        bot.send_message(message.chat.id, new_products)
    cursor.execute(f"SELECT SUM(Цена) FROM Price WHERE DATE(`created`) = '{DATE_DAY}'")
    result = cursor.fetchall()
    for row in result:
        summa1 = "Сумма потраченных денег за выбранный день:  "
        summa2 = row['SUM(Цена)']
        summa = summa1 + str(summa2) + ' руб.'
        bot.send_message(message.chat.id, summa)
        print('Сумма потраченных денег за выбранный день:', row['SUM(Цена)'])


def all_my_products_in_database(message):
    print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
          '-------------------ПРОСМАТРИВАЕТ ВСЕ ТОВАРЫ В БАЗЕ ДАННЫХ--------------------------')
    db = connect(**MYSQLCONF)
    cursor = db.cursor()

    cursor.execute("SELECT ID, Цена, Наименование, Количество FROM `Price`")
    result = cursor.fetchall()
    print("ID    Цена    Наименование")
    bot.send_message(message.chat.id, "ID    Цена    Наименование")
    for row in result:
        print(row['ID'], '    ', row['Цена'], '    ', row['Наименование'])
        products = [(row['ID'], (row['Цена']), row['Наименование'])]
        new_id = row['ID']
        new_price = row['Цена']
        new_name = row['Наименование']
        new_products = str(new_id) + '     ' + str(new_price) + '      ' + str(new_name)
        # Создать 3 новых переменных, создать из них одну STR, выводить её.
        bot.send_message(message.chat.id, new_products)
    db.close()


def add_product_to_database():

    db = connect(**MYSQLCONF)
    cursor = db.cursor()

    cursor.execute(
        f"INSERT INTO `Price` (`ID`, `Цена`, `Наименование`, `Количество`) VALUES (NULL, '{price}', '{name}', '{count}')")
    row = cursor.fetchall()
    #   print(row)
    db.close()
    print('Продукт успешно добавлен в базу данных')



def delete_product_from_database(message):
    PRODUCT_ID = message.text
    print(message.from_user.first_name, message.from_user.last_name, message.from_user.id, 'Заупстил функцию удаления товара')
    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    try:
        cursor.execute(f"DELETE FROM `Price` WHERE `Price`.`ID` = {PRODUCT_ID}")
    except:
        bot.send_message(message.chat.id, 'Нельзя использовать другие символы кроме цифр!')
        return False
    print('\nТОВАР УСПЕШНО УДАЛЁН!\n-Вывожу новый список товаров-')
    bot.send_message(message.chat.id, 'Товар успешно удалён!')
    all_my_products()


def info_about_my_product(message):
    print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
          'Заупстил функцию информации о товаре')
    bot.send_message(message.from_user.id, f"Наименование товара: {name}\n"
                                           f"Цена товара: {price}" + " руб.\n"
                                           f"Количество единиц товара: {count}" + " шт.\n")
    add_product_to_database()

def get_count_product(message):
    print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
          'Заупстил функцию получения количества единиц товара')
    global count
    try:
        count = int(message.text)
        if count < 0:
            bot.send_message(message.chat.id,'Количество не может быть отрицательным!')
            return False
        print('Указанная единица товара = ', count)
        msg = bot.send_message(message.from_user.id, 'Ваши заполненные данные: ')
        info_about_my_product(message)
    except Exception:
        bot.send_message(message.chat.id, '[ERROR] * Единица товара должна состоять только из цифр *')
def get_price_product(message):
    print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
          'Заупстил функцию стоимости товара')
    global price
    try:
        price = int(message.text)
        if price < 0:
            bot.send_message(message.chat.id,'Цена не может быть отрицательной!')
            return False
        print('Указанная цена товара = ', price)
        msg = bot.send_message(message.from_user.id, 'Введите наименование товара')
        bot.register_next_step_handler(msg, get_name_product)
    except Exception:
        bot.send_message(message.chat.id, '[ERROR] * Цена должна состоять только из цифр *')
def get_name_product(message):
    print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
          'Заупстил функцию наименования товара')
    global name
    name = message.text
    print('Указанное наименование товара = ', name)
    msg = bot.send_message(message.from_user.id, 'Введите количество единиц товара')
    bot.register_next_step_handler(msg, get_count_product)



@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🎰 Рандомное число':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'Крутит 🎰 Рандомное число')
            bot.send_message(message.chat.id, 'Ваше рандомное число: ' + str(random.randint(0, 1000)))
        elif message.text == '💸 Махинации с чеком':
            if message.from_user.id == 1164013363:
                print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                      'Перешёл в пункт  💸 Махинации с чеком')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('✅ Добавить товар')
                item2 = types.KeyboardButton('❌ Удалить товар')
                item3 = types.KeyboardButton('📚 Все продукты')
                item4 = types.KeyboardButton('Отчёт по дням')
                item5 = types.KeyboardButton('❓ Помощь')
                back = types.KeyboardButton('🔙 Вернуться назад')
                markup.add(item1, item2, item3, item4, item5, back)
                bot.send_message(message.chat.id, '💸 Махинации с чеком', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, '<b>Этот пункт доступен только <a href="tg://user?id=1164013363">Администрации</a>!</b>', parse_mode="HTML")
        elif message.text == '✅ Добавить товар':
            msg = bot.send_message(message.chat.id, 'Введите цену товара')
            bot.register_next_step_handler(msg, get_price_product)
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'ДОБАВЛЯЕТ ТОВАР В БАЗУ ДАННЫХ')
        elif message.text == '❌ Удалить товар':
            all_my_products_in_database(message)
            msg = bot.send_message(message.chat.id, 'Введите ID продукта, который вы хотите удалить: ')
            bot.register_next_step_handler(msg, delete_product_from_database)
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'УДАЛЯЕТ ТОВАР ИЗ БАЗЫ ДАННЫХ')
        elif message.text == '📚 Все продукты':
            all_my_products_in_database(message)

        elif message.text == 'Отчёт по дням':
            today_date = 'Введите дату, за которую хотите получить отчёт: \nПример:', datetime.date.today()
            msg = bot.send_message(message.chat.id, f'Введите дату, за которую хотите получить отчёт: \nПример: {date.today()}')
            bot.register_next_step_handler(msg, send_report_money)

        elif message.text == '❓ Помощь':
            messages = '"✅ Добавить товар" - Введите данные о купленом продукте, он попадёт в базу данных.\n' \
                       '"❌ Удалить товар" - Удаляет товар из базы данных. Изначально выводится весь список товаров с ID. Нужно ввести ID товара, он удалится из базы данных.\n' \
                       '"📚 Все продукты" - Выводит все продукты в базе данных в формате: ID, PRICE, NAME'
            bot.send_message(message.chat.id, messages, parse_mode="HTML", disable_web_page_preview=True)




        elif message.text == '🔔 Информация':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'Перешёл в пункт 🔔 Информация')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🤖 О боте')
            item2 = types.KeyboardButton('👤 Разработчик бота')
            back = types.KeyboardButton('🔙 Вернуться назад')
            markup.add(item1, item2, back)

            bot.send_message(message.chat.id, '🔔 Информация', reply_markup=markup)

        elif message.text == '⛓ Другое':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'Перешёл в пункт ⛓ Другое')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('⚙ Настройка')
            item2 = types.KeyboardButton('🎭 Стикер')
            item3 = types.KeyboardButton("🔊Музыка")
            item4 = types.KeyboardButton('🎰 Рандомное число')
            item5 = types.KeyboardButton('😂 Анекдот')
            back = types.KeyboardButton('🔙 Вернуться назад')
            markup.add(item1, item2, item3, item4, item5, back)

            bot.send_message(message.chat.id, '⛓ Другое', reply_markup=markup)
        elif message.text == '🔙 Вернуться назад':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'ВЕРНУЛСЯ НАЗАД')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            item2 = types.KeyboardButton('👁‍🗨Парсинг товаров')
            item3 = types.KeyboardButton('💸 Махинации с чеком')
            item4 = types.KeyboardButton('🔔 Информация')
            item5 = types.KeyboardButton('⛓ Другое')
            item6 = types.KeyboardButton('Отчёт')

            markup.add(item2, item3, item4, item5, item6)
            bot.send_message(message.chat.id, '🔙 Вернуться назад', reply_markup=markup)
        elif message.text == '🎭 Стикер':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'Отправил себе стикер')
            stick = open('media/stickers/telegram_stick.webp', 'rb')
            bot.send_sticker(message.chat.id, stick)
        elif message.text == '🔊Музыка':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'Зашёл в раздел с музыкой')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('1️⃣ Получить 10 секундную музыку')
            item2 = types.KeyboardButton('📂 Получить архив с музыкой')
            item3 = types.KeyboardButton('⏩ Получить всю музыку в диалог')
            item4 = types.KeyboardButton('🔙 Вернуться назад')
            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, '🔊Музыка', reply_markup=markup)
        elif message.text == '1️⃣ Получить 10 секундную музыку':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'Отправил себе одну музыку')
            choose_random_music = random.randrange(2, 12)
            audio = open(f'media/audio/{choose_random_music}.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)
            audio.close()
        elif message.text == '⏩ Получить всю музыку в диалог':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'Отправил себе всю музыку')
            for filename in os.listdir("media/audio"):
                f = os.path.join("media/audio", filename)
                audio = open(f'{f}', 'rb')
                bot.send_audio(message.chat.id, audio)
                audio.close()
        elif message.text == '📂 Получить архив с музыкой':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'Отправил себе архив с музыкой')
            with zipfile.ZipFile('music.zip', 'w') as myzip:
                for filename in os.listdir("media/audio"):
                    f = os.path.join("media/audio", filename)
                    myzip.write(f)
            with open('music.zip', 'rb') as file:
                bot.send_document(message.chat.id, file)


        elif message.text == '🤖 О боте':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                  'Вывел информацию 🤖 О боте')
            bot.send_message(message.chat.id, '<u>🤖 О боте</u>'
                                              '\n\n '
                                              '<b>Бот разработан с целью изучения библиотеки TeleBot и MYSQL</b>\n'
                                              'Основной задачей бота являлся пункт 💸 Махинации с чеком, где пользователь мог отслеживать свои траты в определенный день, добавляя и редактируя список покупаемых товаров.\n'
                                              '\nБот продолжает развиваться, поэтому <b>бот становится универсальным и многозадачным</b>, из-за чего он не имеет узконаправленную задачу.\n'
                                              '\nВторым основным пунктом является пункт "👁‍🗨Парсинг товаров". \nПользователь может задавать ссылку на определенный сайт с товаром, о котором он будет получать информацию в телеграм боте.\n'
                                              'Такой функционал преимущественно используется для отслеживания цены товара и приобретения его по более низкой цене.\n'
                                              '\n<strong>В каждом пункте имеется <i>"Помощь"</i>, где описаны все хитрости использования команд. </strong>', parse_mode="HTML")

        elif message.text == '👤 Разработчик бота':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                'Открыл информации о разработчике бота')
            messages = '<b><u>Информация о разработчике</u></b>\n\n' \
                       '<strong>Социальные сети:</strong> \n' \
                       '- <a href="https://vk.com/wolf_rb">ВКонтакте</a> \n'\
                       '- <a href="https://t.me/CreativiTTy">Telegram</a> \n' \
                       '- <b>Discord:</b> <span class="tg-spoiler">Familiar#5206</span>'
            bot.send_message(message.chat.id, messages, parse_mode="HTML", disable_web_page_preview=True)
        elif message.text == '😂 Анекдот':
            print(message.from_user.first_name, message.from_user.last_name, message.from_user.id,
                'Захотел посмеяться, выбрав пункт 😂 Анекдот')
            bot.send_message(message.chat.id, random.choice(anektodes))
            # audio = open('media/audio/2.mp3', 'rb')
            # bot.send_audio(message.chat.id, audio)


bot.polling(none_stop=True)