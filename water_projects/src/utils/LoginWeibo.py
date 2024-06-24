import time
import json
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.utils.Path import current_path


def create_chrome_driver(*, headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    webdriver_path = current_path + '/resources/chromedriver.exe'
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(service=Service(webdriver_path), options=options)
    # browser.set_window_size(1600, 1000)
    # browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undfined})'})
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => false
        })
      """
    })

    return browser

def login_weibo():
    browser = create_chrome_driver(headless=False)

    browser.get('https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F')

    browser.implicitly_wait(15)
    log_in_button = browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/div[1]/div[2]/div/button').click()
    time.sleep(2)
    WebDriverWait(browser, 100).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[1]/div[1]/div[2]/div/button')))
    with open(current_path + '/documents/weibo.json', 'w') as file:
        json.dump(browser.get_cookies(), file)
    print('cookies 已保存')
    browser.quit()
