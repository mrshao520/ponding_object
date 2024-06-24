import json
from datetime import datetime, timedelta

from DrissionPage import *
import time
from src.utils.Path import current_path

all_data = []
all_clear_data = []
def get_cookies_dict():
    with open(current_path + "/documents/douyin.json", 'r') as file:
        cookies_list = json.load(file)

    cookies_dict = {}
    for cookies_dict_item in cookies_list:
        cookies_dict[cookies_dict_item["name"]] = cookies_dict_item["value"]

    return cookies_dict

COOKIE_DICT = get_cookies_dict()
def convert_description_to_date(description):
    time_units = {"年前": 365, "月前": 30, "周前": 7, "天前": 1}

    for unit, days in time_units.items():
        if unit in description:
            time_ago = int(description.split(unit)[0])
            return datetime.now() - timedelta(days=days * time_ago)

    return datetime.min


def start_DrissionPage(selected_city, selected_date, output):
    page = WebPage()
    ChromiumOptions().auto_port(True)
    # page.set.window.hide()
    # page.get('https://www.douyin.com/')
    # page.set.cookies(COOKIE_DICT)

    page.get(f'https://www.douyin.com/search/{selected_city}?type=video')
    # page.get('https://www.douyin.com/video/6859894938495094023')
    time.sleep(1)
    # tag = 1
    # while tag <= 20:
    #     page.scroll.down(1000)
    #     time.sleep(1)
    #     tag += 1
    size = 1000
    for it in range(0, 20):
        page.scroll.down(size)
        size += size
        time.sleep(1)
        
    data_list = page.eles('@class=HN50D2ec Z3LKqldT')
    if len(data_list) == 0:
        output(f"检索失败-error-抖音-字符串匹配失败")
        return
    for item in data_list:
        title = item.ele('@class=F1Pew_Wu').text
        link = item.ele('@class=B3AsdZT9 KdyjYby4').link
        date = item.ele('@class=H_OXalNs').text
        # print(title, link, date)
        # all_data.append({'title': title, 'link': link, 'date': date})
        if '雨' in title and '积水' in title and '补漏' not in title and '水砖' not in title and '装修' not in title and '孕' not in title and '肾' not in title and '卵' not in title:
            all_data.append({'url': link, 'date': date, 'title': title})
    print(len(all_data))
    page.quit()
    days_difference = (datetime.now() - selected_date).days
    filtered_links = [link for link in all_data if
                      convert_description_to_date(link['date']) >= datetime.now() - timedelta(days=days_difference) and
                      '雨' in link['title'] and '积水' in link['title'] and
                      '补漏' not in link['title'] and
                      '水砖' not in link['title'] and
                      '装修' not in link['title']]
    all_clear_data.extend(filtered_links)
    print(len(all_clear_data))
    print(all_clear_data)
    get_data(output)

def get_data(output):
    page = WebPage()
    ChromiumOptions().auto_port(True)
    # page.set.window.hide()
    page.get('https://www.douyin.com/')
    page.set.cookies(COOKIE_DICT)
    start_url = all_clear_data
    urls = [data['url'] for data in start_url]
    for url in urls:
        page.get(url=url)
        # page.set.load_mode.eager()
        title = page.ele('@class=hE8dATZQ').text
        date = page.ele('@class=D8UdT9V8').text
        print(title, date)
        output(f'{date} {title}')
    page.quit()



