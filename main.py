#--coding: utf-8--
import logging
from aiogram import Bot, Dispatcher, types
#from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor
import database as db
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import threading

menu_buttons = ["Классика", "Авторское меню"]

menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
for button in menu_buttons:
        menu_keyboard.add(button)

classic_menu = [
    "Капучино",
    "Американо с молоком",
    "Латте",
    "Эспрессо с молоком",
    "Горячий шоколад",
    "Какао",
    "Раф",
    "Флэт Уайт",
	"Мокачино",
    "Назад"
]

custom_menu = [
    "Раф Кава Кокос",
    "Раф Кава Шоколад",
    "Раф Кава Мёд",
    "Латте Bounty",
    "Латте Snickers",
    "Латте Oreo",
    "Латте Солёная Карамель",
    "Вишнёвый Мокко",
    "Матча с белым шоколадом",
    "Ванильно-медовый капучино",
    "Бомбино",
    "Назад"
]

classic_dict_small = {
	"Капучино": 150,
    "Американо с молоком": 30,
    "Латте": 150,
    "Эспрессо с молоком": 30,
    "Горячий шоколад": 100,
    "Раф": 100,
    "Флэт Уайт": 110,
	"Мокачино": 150
}

classic_dict_middle = {
	"Капучино": 200,
    "Американо с молоком": 50,
    "Латте": 230,
    "Горячий шоколад": 150,
    "Какао": 230,
    "Раф": 170,
	"Мокачино": 200
}

classic_dict_large = {
	"Капучино": 300,
    "Американо с молоком": 70,
    "Латте": 300,
    "Горячий шоколад": 250,
    "Какао": 330,
    "Раф": 220,
	"Мокачино": 250
}

classic_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
for button in classic_menu:
        classic_menu_keyboard.add(button)

custom_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
for button in custom_menu:
        custom_menu_keyboard.add(button)

size_buttons = ["Маленький", "Средний", "Большой", "Назад"]

size_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
for button in size_buttons:
        size_keyboard.add(button)

API_TOKEN = '6749577684:AAGUrE2L-INm8dunF9DdNtw-_6wrcLQAT1M'

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Определение команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	userid = message.from_user.id
	if not db.check(userid):
		await bot.send_message(message.chat.id, "Привет, для авторизации введи код: ")
	else:
		db.setstate(userid, 1)
		await bot.send_message(message.chat.id, "Вы уже авторизованы!", reply_markup=menu_keyboard)

