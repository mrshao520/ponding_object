import asyncio
from datetime import datetime
from aiohttp import ClientSession
from retrying import retry
import requests
import re
from collections import OrderedDict
from bs4 import BeautifulSoup


def convert_judge(formatted_date_str, start_date, end_date):
    try:
        formatted_date = datetime.strptime(formatted_date_str, "%Y年%m月%d日 %H:%M")
    except ValueError:
        try:
            formatted_date = datetime.strptime(formatted_date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError(f"Unsupported date format: {formatted_date_str}")

    date_str = formatted_date.strftime('%Y-%m-%d %H:%M:%S')
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    
    in_range = (start_date <= formatted_date <= end_date)

    return date_str, in_range


async def scrape_flood_news(strat_date, end_date, city, output):
    all_urls = []
    max_pages = 15
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Cookie": "__ac_nonce=0666a9af300539a94b72a; __ac_signature=_02B4Z6wo00f01LdMVLQAAIDBaBen-86gj-C3bFAAAEu-9a; __ac_referer=__ac_blank; tt_webid=7379881230432617996; _ga_QEHZPBE5HH=GS1.1.1718262521.1.0.1718262521.0.0.0; _ga=GA1.1.584859241.1718262522; ttwid=1%7CeIRuAYmcKThvmtZtbW6uZ9byj2nGtlXr-Sr2zdKLLeg%7C1718262521%7C86b8c4efb1e7b3d695e59f8ff14501cf203f98296d9fbbb751dac46695dac676; _tea_utm_cache_4916=undefined; _S_WIN_WH=1659_804; _S_DPR=1.5; _S_IPAD=0; mp_851392464b60e8cc1948a193642f793b_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A190106d61a91896-0b4861772d16f1-4c657b58-190140-190106d61a91896%22%2C%22%24device_id%22%3A%20%22190106d61a91896-0b4861772d16f1-4c657b58-190140-190106d61a91896%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fso.toutiao.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22so.toutiao.com%22%7D; s_v_web_id=verify_lxcx828g_xXGOBmx6_vRc5_4Ux8_AYPY_ysCrxOTOxoLV",
        "referer": "https://so.toutiao.com/search?",
    }

    print(f"当前城市{city}")
    for page in range(max_pages):
        print(f"当前页{page}")
        url = f"https://so.toutiao.com/search?keyword={city}&pd=information&source=search_subtab_switch&dvpf=pc&aid=4916&page_num={page}&from=news&search_json=%7B%22from_search_id%22%3A%2220240124085830E55600FE028ECC0777C8%22%7D&action_type=search_subtab_switch&search_id=&cur_tab_title=news"
        response = requests.get(url=url, headers=headers)
        data = response.text
        obj = re.compile(r'"share_url":"(?P<url>.*?)"', re.S)
        # obj = re.compile(r'"share_url00":"(?P<url>.*?)"', re.S)
        result = obj.finditer(data)
        for i in result:
            url = i.group("url")
            all_urls.append(url)
    if len(all_urls) == 0:
        output(f"检索失败-error-头条-链接匹配失败")

    unique_urls = list(OrderedDict.fromkeys(all_urls))
    modified_urls = [
        url.replace("toutiao.com", "www.toutiao.com") for url in unique_urls
    ]
    modified_urls = [url.replace("group", "article") for url in modified_urls]
    pattern = re.compile(
        r"(news\.bjd\.com\.cn|www\.toutiao\.com|m\.bjnews\.com\.cn|3w\.huanqiu\.com|bj\.bjd\.com\.cn)"
    )
    modified_urls = list(filter(lambda url: pattern.search(url), modified_urls))
    print(len(modified_urls))

    async def get_url_content_async(url, headers):
        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    async def get_url_content_retry_async(url, headers):
        return await get_url_content_async(url, headers)

    async def process_urls_async(modified_urls, headers):
        tasks = [get_url_content_retry_async(url, headers) for url in modified_urls]
        return await asyncio.gather(*tasks)

    async def main():
        try:
            results = await process_urls_async(modified_urls, headers)
            for result in results:
                soup = BeautifulSoup(result, "html.parser")
                article_div = soup.find("div", class_="article")
                if article_div:
                    all_text = "".join(article_div.stripped_strings)
                    if "雨" in all_text and "积水" in all_text:
                        # output(all_text)
                        time_element = soup.find("div", class_="time")
                        if time_element:
                            time_info = time_element.get_text(strip=True)

                            time_info, in_range = convert_judge(time_info, strat_date, end_date)
                            if in_range:
                                output(f'{time_info} {all_text}')

                        else:
                            print("No time element found.")
                else:
                    article_div = soup.find("div", class_="article-content")
                    if article_div:
                        all_text = "".join(article_div.stripped_strings)
                        article_meta_div = soup.find("div", class_="article-meta")
                        if "雨" in all_text and "积水" in all_text:
                            # output(all_text)
                            if article_meta_div:
                                time_element = article_meta_div.find(
                                    "span",
                                    string=re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}"),
                                )
                                if time_element:
                                    time_info = time_element.get_text(strip=True)

                                    time_info, in_range = convert_judge(time_info, strat_date, end_date)
                                    if in_range:
                                        output(f'{time_info} {all_text}')
                                else:
                                    print("No time element found.")
                            else:
                                print("No article meta div found.")
                    else:
                        article_div = soup.find("div", class_="article-cen")
                        if article_div:
                            all_text = "".join(article_div.stripped_strings)
                            if "雨" in all_text and "积水" in all_text:
                                # output(all_text)
                                time_element = soup.find(
                                    "p", style="float: right;margin-right: 0;"
                                )
                                if time_element:
                                    time_info = time_element.get_text(strip=True)

                                    time_info, in_range = convert_judge(time_info, strat_date, end_date)
                                    if in_range:
                                        output(f'{time_info} {all_text}')
                                else:
                                    print("No time element found.")
                        else:
                            article_div = soup.find("div", class_="content-a")
                            if article_div:
                                all_text = "".join(article_div.stripped_strings)
                                if "雨" in all_text and "积水" in all_text:
                                    # output(all_text)
                                    time_element = soup.find("span", class_="time")
                                    if time_element:
                                        time_info = time_element.get_text(strip=True)

                                        time_info, in_range = convert_judge(time_info, strat_date, end_date)
                                        if in_range:
                                            output(f'{time_info} {all_text}')
                                    else:
                                        print("No time element found.")
                            else:
                                article_div = soup.find("div", class_="col-lg-12")
                                if article_div:
                                    all_text = "".join(article_div.stripped_strings)
                                    if "雨" in all_text and "积水" in all_text:
                                        # output(all_text)
                                        time_element = soup.find(
                                            "span",
                                            string=re.compile(
                                                r"\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}"
                                            ),
                                        )
                                        if time_element:
                                            time_info = time_element.get_text(
                                                strip=True
                                            )

                                            time_info, in_range = convert_judge(time_info, strat_date, end_date)
                                            if in_range:
                                                output(f'{time_info} {all_text}')
                                        else:
                                            print("No time element found.")
                                else:
                                    article_div = soup.find(
                                        "div", class_="bjd-article-centent"
                                    )
                                    if article_div:
                                        all_text = "".join(article_div.stripped_strings)
                                        if "雨" in all_text and "积水" in all_text:
                                            # output(all_text)
                                            time_element = soup.find(
                                                "p",
                                                style="float: right;margin-right: 0;",
                                            )
                                            if time_element:
                                                time_info = time_element.get_text(
                                                    strip=True
                                                )

                                                time_info, in_range = convert_judge(time_info, strat_date, end_date)
                                                if in_range:
                                                    output(f'{time_info} {all_text}')
                                            else:
                                                time_element = soup.find(
                                                    "div", class_="bjd-article-source"
                                                ).find("p")
                                                if time_element:
                                                    time_info = time_element.get_text(
                                                        strip=True
                                                    )
                                                    time_info, in_range = convert_judge(time_info, strat_date, end_date)
                                                    if in_range:
                                                        output(f'{time_info} {all_text}')
                                                else:
                                                    print("No time element found.")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    await main()


if __name__ == "__main__":
    cities = "济南积水点"
    start_date = "2023-01-01 00:00:00"
    end_date = "2024-09-08 23:59:00"
    asyncio.run(scrape_flood_news(start_date, end_date, cities, print))
