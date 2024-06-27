import os
from datetime import timedelta
from flask_apscheduler.auth import HTTPBasicAuth
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "pear-admin-flask")

    SQLALCHEMY_DATABASE_URI = ""

    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    # 设置时区，时区不一致会导致定时任务的时间错误
    # SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    # 一定要开启API功能，这样才可以用api的方式去查看和修改定时任务
    SCHEDULER_API_ENABLED = True
    # api前缀（默认是/scheduler）
    SCHEDULER_API_PREFIX = "/scheduler"
    # 配置允许执行定时任务的主机名
    SCHEDULER_ALLOWED_HOSTS = ["*"]
    # auth验证。默认是关闭的，
    # SCHEDULER_AUTH = HTTPBasicAuth()
    # 设置定时任务的执行器（默认是最大执行数量为80的线程池）
    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 80}}

    # loguru 日志设置
    LOG_FILENAME = "./log/log_{time:YYYY-MM-DD}.log"
    LOG_ROTATION = "00:00"  # rotation 将日志记录以文件大小、时间等方式进行分割或划分
    # LOG_COMPRESSION = "zip" # compress 对日志进行压缩
    LOG_RETENTION = "20 days"  # retention 日志保留时间
    LOG_LEVEL = "DEBUG"
    LOG_FORMAT = (
        "{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}"
    )
    # GPU服务器设置
    OPEN_PONDING_SERVER = True
    PONDING_EXTRACT = "http://127.0.0.1:8886/extract"
    # 高德API KEY设置
    GAODE_API = "3f9d8dabae7db3acf1612c15a3b1e150"

    # model config
    USE_MODEL = False  # 是否使用GPU服务模块
    MODEL_PATH = "./static/model"  # 模型文件地址
    MODEL_SCHEMA = ["日期", "时间", "城市", {"地点": ["描述", "深度值"]}]  # 模型模式
    MODEL_DEVICE_ID = 0  # 模型 GPU id
    MODEL_SAVE_DATA = True  # 模型处理后保存结果
    MODEL_GET_LOCATION = False  # 模型处理后使用API获取经纬度
    MODEL_FORMAT_RES = True  # 在model模块中进行格式化结果

    # ftp config
    FTP_USER = "pmsc_cps_user"
    FTP_HOST = "10.0.65.153"
    FTP_PASSWORD = "Y6zXTwdpDKcjMMWX"
    FTP_PASSIVE = True

    # 保存文件设置
    REMOTE_PATH = "/ponding/ponding_server/pear-admin-flask"
    UNTREATED_DATA_FILE = "./data/untreated_data.txt"  # 爬虫爬取的文件
    TREATED_DATA_FILE = "./data/treated_data.csv"  # 模型处理后的数据文件，不包含经纬度
    DATA_FILE = "./data/data.csv"  # 含有经纬度的数据文件
    RESULTS_DATA_FILE = "./data/results.csv"  # 汇总数据文件
    DATA_CITIES = [
        "北京",
        "上海",
        "深圳",
        "广州",
        "杭州",
        "成都",
        "天津",
        "合肥",
        "东莞",
        "武汉",
        "西安",
        "重庆",
        "郑州",
        "南京",
        "济南",
    ]
    # CSV_FILENAME = "./data/data_{time:%Y_%m_%d_%H}.csv"
    CSV_HEADERS = [
        "date",
        "time",
        "format_time",
        "city",
        "position",
        "longitude",
        "latitude",
        "depth_value",
        "format_depth_value",
        "description",
    ]


class DevelopmentConfig(BaseConfig):
    """开发配置"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///pear_admin.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 存储定时任务
    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(
            url="sqlite:///instance/pear_admin.db", tablename="ums_task_scheduler"
        )
    }


class TestingConfig(BaseConfig):
    """测试配置"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # 内存数据库


class ProductionConfig(BaseConfig):
    """生成环境配置"""

    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/pear_admin"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {"dev": DevelopmentConfig, "test": TestingConfig, "prod": ProductionConfig}
