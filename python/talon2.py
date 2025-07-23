import requests
from datetime import datetime, timedelta
import time
import random

def getToken():
	with open('token.txt') as f:
		cookies = f.read().split('; ')
		print(cookies)
		for cookie in cookies:
			if cookie.startswith('__Secure-auth.access-token='):
				return cookie.split('=', 1)[1]

def sendToTelegram(text, only_print = False):
	print(text)
	url = 'https://api.telegram.org/bot165301541:AAEZJhUNLx1KXJWts3McIpkgJpQaho8kxfo/sendMessage?chat_id=156531024&text=%s' % (text)
	if only_print == False:
		requests.get(url)

def getNext20Days(start=None, stop_date=1):
	
	if start is None:
		start_date = datetime.now()
	else:
		start_date = datetime.strptime(start, "%Y-%m-%d")
	# Создаем список для хранения дат
	date_list = []

	# Генерируем даты для следующих 20 дней (включая текущий день)
	for i in range(stop_date):
		current_date = start_date + timedelta(days=i)
		weekday = current_date.weekday()
		if weekday != 0 and weekday != 6:
			formatted_date = current_date.strftime('%Y-%m-%d')
			date_list.append(formatted_date)
	
	return date_list

def sendToMreo(token):
	url = 'https://eqn.hsc.gov.ua/api/v2/equeue/days' 

	params = {
		'serviceId': '49',
		'departmentId': '154'
		# 'departmentId': '35'
	}


	headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,uk;q=0.5',
		'cache-control': 'no-cache',
		'pragma': 'no-cache',
		'priority': 'u=0, i',
		'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Linux"',
		'sec-fetch-dest': 'document',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'none',
		'sec-fetch-user': '?1',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
	}

	cookies = {
		'__Secure-auth.access-token': token
	}

	response = requests.get(url, params=params, headers=headers, cookies=cookies)

	return response

def checkTalon(data, dates):
	data_dates = {d['date'][:10] for d in data['data']}
	return any(date in data_dates for date in dates), [date for date in dates if date in data_dates]

def haveTalon(dates):
	for i in range(3):
		sendToTelegram('mreo: have talon on %s' % (', '.join(dates)))
		time.sleep(20)

def main():
	sum_sleep = 0
	token = getToken()
	dates = getNext20Days('2025-07-18', 1)
	print('%s - %s' % (dates[0], dates[-1]))

	while True:
		res = sendToMreo(token)

		if res.status_code == 429:
			print('retry request')
			time.sleep(10)
			res = sendToMreo(token)

		if res.status_code == 401:
			sendToTelegram('mreo: must reauth')
			return

		if res.status_code != 200:
			if res.status_code != 424:
				sendToTelegram('mreo some error code - %s' % (res.status_code), True)
			time.sleep(60)
		else:
			ch, ch_dates = checkTalon(res.json(), dates)
			if ch:
				haveTalon(ch_dates)
				time.sleep(120)

		_sleep = 27 + random.randint(1, 9)
		sum_sleep += _sleep
		print('---  %s' % (sum_sleep))
		time.sleep(_sleep)

if __name__ == '__main__':
	main()