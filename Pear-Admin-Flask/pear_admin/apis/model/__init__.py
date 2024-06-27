from flask import Blueprint, request
from .uie_model import UIE_Model
from .model_task import model_task_get_data, model_task_get_untreated
from loguru import logger
import json

model_api = Blueprint("model", __name__, url_prefix="/model")


@model_api.post("/extract/")
def extract():
    if request.content_type.startswith("application/json"):
        # 获取前端传来的json数据
        data = json.loads(request.get_json())
        # print(data)
        # 获取待模型提取的文本
        city = data["city"]
        content = data["content"]
        city = city.split(":")
        logger.info(f"城市列表 : {city}")
        logger.info(f"待模型提取的文本 : {content}")
        # 模型提取后并过滤的文本
        uie = UIE_Model()
        results = uie.predict(city, content)
        logger.info(f"模型提取并过滤的结果 : {results}")
        if not results:
            return {"status": "fail", "info": "未抽取相应结果"}
        return {"status": "success", "info": results}
    else:
        return {"status": "fail", "info": "错误的数据格式"}
