import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
from time import strftime, sleep # для времени

# парсинг
import requests as req
from bs4 import BeautifulSoup as BS

V = 0.2

r_version = req.get('https://information-app.000webhostapp.com/')
html_version = BS(r_version.content, 'html.parser')

version = float(html_version.select('.latest-version')[0].text)

if version == V:
	pass

else:
	pass

def remove_spaces(your_string):
    # удалить все пробелы из строки
    result = ''.join(your_string.split())
    return result


def get_nums(your_string):
    # получить только числа из строки до +
    nums = '0123456789'
    my_list = []

    for i in your_string:
        if i in nums:
            my_list.append(i)

        if i == '+':
            break

    return "".join(map(str, my_list))


headers = {
    # хэдеры для парсинга
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
	def __init__(self):
		# Это здесь нужно для доступа к переменным, методам
		# и т.д. в файле design.py
		super(App, self).__init__()
		self.ui = design.Ui_MainWindow()
		self.ui.setupUi(self)

		# первоначально задаем время
		self.time_now = strftime('%H:%M')
		self.ui.time.setText(self.time_now)

		# задаем температуру
		r_weather_foreca = req.get('https://www.foreca.ru/Russia/Blagoveshchensk')
		html_weather_foreca = BS(r_weather_foreca.content, 'html.parser')
		temp_now = remove_spaces(html_weather_foreca.select('.left > .txt-xxlarge')[0].text)
		self.ui.now_temp.setText(temp_now)

		# делаем апдейт времени
		self.ui.weather_today.clicked.connect(self.update_time)
		self.ui.weather_tomorrow.clicked.connect(self.update_time)
		self.ui.weather_after_tomorrow.clicked.connect(self.update_time)
		self.ui.in_rus.clicked.connect(self.update_time)
		self.ui.in_amur.clicked.connect(self.update_time)
		self.ui.in_world.clicked.connect(self.update_time)

		# отслеживаем нажатия кнопок
		self.ui.weather_today.clicked.connect(self.show_weather_today)
		self.ui.weather_tomorrow.clicked.connect(self.show_weather_tomorrow)
		self.ui.weather_after_tomorrow.clicked.connect(self.show_weather_day_after_tomorrow)
		self.ui.in_rus.clicked.connect(self.show_corona_stats_rus)
		self.ui.in_amur.clicked.connect(self.show_corona_stats_amur)
		self.ui.in_world.clicked.connect(self.show_stats_world)
		self.ui.course_money.clicked.connect(self.show_money_course)


	def update_time(self):
		# функция апдейта времени
		self.time_now = strftime('%H:%M')
		self.ui.time.setText(self.time_now)


	def show_weather_today(self):
		# показать погоду на сегодня
		r_weather = req.get('https://www.accuweather.com/ru/ru/blagoveshchensk/286867/daily-weather-forecast/286867', headers=headers)
		html_weather = BS(r_weather.content, 'html.parser')

		r_weather_foreca = req.get('https://www.foreca.ru/Russia/Blagoveshchensk')
		html_weather_foreca = BS(r_weather_foreca.content, 'html.parser')

		today_temps = remove_spaces(html_weather.select('.temps > .high')[0].text) + remove_spaces(html_weather.select('.temps > .low')[0].text)
		today_status = (html_weather.select('.phrase')[0].text).strip()
		today_rain_prob = remove_spaces(html_weather.select('.precip > p')[1].text)

		today_humidity = html_weather_foreca.select('.txt-tight > strong')[3].text

		r_weather_foreca_2 = req.get('https://www.foreca.ru/Russia/Blagoveshchensk?tenday&quick_units=metric')
		html_weather_foreca_2 = BS(r_weather_foreca_2.content, 'html.parser')

		wind_speed_today = html_weather_foreca_2.select('.cell > span > span > strong')[0].text + ' м/с'
		
		self.ui.temps_value.setText(today_temps)
		self.ui.status_value.setText(today_status)
		self.ui.wind_speed_value.setText(wind_speed_today)
		self.ui.rain_prob_value.setText(today_rain_prob)
		self.ui.humidity_value.setText(today_humidity)
		self.ui.status.setText('Сегодня')


	def show_weather_tomorrow(self):
		# показать погоду на завтра
		r_weather = req.get('https://www.accuweather.com/ru/ru/blagoveshchensk/286867/daily-weather-forecast/286867', headers=headers)
		html_weather = BS(r_weather.content, 'html.parser')

		r_weather_foreca = req.get('https://www.foreca.ru/Russia/Blagoveshchensk')
		html_weather_foreca = BS(r_weather_foreca.content, 'html.parser')

		tomorrow_temps = remove_spaces(html_weather.select('.temps > .high')[1].text) + remove_spaces(html_weather.select('.temps > .low')[1].text)
		tomorrow_status = (html_weather.select('.phrase')[1].text).strip()
		tomorrow_rain_prob = remove_spaces(html_weather.select('.precip > p')[3].text)

		r_weather_foreca_2 = req.get('https://www.foreca.ru/Russia/Blagoveshchensk?tenday&quick_units=metric')
		html_weather_foreca_2 = BS(r_weather_foreca_2.content, 'html.parser')

		wind_speed_tomorrow = html_weather_foreca_2.select('.cell > span > span > strong')[1].text + ' м/с'

		self.ui.temps_value.setText(tomorrow_temps)
		self.ui.status_value.setText(tomorrow_status)
		self.ui.wind_speed_value.setText(wind_speed_tomorrow)
		self.ui.rain_prob_value.setText(tomorrow_rain_prob)
		self.ui.humidity_value.setText('Нет данных')
		self.ui.status.setText('Завтра')


	def show_weather_day_after_tomorrow(self):
		# показать погоду на послезавтра
		r_weather = req.get('https://www.accuweather.com/ru/ru/blagoveshchensk/286867/daily-weather-forecast/286867', headers=headers)
		html_weather = BS(r_weather.content, 'html.parser')

		r_weather_foreca = req.get('https://www.foreca.ru/Russia/Blagoveshchensk')
		html_weather_foreca = BS(r_weather_foreca.content, 'html.parser')

		day_after_tomorrow_temps = remove_spaces(html_weather.select('.temps > .high')[2].text) + remove_spaces(html_weather.select('.temps > .low')[2].text)
		day_after_tomorrow_status = (html_weather.select('.phrase')[2].text).strip()
		day_after_tomorrow_rain_prob = remove_spaces(html_weather.select('.precip > p')[5].text)

		r_weather_foreca_2 = req.get('https://www.foreca.ru/Russia/Blagoveshchensk?tenday&quick_units=metric')
		html_weather_foreca_2 = BS(r_weather_foreca_2.content, 'html.parser')

		wind_speed_day_after_tomorrow = html_weather_foreca_2.select('.cell > span > span > strong')[2].text + ' м/с'

		self.ui.temps_value.setText(day_after_tomorrow_temps)
		self.ui.status_value.setText(day_after_tomorrow_status)
		self.ui.wind_speed_value.setText(wind_speed_day_after_tomorrow)
		self.ui.rain_prob_value.setText(day_after_tomorrow_rain_prob)
		self.ui.humidity_value.setText('Нет данных')
		self.ui.status.setText('Послезавтра')


	def show_corona_stats_rus(self):
		# показать статистику по короне рус
		r_corona_rus = req.get('https://coronavirus-monitor.info/country/russia/')
		html_corona_rus  = BS(r_corona_rus.content, 'html.parser')

		sick_rus = get_nums(html_corona_rus.select('.confirmed > h2')[0].text)
		recovered_rus = get_nums(html_corona_rus.select('.cured > h2')[0].text)
		dead_rus = get_nums(html_corona_rus.select('.deaths > h2')[0].text)

		try:
			sick_rus_change = html_corona_rus.select('.confirmed > h2 > sup')[0].text
			recovered_rus_change = html_corona_rus.select('.cured > h2 > sup')[0].text
			dead_rus_change = html_corona_rus.select('.deaths > h2 > sup')[0].text

			self.ui.sick_value.setText('{0} ({1})'.format(sick_rus, sick_rus_change))
			self.ui.recovered_value.setText('{0} ({1})'.format(recovered_rus, recovered_rus_change))
			self.ui.dead_value.setText('{0} ({1})'.format(dead_rus, dead_rus_change))

		except:
			self.ui.sick_value.setText('{0}'.format(sick_rus))
			self.ui.recovered_value.setText('{0}'.format(recovered_rus))
			self.ui.dead_value.setText('{0}'.format(dead_rus))


	def show_corona_stats_amur(self):
		# показать статистику по короне амур
		r_corona_amur = req.get('https://coronavirus-monitor.info/country/russia/amurskaya-oblast/')
		html_corona_amur = BS(r_corona_amur.content, 'html.parser')

		sick_amur = get_nums(html_corona_amur.select('.confirmed > h2')[0].text)
		recovered_amur = get_nums(html_corona_amur.select('.cured > h2')[0].text)   
		dead_amur = get_nums(html_corona_amur.select('.deaths > h2')[0].text)


		try:
			sick_amur_change = html_corona_amur.select('.confirmed > h2 > sup')[0].text
			recovered_amur_change = html_corona_amur.select('.cured > h2 > sup')[0].text
			dead_amur_change = html_corona_amur.select('.deaths > h2 > sup')[0].text

			self.ui.sick_value.setText('{0} ({1})'.format(sick_amur, sick_amur_change))
			self.ui.recovered_value.setText('{0} ({1})'.format(recovered_amur, recovered_amur_change))
			self.ui.dead_value.setText('{0} ({1})'.format(dead_amur, dead_amur_change))

		except:
			self.ui.sick_value.setText('{0}'.format(sick_amur))
			self.ui.recovered_value.setText('{0}'.format(recovered_amur))
			self.ui.dead_value.setText('{0}'.format(dead_amur))


	def show_stats_world(self):
		# показать статистику по короне в мире
		r_corona_world = req.get('https://coronavirus-monitor.info')
		html_corona_world = BS(r_corona_world.content, 'html.parser')

		sick_world = get_nums(html_corona_world.select('.confirmed > h2')[0].text)
		recovered_world = get_nums(html_corona_world.select('.cured > h2')[0].text)
		dead_world = get_nums(html_corona_world.select('.deaths > h2')[0].text)

		try:
			sick_world_change = html_corona_world.select('.confirmed > h2 > sup')[0].text
			recovered_world_change = html_corona_world.select('.cured > h2 > sup')[0].text
			dead_world_change = html_corona_world.select('.deaths > h2 > sup')[0].text

			self.ui.sick_value.setText('{0} ({1})'.format(sick_world, sick_world_change))
			self.ui.recovered_value.setText('{0} ({1})'.format(recovered_world, recovered_world_change))
			self.ui.dead_value.setText('{0} ({1})'.format(dead_world, dead_world_change))

		except:
			self.ui.sick_value.setText('{0}'.format(sick_world))
			self.ui.recovered_value.setText('{0}'.format(recovered_world))
			self.ui.dead_value.setText('{0}'.format(dead_world))


	def show_money_course(self):
		# показать курсы валют
		r_money = req.get('https://yandex.ru', headers = headers)
		html_money = BS(r_money.content, 'html.parser')

		r_money_cny = req.get('https://yandex.ru/news/quotes/10018.html', headers = headers)
		html_money_cny = BS(r_money_cny.content, 'html.parser')

		yuan = html_money_cny.select('.quote__day > .quote__value')[0].text
		yuan_change = html_money_cny.select('.quote__day > .quote__change')[0].text

		usd = html_money.select('.inline-stocks__value_inner')[0].text
		usd_change = html_money.select('.inline-stocks__cell_change_small')[0].text

		eur = html_money.select('.inline-stocks__value_inner')[1].text
		eur_change = html_money.select('.inline-stocks__cell_change_small')[1].text

		oil = html_money.select('.inline-stocks__value_inner')[2].text

		try:
			oil_change = html_money.select('.inline-stocks__cell_change_small')[2].text

		except:
			oil_change = html_money.select('.a11y-hidden')[2].text


		# в зависимости от изменения курса валют применяем определенный цвет css
		if '+' in usd_change:
			self.ui.dollar_value.setStyleSheet('color: red;')
			self.ui.dollar_value_change.setStyleSheet('color: red;')
			self.ui.dollar_value.setText(usd)
			self.ui.dollar_value_change.setText(usd_change)

		else:
			self.ui.dollar_value.setStyleSheet('color: green;')
			self.ui.dollar_value_change.setStyleSheet('color: green;')
			self.ui.dollar_value.setText(usd)
			self.ui.dollar_value_change.setText(usd_change)

		if '+' in eur_change:
			self.ui.eur_value.setStyleSheet('color: red;')
			self.ui.eur_value_change.setStyleSheet('color: red;')
			self.ui.eur_value.setText(eur)
			self.ui.eur_value_change.setText(eur_change)

		else:
			self.ui.eur_value.setStyleSheet('color: green;')
			self.ui.eur_value_change.setStyleSheet('color: green;')
			self.ui.eur_value.setText(eur)
			self.ui.eur_value_change.setText(eur_change)

		if '-' in oil_change:
			self.ui.oil_value.setStyleSheet('color: red;')
			self.ui.oil_value_change.setStyleSheet('color: red;')
			self.ui.oil_value.setText(oil)
			self.ui.oil_value_change.setText(oil_change)

		else:
			self.ui.oil_value.setStyleSheet('color: green;')
			self.ui.oil_value_change.setStyleSheet('color: green;')
			self.ui.oil_value.setText(oil)
			self.ui.oil_value_change.setText(oil_change)

		if '-' in yuan_change:
			self.ui.yuan_value.setStyleSheet('color: green;')
			self.ui.yuan_value_change.setStyleSheet('color: green;')
			self.ui.yuan_value.setText(yuan)
			self.ui.yuan_value_change.setText(yuan_change)

		else:
			self.ui.yuan_value.setStyleSheet('color: red;')
			self.ui.yuan_value_change.setStyleSheet('color: red;')
			self.ui.yuan_value.setText(yuan)
			self.ui.yuan_value_change.setText('+' + yuan_change)


def main():
	app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	window = App()  # Создаём объект класса ExampleApp
	window.setFixedSize(800, 590) # чтобы нельзя было изменять окно
	window.show()  # Показываем окно
	app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	main()  # то запускаем функцию main()

