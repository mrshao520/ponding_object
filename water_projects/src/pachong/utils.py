import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


from src.utils.Path import current_path


def create_chrome_driver2(headless = False):
    webdriver_path = current_path + '/resources/chromedriver.exe'
    opt = Options()
    if headless:
        opt.add_argument("--headless")
        opt.add_argument("--disable-gpu")
    opt.add_argument('--disable-blink-features=AutomationControlled')
    web = webdriver.Chrome(service=Service(webdriver_path), options=opt)
    return web

def create_chrome_driver(headless = False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    webdriver_path = current_path + '/resources/chromedriver.exe'
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(service=Service(webdriver_path), options=options)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => false})'})
    browser.implicitly_wait(5)
    return browser

def add_cookies(browser, cookie_file):
    with open(cookie_file, 'r') as file:
        cookies_list = json.load(file)
        for cookies_dict in cookies_list:
            if cookies_dict['secure']:
                browser.add_cookie(cookies_dict)