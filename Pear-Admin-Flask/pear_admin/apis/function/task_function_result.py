from datetime import datetime
from loguru import logger
from .get_location import get_location
from configs import BaseConfig
from pear_admin.orms import DataPondingORM
from pear_admin.extensions import scheduler
import csv, os


@scheduler._scheduler.scheduled_job(
    id="task_function_results",
    trigger="interval",
    # hours=1,
    minutes=5,  # for test
    start_date="2024-06-26 00:53:00",
    end_date="2034-06-26 00:00:00",
    max_instances=100,
)
def task_function_result():
    """根据模型处理后的结果获取经纬度"""
    now = datetime.now()
    logger.info(f"当前时间: {now} - task_function_result")

    treated_data_file = BaseConfig.TREATED_DATA_FILE
    data_file = BaseConfig.DATA_FILE
    csv_headers = BaseConfig.CSV_HEADERS

    if os.path.exists(treated_data_file) and os.path.isfile(treated_data_file):
        # 使用with语句确保文件正确关闭
        with open(treated_data_file, mode="r", encoding="utf-8") as file:
            # 打开CSV文件
            with open(data_file, mode="a", newline="", encoding="utf-8") as csvfile:
                # 创建CSV写入器
                writer = csv.writer(csvfile)
                # 如果CSV文件不存在，则写入列名
                if not csvfile.tell():
                    writer.writerow(csv_headers)

                # 使用csv.DictReader读取文件
                csv_reader = csv.DictReader(file)
                # 遍历CSV文件的每一行
                for row in csv_reader:
                    # logger.info(f"{row}")
                    # 获取经纬度
                    lati_longi_tude = get_location(
                        city=row["city"], address=row["position"]
                    )
                    if not lati_longi_tude:
                        # 未获取经纬度
                        logger.info(f'{row["city"]}-{row["position"]}: 未获取经纬度!')
                        continue
                    longitude, latitude = lati_longi_tude.split(",", maxsplit=2)
                    row["longitude"] = longitude
                    row["latitude"] = latitude
                    row["date"] = datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")
                    row["format_time"] = (
                        datetime.strptime(row["format_time"], "%Y-%m-%d %H:%M:%S")
                        if row["format_time"]
                        else None
                    )
                    with scheduler.app.app_context():
                        ponding = DataPondingORM(**row)
                        result = ponding.save()
                        ponding_json = ponding.json()
                    if not result:
                        continue

                    ponding_list = [
                        ponding_json.get(header, None) for header in csv_headers
                    ]
                    # 写入数据
                    writer.writerow(ponding_list)
                    # 打印每一行的内容
                    # logger.info(ponding_list)
        logger.info(f"文件 {data_file} 已生成!")
        os.remove(treated_data_file)
    else:
        logger.info(f"文件 {treated_data_file} 不存在，返回")
        return
