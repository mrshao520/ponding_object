import csv
import os
import re

from flask import Flask, current_app

from pear_admin.extensions import db
from pear_admin.orms import (
    DepartmentORM,
    RightsORM,
    RoleORM,
    UserORM,
    DataPondingORM,
    ChannelsORM,
)
from datetime import datetime
from configs import DevelopmentConfig
from pear_admin.apis.function.format_time import format_datetime

def dict_to_orm(d, o):
    for k, v in d.items():
        if k == "password":
            o.password = v
        if k == "date":
            o.date = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        else:
            try:
                setattr(o, k, v or None)
            except:
                print(f"{k}-{v}-{d}")
                exit


def csv_to_databases(path, orm):
    with open(path, encoding="utf-8") as file:
        for d in csv.DictReader(file):
            o = orm()
            dict_to_orm(d, o)
            db.session.add(o)
            db.session.flush()
        db.session.commit()

def register_script(app: Flask):
    # 用于注册一个命令到Flask应用程序的命令行界面（CLI）
    # 这个命令是 init，用于初始化数据库
    @app.cli.command()  # 装饰器，将 init 函数注册为 Flask CLI 命令
    def init():
        """
        将 csv 文件中的数据导入到数据库
        """
        # 删除所有数据库
        db.drop_all()
        # 创建数据库
        db.create_all()

        root = current_app.config.get("ROOT_PATH")

        rights_data_path = os.path.join(root, "static", "data", "ums_rights.csv")
        csv_to_databases(rights_data_path, RightsORM)

        role_data_path = os.path.join(root, "static", "data", "ums_role.csv")
        csv_to_databases(role_data_path, RoleORM)

        with open(role_data_path, encoding="utf-8") as file:
            for d in csv.DictReader(file):
                role: RoleORM = RoleORM.query.get(d["id"])
                id_list = [int(_id) for _id in d["rights_ids"].split(":")]
                role.rights_list = RightsORM.query.filter(
                    RightsORM.id.in_(id_list)
                ).all()
                db.session.commit()

        department_data_path = os.path.join(
            root, "static", "data", "ums_department.csv"
        )
        csv_to_databases(department_data_path, DepartmentORM)

        user_data_path = os.path.join(root, "static", "data", "ums_user.csv")
        csv_to_databases(user_data_path, UserORM)

        with open(user_data_path, encoding="utf-8") as file:
            for d in csv.DictReader(file):
                user: UserORM = UserORM.query.get(d["id"])
                id_list = [int(_id) for _id in d["role_ids"].split(":")]
                user.role_list = RoleORM.query.filter(RoleORM.id.in_(id_list)).all()
                db.session.commit()

        ponding_data_path = os.path.join(root, "static", "data", "ums_data_ponding.csv")
        # csv_to_databases(ponding_data_path, DataPondingORM)
        ponding_to_databases(ponding_data_path, DataPondingORM)

        channels_data_path = os.path.join(
            root, "static", "data", "ums_task_channels.csv"
        )
        csv_to_databases(channels_data_path, ChannelsORM)

        try:
            DevelopmentConfig.SCHEDULER_JOBSTORES.get("default").remove_all_jobs()
        except Exception as e:
            print(f"{e}")


def ponding_to_orm(d, o):
    for k, v in d.items():
        if k == "date":
            o.date = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        elif k == "time" and v:
            setattr(o, "time", v or None)
            if not o.date:
                o.date = datetime.strptime(d["date"], "%Y-%m-%d %H:%M:%S")
            setattr(o, "format_time", format_datetime(o.date, v) or None)
        elif k == "depth_value" and v:
            setattr(o, k, v or None)
            format_v = format_value(v)
            # print(format_v)
            setattr(o, "format_depth_value", format_v or None)
        else:
            try:
                setattr(o, k, v or None)
            except:
                print(f"{k}-{v}-{d}")
                exit


def ponding_to_databases(path, orm):
    with open(path, encoding="utf-8") as file:
        for d in csv.DictReader(file):
            o = orm()
            ponding_to_orm(d, o)
            db.session.add(o)
            db.session.flush()
        db.session.commit()
        
def format_value(depth:str):
    numbers = re.findall(r"\d+\.\d+|\d+", depth)
    # print(numbers)
    if not numbers:
            return 
    number = float(numbers[0]) # 获取第一个数字    
    if 'cm' in depth or 'CM' in depth or '厘米' in depth or '公分' in depth:
        return f'{number}cm'
    if 'mm' in depth or 'MM' in depth or '毫米' in depth:
        return f'{number // 100}cm'
    elif 'm' in depth or 'M' in depth or '米' in depth:
        return f'{number * 100}cm'
    return 
