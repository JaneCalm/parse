from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from pymongo import MongoClient
import time


class DB:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.mailru

    def parse_date(self, date):

        MONTHES = ['января', 'февраля', 'марта', 'апреля',
                   'мая', 'июня', 'июля', 'августа',
                   'сентября', 'октрября', 'ноября', 'декабря']
        if date.startswith('Сегодня') or date.startswith('Вчера'):
            if date.startswith('Сегодня'):
                pattern = 'Сегодня'
                d = datetime.now()
            else:
                pattern = 'Вчера'
                d = datetime.now() - timedelta(1)
            day = d.day
            month = MONTHES[d.month - 1]

            return date.replace(pattern, f'{day} {month}')

        return date

    def insert_data(self, content, href):
        sender = Wait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'letter-contact')))[0]
        item = {
            '_id': href,
            'sender': sender.get_attribute('title'),
            'title': Wait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'thread__subject')))[
                0].text,
            'date': self.parse_date(
                Wait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'letter__date')))[0].text)
        }
        print(item)
        self.db['emails'].update_one({'_id': item['_id']}, {'$set': item}, upsert=True)


chrome_options = Options()
chrome_options.add_argument('--headless')
#driver = webdriver.Chrome('./chromedriver')
driver = webdriver.Chrome('./chromedriver',options=chrome_options)
driver.get("https://mail.ru/?from=logout")
assert "почта" in driver.title
Login = 'study.ai_172@mail.ru'
Password = 'NewPassword172'
elem = Wait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'login')))
elem.send_keys(Login)
elem.send_keys(Keys.ENTER)
elem = Wait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password')))
elem.send_keys(Password)
elem.send_keys(Keys.ENTER)

email_urls = []
db = DB()
emails = Wait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'js-letter-list-item')))
new_btm_url = emails[0].get_attribute('href')
driver.get(new_btm_url)
email_urls.append(new_btm_url)
db.insert_data(driver, new_btm_url)

next_el = driver.find_elements_by_class_name('button2_ico-text-top')[-1]

while next_el:
    try:
        next_el.click()
        time.sleep(0.6)
        email_urls.append(driver.current_url)
        db.insert_data(driver, driver.current_url)
    except:
        break


print(f'Insert all : {len(email_urls)}')

driver.close()
