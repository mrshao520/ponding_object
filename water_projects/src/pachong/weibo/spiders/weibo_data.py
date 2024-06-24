import re
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime


from src.pachong.weibo.items import WeiboItem
from src.pachong.utils import create_chrome_driver, add_cookies
from src.utils.Path import current_path


all_links = []
start_date = []
end_date = []
filtered_links = []
requests = []
dates = []


def extract_code_from_url(url):
    match = re.search(r'/([^/?]+)\?', url)
    return match.group(1) if match else None



def is_date_in_range(formatted_date_str, start_date_list, end_date_list):
    try:
        formatted_date = datetime.strptime(formatted_date_str, '%Y年%m月%d日 %H:%M')
    except ValueError:
        try:
            formatted_date = datetime.strptime(formatted_date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValueError(f"Unsupported date format: {formatted_date_str}")

    start_date = start_date_list[0] if start_date_list else None
    end_date = end_date_list[0] if end_date_list else None

    return start_date <= formatted_date <= end_date



def process_date_text(date_text):
    
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_day = datetime.now().day
    date_pattern_with_time = re.compile(r'(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2})')
    date_pattern_without_time = re.compile(r'(\d{2}月\d{2}日 \d{2}:\d{2})')
    date_pattern_new_format = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})')
    date_pattern_today = re.compile(r'今天(\d{2}:\d{2})')

    matches_with_time = date_pattern_with_time.findall(date_text)
    matches_without_time = date_pattern_without_time.findall(date_text)
    matches_new_format = date_pattern_new_format.findall(date_text)
    matches_today = date_pattern_today.findall(date_text)

    formatted_dates = []

    for match in matches_with_time:
        formatted_dates.append(match)

    for match in matches_without_time:
        formatted_dates.append(f'{current_year}年{match}')

    for match in matches_new_format:
        formatted_dates.append(match)

    for match in matches_today:
        time_part = match
        formatted_date = f'{current_year}-{current_month:02d}-{current_day:02d} {time_part}'
        formatted_dates.append(formatted_date)

    return formatted_dates





def acquire_url(selected_city, select_start_date, select_end_date, output, headless):
    dates = []
    
    global start_date, end_date, request
    long_text_links = []
    short_text_links = []
    # 获取选择的结束日期
    start_date.clear()  # 清空全局变量的内容
    end_date.clear()

    start_date.append(select_start_date)  # 使用append方法添加元素到全局变量
    end_date.append(select_end_date)

    browser = create_chrome_driver(headless)
    browser.get(
        'https://weibo.com/newlogin?tabtype=weibo&gid=102803&openLoginLayer=0&url=https%3A%2F%2Fweibo.com%2F')
    path = current_path + '/documents/weibo.json'
    for pag in range(17):
        add_cookies(browser, path)
        url = f'https://s.weibo.com/weibo?q={selected_city}&page={pag + 1}'
        browser.get(url=url)
        response = browser.page_source
        # print(response)
        soup = BeautifulSoup(response, 'html.parser')

        div_class = soup.find_all('div', {'class': 'from'})
        # div_class = soup.find_all('div', {'class': 'fromww1'})

        for it in div_class:
            a_tag = it.find('a', {'href': True, 'target': '_blank'})
            if a_tag:
                short_href_value = a_tag['href']
                date_text = a_tag.text.strip()
                formatted_dates = process_date_text(date_text)
                formatted_date = formatted_dates[0]
                short_text_links.append((formatted_date, short_href_value))

        p_tags = soup.find_all('p', {'node-type': 'feed_list_content'})
        for p_tag in p_tags:
            a_tag = p_tag.find('a', {'href': True, 'action-type': 'fl_unfold'})
            if a_tag:
                long_href_value = a_tag['href']
                long_text_links.append((long_href_value,))

        short_text_links = [tuple(item) for item in short_text_links]
        long_text_links = [tuple(item) for item in long_text_links]

        unique_short_urls = set(item[1] for item in short_text_links)
        unique_long_urls = set(item[0] for item in long_text_links)

        unique_short_text_links = [item for item in short_text_links if
                                    item[1] in unique_short_urls - unique_long_urls]
        new_long_text_links = []
        for i, (formatted_date, short_href) in enumerate(short_text_links):
            if (formatted_date, short_href) not in unique_short_text_links:
                new_long_text_links.append((formatted_date, short_href))

        for formatted_date, short_href in new_long_text_links:
            extracted_code = extract_code_from_url(short_href)
            if extracted_code:
                long_link = f'https://weibo.com/ajax/statuses/longtext?id={extracted_code}'
                all_links.append((formatted_date, long_link))
            else:
                print(f"Short URL: {short_href}, 无法提取代码")

        for formatted_date, short_href in unique_short_text_links:
            # print(f"Formatted Date: {formatted_date}, Short Href: {short_href}")
            extracted_code = extract_code_from_url(short_href)
            if extracted_code:
                short_link = f'https://weibo.com/ajax/statuses/show?id={extracted_code}&locale=zh-CN'
                all_links.append((formatted_date, short_link))
            else:
                print(f"Short URL: {short_href}, 无法提取代码")

        for formatted_date, short_href in all_links:
            date = formatted_date
            if is_date_in_range(date, start_date, end_date):
                filtered_links.append((formatted_date, short_href))

    for formatted_date, url in filtered_links:
        request = scrapy.Request(url, meta={'formatted_date': formatted_date})
        requests.append(request)
        dates.append(formatted_date)

    if len(all_links) == 0:
        output(f"检索失败-error-微博-字符串匹配失败")
        return
    return requests


class WeiboDataSpider(scrapy.Spider):
    name = "weibo_data"
    allowed_domains = ["weibo.com"]
    
    Queue = None
    cityName = None
    startTime = None
    endTime = None
    
    def __init__(self, *args, **kwargs):
        super(WeiboDataSpider, self).__init__(*args, **kwargs)
        # self.Queue.put('+++++++++' + self.name)
        # self.Queue.put(self.cityName)
        # self.Queue.put(self.startTime)
        # self.Queue.put(self.endTime)
        self.start_date = datetime.strptime(self.startTime, '%Y-%m-%d %H:%M:%S')
        self.end_date = datetime.strptime(self.endTime, '%Y-%m-%d %H:%M:%S')
        self.requests = acquire_url(self.cityName, self.start_date, self.end_date, 
                                    self.Queue.put, headless=self.headless)  # 获取 formatted_dates

    def start_requests(self):
        self.Queue.put('开始采集 微博 渠道')
        for request in self.requests:
            # print(request)
            yield request
            
    def close(spider, reason):
        spider.Queue.put('微博 渠道采集结束')

    def parse(self, response, **kwargs):
        data_item = WeiboItem()
        formatted_date = response.meta.get('formatted_date')
        # formatted_date = convert_date_format(formatted_date)
        chinese_pattern = re.compile('[\u4e00-\u9fa5]+')
        matches = chinese_pattern.findall(response.text)
        result_string = ''.join(matches)
        self.Queue.put(formatted_date + result_string)
        # 使用正则表达式判断字符串中是否包含“雨”和“积水”
        if '雨' in result_string and '积水' in result_string:
            data_item['date'] = formatted_date
            data_item['data'] = result_string
            self.Queue.put(formatted_date + result_string)
            yield data_item



