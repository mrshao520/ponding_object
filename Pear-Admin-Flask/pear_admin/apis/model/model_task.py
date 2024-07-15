from datetime import datetime
from loguru import logger
from configs import BaseConfig
from pear_admin.extensions import scheduler
from pear_admin.utils import FtpUtil
from pear_admin.orms import DataPondingORM
from .uie_model import UIE_Model
import os, csv
from pathlib import Path


@scheduler._scheduler.scheduled_job(
    id="model_task_get_untreated",
    trigger="interval",
    # hours=1,
    minutes=5,  # for test
    start_date="2024-06-26 00:40:00",
    end_date="2034-06-26 00:00:00",
    max_instances=100,
)
def model_task_get_untreated():
    now = datetime.now()
    logger.info(f"当前时间: {now} - model_task_get_untreated")
    # 配置文件中的文件和路径
    remote_path = BaseConfig.REMOTE_PATH  # 远程路径
    untreated_data_file = BaseConfig.UNTREATED_DATA_FILE  # 未处理的数据
    treated_data_file = BaseConfig.TREATED_DATA_FILE  # 处理后不带有经纬度的数据
    cities = BaseConfig.DATA_CITIES
    # 远程文件
    untreated_remote_file = str(Path(remote_path) / Path(untreated_data_file))
    treated_remote_file = str(Path(remote_path) / Path(treated_data_file))
    untreated_file_name_without_extension, untreated_file_extension = os.path.splitext(
        untreated_data_file
    )
    treated_file_name_without_extension, treated_file_extension = os.path.splitext(
        treated_data_file
    )
    # 本地文件
    untreated_local_file = (
        untreated_file_name_without_extension
        + f"_{now:%Y_%m_%d_%H}"
        + untreated_file_extension
    )
    treated_local_file = (
        treated_file_name_without_extension
        + f"_{now:%Y_%m_%d_%H}"
        + treated_file_extension
    )
    # FTP 下载文件
    ftp_client = FtpUtil()
    down_res = ftp_client.downloadfile(untreated_local_file, untreated_remote_file)
    if not down_res:
        logger.info(f"文件 {untreated_remote_file} 下载失败,返回！")
        ftp_client.close()
        return False
    ftp_client.deletfile(untreated_remote_file)
    ftp_client.close()
    # 打开文件
    content = []
    with open(untreated_local_file, "r", encoding="utf-8") as file:
        # 读取所有行到一个列表中
        content = file.readlines()

    # 保存文件
    uie = UIE_Model()
    results = uie.predict(cities, content, treated_local_file)

    if len(results) == 0:
        logger.info("未提取有效信息!")
        return

    if not os.path.exists(treated_local_file):
        logger.info(f"{treated_local_file} 不存在，返回！")
        return False
    # FTP 上传文件
    ftp_client = FtpUtil()
    # ftp_client.deletfile(treated_remote_file)
    ftp_client.uploadfile(treated_local_file, treated_remote_file)
    ftp_client.close()


@scheduler._scheduler.scheduled_job(
    id="model_task_get_data",
    trigger="interval",
    # hours=1,
    minutes=5,  # for test
    start_date="2024-06-26 00:57:00",
    end_date="2034-06-26 00:00:00",
    max_instances=100,
)
def model_task_get_data():
    now = datetime.now()
    logger.info(f"当前时间: {now} - model_task_get_data")
    csv_headers = BaseConfig.CSV_HEADERS
    # 配置文件中的文件和路径
    remote_path = BaseConfig.REMOTE_PATH  # 远程路径
    data_file = BaseConfig.DATA_FILE
    results_data_file = BaseConfig.RESULTS_DATA_FILE
    # 远程文件
    data_remote_file = str(Path(remote_path) / Path(data_file))
    file_name_without_extension, file_extension = os.path.splitext(data_file)
    # 本地文件
    data_local_file = (
        file_name_without_extension + f"_{now:%Y_%m_%d_%H}" + file_extension
    )
    # FTP 下载文件
    ftp_client = FtpUtil()
    down_res = ftp_client.downloadfile(data_local_file, data_remote_file)
    if not down_res:
        logger.info(f"下载 {data_remote_file} 文件失败，返回！")
        ftp_client.close()
        return False
    ftp_client.deletfile(data_remote_file)
    ftp_client.close()

    if not os.path.exists(results_data_file):
        logger.info(f"最终结果文件不存在: {results_data_file}")

    # 打开源CSV文件，读取数据
    with open(data_local_file, mode="r", encoding="utf-8") as source_file:
        with open(
            results_data_file, mode="a", encoding="utf-8", newline=""
        ) as dest_file:
            # 使用csv.DictReader读取文件
            source_reader = csv.DictReader(source_file)
            dest_writer = csv.writer(dest_file)
            # 遍历CSV文件的每一行
            for row in source_reader:
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
                dest_writer.writerow(ponding_list)
    logger.info(f"已保存到数据库和最终结果文件中!")
