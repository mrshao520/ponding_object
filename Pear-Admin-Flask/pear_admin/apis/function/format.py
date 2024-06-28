import re
from datetime import datetime
from loguru import logger


def format_value(depth: str):
    if depth == "":
        return None
    numbers = re.findall(r"\d+\.\d+|\d+", depth)
    # print(numbers)
    if not numbers:
        return None
    number = float(numbers[0])  # 获取第一个数字
    if "cm" in depth or "CM" in depth or "厘米" in depth or "公分" in depth:
        return f"{number}cm"
    if "mm" in depth or "MM" in depth or "毫米" in depth:
        return f"{number / 10}cm"
    elif "m" in depth or "M" in depth or "米" in depth:
        return f"{number * 100}cm"
    return None


def format_datetime(input_datetime: datetime, str_datetime: str):
    if str_datetime == "":
        return None
    # 定义时间表达式的正则模式
    time_patterns = {
        # 年份+月份+日期
        r"(\d+)年(\d+)月(\d+)[日|号]": lambda year, month, day: datetime(
            year=year, month=month, day=day
        ),
        # 月份+日期
        r"(\d+)月(\d+)[日|号]": lambda month, day: datetime(
            year=input_datetime.year, month=month, day=day
        ),
        # 日期
        r"(\d+)[日|号]": lambda day: datetime(
            year=input_datetime.year, month=input_datetime.month, day=day
        ),
        r"今|当": lambda: datetime(
            year=input_datetime.year,
            month=input_datetime.month,
            day=input_datetime.day,
        ),
        r"昨": lambda: datetime(
            year=input_datetime.year,
            month=input_datetime.month,
            day=input_datetime.day - 1,
        ),
        r"明": lambda: datetime(
            year=input_datetime.year,
            month=input_datetime.month,
            day=input_datetime.day + 1,
        ),
        r"(\d{4})-(\d{2})-(\d{2})": lambda year, month, day: datetime(year, month, day),
        r"(\d{2})-(\d{2})": lambda month, day: datetime(
            input_datetime.year, month, day
        ),
        r"(\d{4})/(\d{2})/(\d{2})": lambda year, month, day: datetime(year, month, day),
        r"(\d{2})/(\d{2})": lambda month, day: datetime(
            input_datetime.year, month, day
        ),
    }
    # 解析时间表达式
    for pattern, func in time_patterns.items():
        match = re.search(pattern, str_datetime)
        # print(str_datetime)
        if match:
            try:
                match = [int(m) for m in match.groups()]
                format_time = func(*match)
                return format_time
            except Exception as e:
                logger.debug(f"format_time throw an exception: {e}")
                return None
    return None


if __name__ == "__main__":
    # 测试
    texts = [
        "2月19日晚至20日凌晨",
        "今天上午",
        "11日17时至13日0时",
        "截至12点",
        "7月29日下午2时许",
        "7月31日一大早",
        "今天上午",
        "昨天早上5时许",
        "今天上午9时",
        "9月7日夜间到8日早晨",
        "28日10时至14时",
        "昨天（7月11日）",
        "昨天早上",
        "2月19日晚至20日凌晨",
        "截至7月29日中午11时30分",
    ]

    for text in texts:
        now = datetime.now()
        result = format_datetime(now, text)
        print(f"{now}       {result}")
