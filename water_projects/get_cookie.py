import json
import time

from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def create_chrome_driver(*, headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    webdriver_path = 'D:/code/python/water_projects/resources/chromedriver.exe'
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(service=Service(webdriver_path), options=options)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => false})'})
    browser.implicitly_wait(5)
    return browser

# browser = create_chrome_driver(headless=False)
# browser.get('https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F')

# browser.implicitly_wait(15)
# time.sleep(20)
# with open(r'D:\code\python\water_projects\documents\weibo.json', 'w')as file:
#     json.dump(browser.get_cookies(), file)

browser = create_chrome_driver(headless=False)

browser.get('https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F')

browser.implicitly_wait(15)
log_in_button = browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/div[1]/div[2]/div/button').click()
time.sleep(2)
WebDriverWait(browser, 100).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[1]/div[1]/div[2]/div/button')))
with open('weibo/spiders/weibo.json', 'w')as file:
    json.dump(browser.get_cookies(), file)
print('cookies 已保存')
browser.quit()