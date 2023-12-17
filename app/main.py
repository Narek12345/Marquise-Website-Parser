from fastapi import FastAPI

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests, json, time, re


app = FastAPI()


@app.get('/marquise_website_parser')
def marquise_website_parser(sites: str):
	"""Принимает список сайтов и парсим в каждом сайте номер телефона и код чатов."""
	driver = webdriver.Chrome()
	sites = eval(sites)
	list_phone_numbers = []

	# Итерируемся по списку сайтов.
	for site in sites:
		driver.get(site)
		time.sleep(3)
		wait = WebDriverWait(driver, 10)

		page_text = driver.page_source.replace(' ', '')

		try:
			find_jivo_chat_by_class_name = driver.find_element(By.CLASS_NAME, "hoverl_a149")
		except:
			find_jivo_chat_by_class_name = None

		try:
			find_jivo_chat_by_tag_name = driver.find_element(By.TAG_NAME, 'jdiv')
		except:
			find_jivo_chat_by_tag_name = None

		try:
			phone_element_by_div = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="start"]/div/div[3]/div[2]/div[1]/div[1]')))
			phone_number_by_div = phone_element_by_div.text
		except Exception as e:
			phone_number_by_div = None

		try:
			phone_element_by_a = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="start-page__phone start-page__phone_clickable"]')))
			phone_number_by_a = phone_element_by_a.text
		except:
			phone_number_by_a = None		

		if find_jivo_chat_by_class_name or find_jivo_chat_by_tag_name:
			if phone_number_by_a:
				list_phone_numbers.append({site: ([phone_number_by_a], 'Да')})
			elif phone_number_by_div:
				list_phone_numbers.append({site: ([phone_number_by_div], 'Да')})
		else:
			if phone_number_by_a:
				list_phone_numbers.append({site: ([phone_number_by_a], 'Нет')})
			elif phone_number_by_div:
				list_phone_numbers.append({site: ([phone_number_by_div], 'Нет')})
			

	driver.quit()

	return list_phone_numbers


# <jdiv class="hoverl_a149"><jdiv class="omnichannel_c7e7 bottom_fbd9"></jdiv></jdiv>


		# try:
		# 	phone_element_by_div = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="start"]/div/div[3]/div[2]/div[1]/div[1]')))
		# 	phone_number_by_div = phone_element_by_div.text
		# except Exception as e:
		# 	phone_number_by_div = None

		# try:
		# 	phone_element_by_a = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="start-page__phone start-page__phone_clickable"]')))
		# 	phone_number_by_a = phone_element_by_a.text
		# except:
		# 	phone_number_by_a = None



# phone_number_match = re.search(r'\+7[0-9\s-]+', page_text)
# 		if phone_number_match:
# 			phone_number_ = phone_number_match.group()
# 		else:
# 			phone_number_ = None

# 		try:
# 			phone_number_match = re.search(r'\+9[0-9\s-]+', page_text)
# 			if phone_number_match:
# 				phone_number = phone_number_match.group()
# 			else:
# 				phone_number = None
# 		except:
# 			pass