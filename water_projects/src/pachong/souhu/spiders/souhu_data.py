import time
from typing import Iterable
import scrapy
from lxml import html
from scrapy.http import Request
from datetime import datetime
from bs4 import BeautifulSoup

from src.pachong.utils import create_chrome_driver
from src.pachong.souhu.items import SouhuItem

start_data = [
        {"id": "北京积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E5%8C%97%E4%BA%AC%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700806918549uAQjrPb_1467"},
        {"id": "上海积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E4%B8%8A%E6%B5%B7%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "南京积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E5%8D%97%E4%BA%AC%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "深圳积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E6%B7%B1%E5%9C%B3%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "重庆积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E9%87%8D%E5%BA%86%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "武汉积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E6%AD%A6%E6%B1%89%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "杭州积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E6%9D%AD%E5%B7%9E%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "西安积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E8%A5%BF%E5%AE%89%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "郑州积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E9%83%91%E5%B7%9E%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "广州积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E5%B9%BF%E5%B7%9E%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "东莞积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E4%B8%9C%E8%8E%9E%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "成都积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E6%88%90%E9%83%BD%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "天津积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E5%A4%A9%E6%B4%A5%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "济南积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E6%B5%8E%E5%8D%97%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"},
        {"id": "合肥积水点",
         "url": "https://search.sohu.com/?queryType=outside&keyword=%E5%90%88%E8%82%A5%E7%A7%AF%E6%B0%B4%E7%82%B9&spm=smpc.home.0.0.1700996096681bi2jPfJ_1467"}
    ]


def on_city_select(selected_city, output, headless):
    all_links = []
    selected_url = next((data["url"] for data in start_data if data["id"] == selected_city), None)
    if selected_url:
        browser = create_chrome_driver(headless)
        print(f'---------------正在获取{selected_city}数据-------------------')
        browser.get(url=selected_url)
        time.sleep(2)
        scroll_pause_time = 2
        last_height = browser.execute_script("return document.body.scrollHeight;")
        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = browser.execute_script("return document.body.scrollHeight;")
            if new_height == last_height:
                break
            last_height = new_height
        response = browser.page_source
        # 使用Beautiful Soup解析页面源代码
        soup = BeautifulSoup(response, 'html.parser')
        # 通过Beautiful Soup选择器选择元素
        try:
            link_elements = soup.select('#news-list div div div:nth-child(2) div a, #news-list div div h4 a')
            # link_elements = soup.select('#news-list div div div:nth-child() div a, #news-list div div h4 b')
            # 提取链接并添加到全局变量
            for link_element in link_elements:
                link_href = link_element.get('href')
                print(link_href)
                all_links.append(link_href)
        except:
            output(f"检索失败-error-搜狐-链接匹配失败")
        browser.quit()
    return all_links

class SouhuDataSpider(scrapy.Spider):
    name = "souhu_data"
    allowed_domains = ["souhu.com"]
    
    Queue = None
    cityName = None
    startTime = None
    endTime = None
    headless = False

    def __init__(self, *args, **kwargs):
        super(SouhuDataSpider, self).__init__(*args, **kwargs)

        
        result = on_city_select(self.cityName, self.Queue.put, self.headless)
        # result = acquire_url()
        # self.Queue.put(result)
        self.start_urls = result

        # 修复 self.start_date 和 self.end_date 的初始化
        self.start_date = datetime.strptime(self.startTime, '%Y-%m-%d %H:%M:%S')
        self.end_date = datetime.strptime(self.endTime, '%Y-%m-%d %H:%M:%S')


    def is_date_in_range(self, date, start_date, end_date):
        return start_date <= date <= end_date

    def start_requests(self) -> Iterable[Request]:
        self.Queue.put('开始采集 搜狐 渠道')
        return super().start_requests()
    
    def close(spider, reason):
        spider.Queue.put('搜狐 渠道采集结束')
        
    def parse(self, response):
        page_source = response.text
        # self.Queue.put(page_source)
        tree = html.fromstring(page_source)
        raw_date = tree.xpath('//*[@id="news-time"]/text()')
        if raw_date:
            if len(raw_date) > 0:
                # 清理日期字符串，去除前导和尾随的空格和换行符
                cleaned_date = raw_date[0].strip()
                try:
                    parsed_date = datetime.strptime(cleaned_date, '%Y-%m-%d %H:%M')
                    if self.is_date_in_range(parsed_date, self.start_date, self.end_date):
                        paragraphs = tree.xpath('//div[@class="text"]/article[@class="article"]/p/text()')
                        full_paragraph = '\n'.join(paragraph.strip() for paragraph in paragraphs)
                        if "积水" in full_paragraph and "雨" in full_paragraph:
                            full_paragraph = full_paragraph.replace("\n", "")
                        
                        # print(full_paragraph)
                        # print(parsed_date.strftime('%Y-%m-%d %H:%M'))
                            self.Queue.put(parsed_date.strftime('%Y-%m-%d %H:%M:%S') + ' ' +full_paragraph)

                            data_item = SouhuItem()
                            data_item['data'] = full_paragraph
                            data_item['date'] = parsed_date.strftime('%Y-%m-%d %H:%M:%S')

                            yield data_item
                except ValueError:
                    # 日期解析失败
                    pass


