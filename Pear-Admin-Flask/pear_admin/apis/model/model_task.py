from datetime import datetime, timedelta
from loguru import logger
from configs import BaseConfig
from pear_admin.extensions import scheduler
from pear_admin.utils import FtpUtil
from .uie_model import UIE_Model
import os, csv


@scheduler._scheduler.scheduled_job(
    id="model_task_get_untreated",
    trigger="interval",
    hours=1,
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
    untreated_remote_file = os.path.join(remote_path, untreated_data_file)
    treated_remote_file = os.path.join(remote_path, treated_data_file)
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
    ftp_client.deletfile(untreated_data_file, remote_path)
    ftp_client.close()
    # 打开文件
    content = []
    with open(untreated_local_file, "r", encoding="utf-8") as file:
        # 读取所有行到一个列表中
        content = file.readlines()

    # 保存文件
    uie = UIE_Model()
    results = uie.predict(cities, content, treated_local_file)

    if not os.path.exists(treated_local_file):
        logger.info(f"{treated_local_file} 不存在，返回！")
        return False
    # FTP 上传文件
    ftp_client = FtpUtil()
    ftp_client.deletfile(treated_data_file, remote_path)
    ftp_client.uploadfile(treated_local_file, treated_remote_file)
    ftp_client.close()


@scheduler._scheduler.scheduled_job(
    id="model_task_get_data",
    trigger="interval",
    hours=1,
    start_date="2024-06-26 00:57:00",
    end_date="2034-06-26 00:00:00",
    max_instances=100,
)
def model_task_get_data():
    now = datetime.now()
    logger.info(f"当前时间: {now} - model_task_get_data")
    # 配置文件中的文件和路径
    remote_path = BaseConfig.REMOTE_PATH  # 远程路径
    data_file = BaseConfig.TREATED_DATA_FILE
    results_data_file = BaseConfig.RESULTS_DATA_FILE
    # 远程文件
    data_remote_file = os.path.join(remote_path, data_file)
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
    ftp_client.deletfile(data_file, remote_path)
    ftp_client.close()

    # 打开源CSV文件，读取数据
    with open(data_local_file, mode="r", encoding="utf-8") as source_file:
        source_reader = csv.reader(source_file)
        source_data = list(source_reader)

    # 打开目标CSV文件，追加数据
    with open(results_data_file, mode="a", encoding="utf-8", newline="") as dest_file:
        dest_writer = csv.writer(dest_file)

        # 写入数据到目标文件末尾
        for row in source_data:
            dest_writer.writerow(row)
