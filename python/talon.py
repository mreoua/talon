import requests
from datetime import datetime, timedelta
import time
import random

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7ImlubiI6IjI4MjM2MTg3MzMiLCJwaG9uZSI6IiIsImVtYWlsIjoiIiwiZ2l2ZW5uYW1lIjoi0JLQntCb0J7QlNCY0JzQmNCgIiwibWlkZGxlbmFtZSI6ItCb0JXQntCd0IbQlNCe0JLQmNCnIiwibGFzdG5hbWUiOiLQn9Ce0J_QntCSIiwib3JnYW5pemF0aW9uIjoi0KTQhtCX0JjQp9Cd0JAg0J7QodCe0JHQkCIsImVkcnBvdSI6IiJ9LCJleHAiOjE3NDU4MzAyOTcuMTI5LCJpYXQiOjE3NDU4MjMwOTd9.sfZ94t1JdfuIburgRrYuHeT6hVEYKvoSU0IbnccGc7r3-YfMLnPSa9yLKtdOMqxrsg3Wp8P3Fqyk5lit37UlKBHeQanQmPbHw5JCFWslogafb05Uo1h_ZxiopauUcMQiBJRTZCvryFR3C8637dAAHrdfn_CiV4EZLL_VxHuMmLfyghLIh1BqYaKYEZ2pSHFSXXDzd9NpZF5G4Y4sf0loymQhuVYEGG-XWRgAf_mSpiMdZkaye-xzq3h7_nyPl0oZKNQ3LK7RDfpY1Sfs_1bEFk2Pu3rlCZtqLKBSiezsd9hjzZxalZwuxOEggo5218t9AqbocMlKIj_oY0V86P8SNQ; bm_mi=E3B214C0523E529002FDE17470ADD23F~YAAQn2ReaJmbsHSWAQAAeWQqext3tumc5mLQKO3UMHyuvONIJ6u+A3W5nxZ/VI1+zkA2/sLRb6sverpUR/rhxN27h2AHsi3fhpgfp8vgn97yOC42uKMC22shKsi3F+d7duNihf2ULkisdSCrpbwT466n2G0f6RunZeJMQEByKgmaHP3lSxC2JUpP0uyyq4X0rlVZ/Zm37WgZEdIhIv9arpYliW5BvMKB/XfVJbOtRA/ZPjwBqGaPVjmUDMHr3NmMnwCAipNBAtWrgI27PKQY2YZ0nne/YabuXgUYwDnNVrUS6yyyv6UvmBVpkjj++JwXEOGY7YM=~1'


def sendToTelegram(text):
	print(text)
	url = 'https://api.telegram.org/bot165301541:AAEZJhUNLx1KXJWts3McIpkgJpQaho8kxfo/sendMessage?chat_id=156531024&text=%s' % (text)
	requests.get(url)

def sendToMreo(date, token):
	url = 'https://eqn.hsc.gov.ua/api/v2/departments'

	params = {
		'serviceId': '49',
		'date': date
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
		'__Secure-next-auth.session-token': token
	}

	response = requests.get(url, params=params, headers=headers, cookies=cookies)

	return response

def checkTalon(data, date):
	servCentre = 'ТСЦ МВС № 8049'
	for d in data:
		if d.get('srvCenterName') == servCentre:
			return date

	return False

def getNext20Days(start_date=None):
	# Если начальная дата не указана, используем текущую
	if start_date is None:
		start_date = datetime.now()
	
	# Создаем список для хранения дат
	date_list = []
	
	# Генерируем даты для следующих 20 дней (включая текущий день)
	for i in range(12):
		current_date = start_date + timedelta(days=i)
		weekday = current_date.weekday()
		if weekday != 0 and weekday != 6:
			formatted_date = current_date.strftime('%Y-%m-%d')
			date_list.append(formatted_date)
	first = date_list[0]
	last = date_list[-1]
	
	random.shuffle(date_list)
	
	return date_list, first, last

def test():
	print(getNext20Days())
	sendToTelegram('pop')


def main():
	
	dates, first, last = getNext20Days()
	print('%s - %s' % (first, last))
	while True:
		for date in dates:
			res = sendToMreo(date, token)

			if res.status_code == 429:
				print('retry request')
				time.sleep(10)
				res = sendToMreo(date, token)

			if res.status_code == 440:
				sendToTelegram('mreo: must reauth')
				return

			if res.status_code != 200:
				sendToTelegram('mreo some error code - %s' % (res.status_code))
				time.sleep(60)
			elif d := checkTalon(res.json(), date):
				sendToTelegram('mreo: have talon on %s' % (d))

			print('%s - %s' % (date, len(res.json())))

			time.sleep(random.randint(4, 9))
		print('---')
		time.sleep(60)

if __name__ == '__main__':
	main()