import telebot
import pyowm
import wikipedia

bot = telebot.TeleBot("950262531:AAFfQKfxpGa_XBPgqp7Ih0wuE9zczypQeAE")
owm = pyowm.OWM(API_key = 'ea10913f4eb6164d64ed6bab222667da',language='ru')
wikipedia.set_lang("ru")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название города, о'
    	+ ' котором ты хочешь что то узнать')

@bot.message_handler(content_types=['text'])
def City_Name(message):
	try:
		global Name
		Name = message.text
		observation = owm.weather_at_place(Name)
		w = observation.get_weather()
		bot.send_message(message.from_user.id, """Что тебе интересно в этом городе
			(Список действий: /help)""")
		bot.register_next_step_handler(message, Case_of_Move)
	except Exception:
		bot.send_message(message.from_user.id, """Я не знаю такого города. Выбери другой
			Или попробуй написать название на английском""")
		#bot.register_next_step_handler(message, City_Name)

def Case_of_Move(message):
	ch = message.text
	observation = owm.weather_at_place(Name)
	w = observation.get_weather()
	if ch == "/temper":
		t = w.get_temperature('celsius')['temp']
		bot.send_message(message.from_user.id, "Температура " + str(t) + "C")
		bot.send_message(message.from_user.id, tempr(t))
	elif ch == "/rain":
		rain_s = w.get_detailed_status()
		bot.send_message(message.from_user.id, rain_s)
		bot.send_message(message.from_user.id, rain_Level(rain_s))
		rain_s1 = w.get_status()
	elif ch =="/wind":
		wnd = w.get_wind()
		bot.send_message(message.from_user.id, wind_Level(wnd['speed']))
	elif ch =="/next":
		bot.send_message(message.from_user.id, "Выбери любой другой город")
		return
	elif ch == "/wiki":
		bot.send_message(message.from_user.id, wiki_inf())
	elif ch == "/help":
		bot.send_message(message.from_user.id, """В данный момент вы можете
			Получить данные о температуре (/temper)
			Получить данные о дожде (/rain)
			Получить данные о ветре (/wind)
			Получить краткое описание города (/wiki)
			Или же ты можешь сменить город (/next)""")
	else:
		bot.send_message(message.from_user.id, """Я тебя не понимаю
			Напиши комманду /help""")
	bot.register_next_step_handler(message, Case_of_Move)
def tempr(tem):
	if tem > 20:
		return "Погода хорошая. Надевай что хочешь"
	elif tem < 14:
		return "Немного прохладно, но не критично"
	else:
		return "Лучше одется потеплее"

def rain_Level(rn):
	S = ""
	if rn == "пасмурно":
		S = "Зонт не помешает, на всякий случай"
	elif "дождь" in rn:
		S = "Не забудь взять зонт"
	elif rn == "гроза":
		S = "Будь осторожен"	
	else:
		S = "Можно выдвигаться"
	return S
def wind_Level(wd):
	S = ""
	if wd < 2:
		S = "Практически штиль"
	elif wd < 7:
		S = "Немного ветренно"
	elif wd < 10:
		S = "Ветер довольно крепок"
	else:
		S = "Сильный ветер"
	return S
def wiki_inf():
	return wikipedia.summary(Name)
bot.polling(none_stop=True, interval=0)