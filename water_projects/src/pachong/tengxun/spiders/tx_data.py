from datetime import datetime
import json
import re
import time
import scrapy
from typing import Iterable
from scrapy.http import Request
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from src.utils.Path import current_path

from selenium.webdriver.chrome.service import Service


from src.pachong.utils import create_chrome_driver
from src.pachong.tengxun.items import DataItem

def find_element_with_retry(web, by, value, max_retries=2):
    for _ in range(max_retries):
        try:
            element = web.find_element(by, value)
            return element
        except NoSuchElementException:
            print(f"未找到元素 {value}，重试...")
            time.sleep(1)
    raise NoSuchElementException(f"找不到元素 {value}，退出...")


def on_city_select(selected_city, output, headless):
    all_links = []
    web = create_chrome_driver(headless)
    url = "https://www.qq.com/"
    web.get(url=url)
    select_city = selected_city
    time.sleep(3)
    search_button = web.find_element(By.XPATH, "//*[@id='qqhome-top-header']/div/div/div[2]/div/input")
    search_button.send_keys(select_city)
    time.sleep(1)
    search_button.send_keys(Keys.ENTER)
    web.switch_to.window(web.window_handles[-1])
    for page in range(20):
        time.sleep(2)
        page_source = web.page_source
        # print(page_source)
        obj = re.compile(r'<li class="card-margin.*?<a href="(?P<url>.*?)" target="_blank"', re.S)
        # obj = re.compile(r'<li class="card-margin.*?<a href="(?P<url>.*?)" target="_blank2"', re.S)
        result = obj.finditer(page_source)
        links = [it.group("url") for it in result]
        print(f'--------正在获取{select_city}数据的第{page + 1}页----------')
        # print(links)
        all_links.extend(links)
        tag = 1
        try:
            next_page_button = find_element_with_retry(web, By.XPATH,
                                                       '//*[@id="root"]/div/div[1]/div[1]/div[2]/div/ul/li[12]/a/img')
            next_page_button.click()
        except NoSuchElementException:
            tag += 1
            print("未找到下一页按钮，退出...")
        if tag == 3:
            output(f"检索失败-warning-腾讯-服务器繁忙稍后重试")
            break
    if len(all_links) == 0:
        output(f"检索失败-error-腾讯-链接匹配失败")
    web.quit()
    return all_links

class TxDataSpider(scrapy.Spider):
    name = "tx_data"
    allowed_domains = ["www.qq.com"]
    
    Queue = None
    cityName = None
    startTime = None
    endTime = None
    headless = False

    def __init__(self, *args, **kwargs):
        super(TxDataSpider, self).__init__(*args, **kwargs)
        result = on_city_select(self.cityName, self.Queue.put, self.headless)
        # result = acquire_url()
        # self.Queue.put(result)
        self.start_urls = result

        # 修复 self.start_date 和 self.end_date 的初始化
        self.start_date = datetime.strptime(self.startTime, '%Y-%m-%d %H:%M:%S')
        self.end_date = datetime.strptime(self.endTime, '%Y-%m-%d %H:%M:%S')
        # self.start_date = datetime.strptime(result[1][0].strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        # self.end_date = datetime.strptime(result[2][0].strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

        # self.Queue.put(str(self.start_date))
        # self.Queue.put(str(self.end_date))

    def is_date_in_range(self, date, start_date, end_date):
        return start_date <= date <= end_date
    
    def start_requests(self) -> Iterable[Request]:
        self.Queue.put('开始采集 腾讯 渠道')
        return super().start_requests()
    
    def close(spider, reason):
        spider.Queue.put('腾讯 渠道采集结束')

    def parse(self, response):
        data_item = DataItem()
        # print(response.text)
        obj = re.compile(r'"pubtime":"(?P<date>.*?)","comment_id"', re.S)
        result = obj.search(response.text)
        # self.Queue.put(result)
        if result:
            raw_date = result.group("date")
            if raw_date:
                if len(raw_date) > 0:
                    # 在调用 datetime.strptime 时移除 [0]
                    parsed_date = datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S')

                    if self.is_date_in_range(parsed_date, self.start_date, self.end_date):
                        data_item['date'] = parsed_date.strftime('%Y-%m-%d %H:%M:%S')

                        pattern = re.compile(r'window\.DATA\s*=\s*({.*?});', re.DOTALL)
                        match = pattern.search(response.text)
                        if match:
                            # 匹配到 JSON 数据字符串
                            json_data = match.group(1)
                            # 解析 JSON 数据
                            data_dict = json.loads(json_data)
                            # 提取其中的文字信息
                            content_list = data_dict.get('content', [])
                            if content_list is not None:
                                processed_values = []
                                for item in content_list:
                                    if item['type'] == 1:
                                        processed_value = item.get('value')
                                        if processed_value and processed_value.strip():
                                            cleaned_text = re.sub(r'<[^>]*>', '', processed_value)
                                            cleaned_text_lines = [line.strip() for line in cleaned_text.split('\n') if line.strip()]
                                            processed_value = ''.join(cleaned_text_lines)
                                            # print(processed_value)
                                            if "雨" in processed_value and "积水" in processed_value:
                                                processed_values.append(processed_value)
                                data_item['data'] = processed_values
                                if data_item['data']:
                                    # print(data_item['data'])
                                    # print(data_item['date'])
                                    # print("\n")
                                    self.Queue.put(data_item['date'] + ' ' + data_item['data'])
                                    yield data_item
                            else:
                                obj2 = re.compile(r' window.DATA.*?"title":"(?P<data>.*?)","iNewsRecommendLevel"', re.S)
                                result1 = obj2.finditer(response.text)
                                for it in result1:
                                    data = it.group("data")
                                    # print(data)
                                    if "雨" in data and "积水" in data:
                                        data_item['data'] = data
                                        # print(data_item['data'])
                                        # print(data_item['date'])
                                        # print("\n")
                                        self.Queue.put(data_item['date'] + ' ' + data_item['data'])
                                        yield data_item

