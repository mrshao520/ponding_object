from flask import Blueprint
from pear_admin.extensions import db
from pear_admin.orms import DataSummaryORM

summary_api = Blueprint("summary", __name__)

@summary_api.get("/summary")
def summary_list():
    q = db.select(DataSummaryORM)

    return {
        "code": 0,
        "msg": "获取积水点数据成功",
        "data": [item.json() for item in q.items],
    }
