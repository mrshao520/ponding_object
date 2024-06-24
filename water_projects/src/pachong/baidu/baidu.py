import re
from datetime import datetime

from DrissionPage import *
from bs4 import BeautifulSoup


def get_date(soup):
    time_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}'
    date = re.findall(time_pattern, soup.text)
    if date:
        dates_str = date[0]
        return dates_str
    else:
        return None


def get_title(web, link):
    web.get(link)
    try:
        title = web.ele('@class=EaCvy').text
        title = title.replace("\n", "")
        return title
    except:
        try:
            title = web.ele('@class=container').text
            title = title.replace("\n", "")
            return title
        except:
            return None


def convert_judge(formatted_date_str, start_date, end_date, output):
    try:
        formatted_date = datetime.strptime(formatted_date_str, '%Y年%m月%d日 %H:%M')
    except ValueError:
        try:
            formatted_date = datetime.strptime(formatted_date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            output(f'Unsupported date format: {formatted_date_str}')
            raise ValueError(f"Unsupported date format: {formatted_date_str}")
            pass

    date_str = formatted_date.strftime('%Y-%m-%d %H:%M:%S')

    start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

    in_range = (start_date <= formatted_date <= end_date)

    return date_str, in_range

def get_data(start_date, end_date, selected_city, output):
    all_links = []
    resp = SessionPage()
    for page in range(0, 10):
        url = f"https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_b_pn&cl=2&wd={selected_city}&tn=news&rsv_bp=1&rsv_sug3=31&rsv_sug1=9&rsv_sug7=101&oq=&rsv_sug2=0&rsv_btype=t&f=8&inputT=7856&rsv_sug4=9198&x_bfe_rqs=03E8000000000000000048&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&goods_entry_switch=1&pn={page * 10}"
        resp.get(url)
        link_list = resp.eles('@class=news-title-font_1xS-F')
        for item in link_list:
            link = item.link
            if "for=pc" in link:
                all_links.append(link)
    if len(all_links) == 0:
        output(f"检索失败-error-百度-字符串匹配失败")
        return
    else:
        web = WebPage()
        ChromiumOptions().auto_port(True)
        web.set.load_mode.eager()
        web.set.window.hide()
        for link in all_links:
            title = get_title(web, link)
            if title:
                page = web.html
                soup = BeautifulSoup(page, "html.parser")
                date = get_date(soup)
                date, in_range = convert_judge(date, start_date, end_date, output)
                if in_range:
                    if '雨' in title and '积水' in title:
                        # 判断之后你输出进行
                        print(f"标题: {title}")
                        print(f"日期: {date}")
                        output(date + " " + title)
            else:
                continue
        web.quit()


# start_date = "2023-01-01 00:00:00"
# end_date = "2024-09-08 23:59:00"
# get_data(start_date=start_date, end_date=end_date, selected_city="北京积水点", output=print)