# Текст
@dp.message_handler()
async def message(message: types.Message):
	userid = message.from_user.id
	text = message.text

	#-----------
	if not db.check(userid):
		file = open("users.txt", "rb")
		codes = str(file.read()).replace("b", "").replace("'", "").split("\\r\\n")
		print(codes)
		if message.text in codes:
			db.newuser(userid)
			await bot.send_message(message.chat.id, "Вы успешно авторизовались!", reply_markup=menu_keyboard)
		else:
			await bot.send_message(message.chat.id, "Вас нет в базе данных!")
		print(type(message.text), type(codes[0]))
	#-----------

	elif db.check(userid):
		state = db.getstate(userid)
		if text == "Назад":
			#state = db.getstate(userid)
			#if state == 3:
				#db.setstate(userid, 2)
				#db.setsize(userid, 1)
				#await bot.send_message(message.from_user.id, "Выберите размер: ", reply_markup=size_keyboard)
			if state == 3 or state == 2 or state == 1: #el
				db.setstate(userid, 1)
				db.setsize(userid, 1)
				db.setdrink(userid, "")
				await bot.send_message(message.from_user.id, "Выберите раздел: ", reply_markup=menu_keyboard)
		elif state == 0:
			db.setstate(userid, 1)
			await bot.send_message(message.chat.id, "Выберите раздел: ", reply_markup=menu_keyboard)
		elif state == 1:
			if text == "Классика":
				db.setstate(userid, 2)
				await bot.send_message(message.from_user.id, "Выберите напиток: ", reply_markup=classic_menu_keyboard)
			elif text == "Авторское меню":
				db.setstate(userid, 2)
				await bot.send_message(message.from_user.id, "Выберите напиток: ", reply_markup=custom_menu_keyboard)
			else:
				await bot.send_message(message.from_user.id, "Выберите раздел!")
		elif state == 2:
			if text in classic_menu:
				db.setdrink(userid, text)
				db.setstate(userid, 3)
				await bot.send_message(message.from_user.id, "Выберите размер: ", reply_markup=size_keyboard)
			elif text in custom_menu:
				db.setdrink(userid, text)
				db.setstate(userid, 3)
				await bot.send_message(message.from_user.id, "Выберите размер: ", reply_markup=size_keyboard)
			else:
				await bot.send_message(message.from_user.id, "Выберите напиток!")
		elif state == 3:
			if text in size_buttons:
				drink = db.getdrink(userid)
				if text == "Маленький":
					if drink in classic_dict_small:
						db.setsize(userid, 1)
						db.setstate(userid, 4)
						await bot.send_message(message.chat.id, f"{drink}, {text}, налитое кол-во молока: ", reply_markup=ReplyKeyboardRemove())
					elif drink not in classic_dict_small:
						await bot.send_message(message.chat.id, f"Напитка такого размера нет.", reply_markup=size_keyboard)
				if text == "Средний":
					if drink in classic_dict_middle:
						db.setsize(userid, 2)
						db.setstate(userid, 4)
						await bot.send_message(message.chat.id, f"{drink}, {text}, налитое кол-во молока: ", reply_markup=ReplyKeyboardRemove())
					elif drink not in classic_dict_middle:
						await bot.send_message(message.chat.id, f"Напитка такого размера нет.", reply_markup=size_keyboard)
				if text == "Большой":
					if drink in classic_dict_large:
						db.setsize(userid, 3)
						db.setstate(userid, 4)
						await bot.send_message(message.chat.id, f"{drink}, {text}, налитое кол-во молока: ", reply_markup=ReplyKeyboardRemove())
					elif drink not in classic_dict_large:
						await bot.send_message(message.chat.id, f"Напитка такого размера нет.", reply_markup=size_keyboard)
		elif state == 4:
			drink = db.getdrink(userid)
			size = db.getsize(userid)
			if size == 1:
				plus = int(classic_dict_small.get(drink))-int(message.text)
				milk = db.getmilk(userid)
				db.setmilk(userid, milk+plus)
				db.setstate(userid, 1)
				db.setdrink(userid, "")
				db.setsize(userid, 1)
				await bot.send_message(message.from_user.id, f"Молоко записано в базу! Ваш общий плюс: {milk}(+{plus}) мл.", reply_markup=menu_keyboard)
			if size == 2:
				plus = int(classic_dict_middle.get(drink))-int(message.text)
				milk = db.getmilk(userid)
				db.setmilk(userid, milk+plus)
				db.setstate(userid, 1)
				db.setdrink(userid, "")
				db.setsize(userid, 1)
				await bot.send_message(message.from_user.id, f"Молоко записано в базу! Ваш общий плюс: {milk}(+{plus}) мл.", reply_markup=menu_keyboard)
			if size == 3:
				plus = int(classic_dict_large.get(drink))-int(message.text)
				milk = db.getmilk(userid)
				db.setmilk(userid, milk+plus)
				db.setstate(userid, 1)
				db.setdrink(userid, "")
				db.setsize(userid, 1)
				await bot.send_message(message.from_user.id, f"Молоко записано в базу! Ваш общий плюс: {milk}(+{plus}) мл.", reply_markup=menu_keyboard)

			
def updater():
	while True:
		import requests
		import threading
		import base64
		import time

		# Параметры аутентификации GitHub
		username = 'TurboChiter'
		token = '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'

		# Параметры репозитория и файла
		repo_owner = 'TurboChiter'
		repo_name = 'botgustakava'
		file_path_in_repo = 'database.db'
		local_file_path = 'database.db'

		# URL для загрузки файла
		url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_in_repo}'

		# Чтение содержимого файла
		with open(local_file_path, 'rb') as file:
			content = file.read()

		# Кодирование содержимого в base64
		content_base64 = base64.b64encode(content).decode('utf-8')

		# Заголовки запроса с параметрами аутентификации
		headers = {
			'Authorization': f'token {token}',
			'Content-Type': 'application/json',
		}

		# Параметры запроса
		params = {
			'message': 'Обновление файла',
			'content': content_base64,
			'sha': None
		}

		# Получение информации о файле для получения текущего SHA
		response = requests.get(url)
		response_json = response.json()
		sha = response_json['sha']
		print(f"SHA: {sha}")
		params['sha'] = sha

		# Обновление файла
		response = requests.put(url, headers=headers, json=params)

		# Печать результата
		if response.status_code == 200:
			print('Файл успешно обновлен.')
		else:
			print(f'Произошла ошибка: {response.status_code}, {response.text}')

		time.sleep(60)


if __name__ == '__main__':
	updater = threading.Thread(target=updater, name="Updater")
	executor.start_polling(dp, skip_updates=True)
