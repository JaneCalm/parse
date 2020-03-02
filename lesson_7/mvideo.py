from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time


class DB:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.mvideo

    def get_attr(self, item, css_class):
        try:
            text = item.find_element_by_class_name(css_class).text
            if not text or text == '':
                return None
        except:
            return None
        return int(''.join(filter(lambda x:x.isdigit(), text)))

    def insert_data(self, items):
        goods = items.find_elements_by_class_name('gallery-list-item')
        for good in goods:
            sets = good.find_element_by_class_name('sel-product-tile-title').get_attribute('data-product-info')
            sets = eval(sets)
            title = good.find_element_by_class_name('sel-product-tile-title').text
            if title:
                item = {
                    '_id': good.find_element_by_class_name('sel-product-tile-title').get_attribute('href'),
                    'title': title,
                    'price': self.get_attr(good, 'c-pdp-price__current'),
                    'discount': self.get_attr(good, 'c-pdp-price__trade-price'),
                    'monthly': self.get_attr(good, 'c-pdp-price__monthly'),
                    'sets': sets
                }
                print(item)
                self.db['hit'].update_one({'_id': item['_id']},{'$set': item}, upsert=True)


chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver',options=chrome_options)
driver.get("https://www.mvideo.ru/")

carousel = driver.find_element_by_xpath("//*[@data-init='gtm-push-products']")
ActionChains(driver).move_to_element(carousel).perform()
next_btn = driver.find_element_by_xpath("//*[@data-init='gtm-push-products'][1]//a[contains(@class, 'sel-hits-button-next')]")
db = DB()
db.insert_data(carousel)
while next_btn.is_displayed():
    next_btn.click()
    time.sleep(5)
    db.insert_data(carousel)

driver.quit()
