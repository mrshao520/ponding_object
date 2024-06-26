import fastdeploy
from fastdeploy.text import UIEModel, SchemaLanguage
from pear_admin.apis.function import get_location, format_time
from loguru import logger
from configs import BaseConfig
import csv
import re
import os


class UIE_Model:
    def __init__(self, model_dir=BaseConfig.MODEL_PATH, max_length=128, batch_size=1):
        self.runtime_option = self.build_option()
        model_path = os.path.join(model_dir, "inference.pdmodel")
        param_path = os.path.join(model_dir, "inference.pdiparams")
        vocab_path = os.path.join(model_dir, "vocab.txt")
        schema = BaseConfig.MODEL_SCHEMA
        self.uie = UIEModel(
            model_path,
            param_path,
            vocab_path,
            position_prob=0.5,
            max_length=max_length,
            schema=schema,
            batch_size=batch_size,
            runtime_option=self.runtime_option,
            schema_language=SchemaLanguage.ZH,
        )

    def build_option(self):
        # 获取系统中GPU的数量
        # device_count = fastdeploy.get_device_count("gpu")
        # 创建RuntimeOption，指定使用多个GPU
        # runtime_option = fastdeploy.RuntimeOption(device_type='gpu', device_id=list(range(device_count)))
        runtime_option = fastdeploy.RuntimeOption()
        # set device 指定使用的gpu
        runtime_option.use_gpu(device_id=BaseConfig.MODEL_DEVICE_ID)
        # set backend 指定需要推理的模型
        runtime_option.use_paddle_infer_backend()

        return runtime_option

    def predict(self, city: list, texts: list):
        results = self.uie.predict(texts, return_dict=True)
        return self.handle_results(city, results)

    def handle_results(self, cityName: list, results: list) -> list:
        """对模型的输出结果进一步处理

        Args:
            cityName (list): 城市列表 ["北京", "天津", "上海"]
            results (list): 模型结果

        Returns:
            list: 后处理结果
        """
        # 配置文件，保存的文件路径
        untreated_filename = BaseConfig.UNTREATED_FILENAME
        csv_filename = BaseConfig.CSV_FILENAME
        csv_headers = BaseConfig.CSV_HEADERS

        
        # logger.info(f"抽取后的结果 : {results}")
        handle_res = []
        for res in results:
            position = self.get_pos_data(res.get("地点", []))
            if not position:
                # 未抽取到地点
                logger.debug(f"未抽取到地点的结果 : {res}")
                continue
            city = self.get_valid_data(res.get("城市", []))
            if not city:
                # 未抽取到城市
                logger.debug(f"未抽取到城市的结果 : {res}")
                continue
            # 匹配城市
            match_city_name = False
            for city_name in cityName:
                if city_name in city:
                    # 统一城市名 例如 江苏省南京市 统一为 南京
                    city = city_name
                    match_city_name = True
                    break
            if not match_city_name:
                # 城市不匹配
                logger.debug(f"城市 {cityName} - {city} 不匹配的结果 :  {res}")
                continue

            date = self.get_valid_data(res.get("日期", ""))
            time = self.get_valid_data(res.get("时间", ""))

            if len(date) > 19:
                logger.debug(f"时间长度错误: {date} - length : {len(date)}")
                continue

            # -------------对时间特殊处理：固定格式 2023-07-18 08:23:01
            tmpDate = re.split("/", date)
            if len(tmpDate) > 2:
                # 时间格式为 2023/07/18 08:23:01
                date = "-".join(tmpDate)

            tmpDate = re.split("-", date)
            if len(tmpDate) < 2:
                logger.debug(f"error datetime format")
                continue

            for pos in position:
                pos["date"] = date
                pos["time"] = time
                pos["city"] = city
                # 获取经纬度
                if BaseConfig.MODEL_GET_LOCATION:
                    address = city + pos["position"]
                    lati_longi_tude = get_location(city=city, address=address)
                    if not lati_longi_tude:
                        logger.info(f"未获取正确的经纬度：{city}-{address}")
                        continue
                    longitude, latitude = lati_longi_tude.split(",", maxsplit=2)
                    pos["longitude"] = longitude
                    pos["latitude"] = latitude
                # 保存数据
                if BaseConfig.MODEL_SAVE_DATA:
                    ponding_list = [pos.get(header, None) for header in csv_headers]
                    # 打开CSV文件
                    with open(
                        csv_filename, mode="a", newline="", encoding="utf-8"
                    ) as csvfile:
                        # 创建CSV写入器
                        writer = csv.writer(csvfile)
                        # 如果CSV文件不存在，则写入列名
                        if not csvfile.tell():
                            writer.writerow(csv_headers)
                        # 写入数据
                        writer.writerow(ponding_list)
                # 添加结果    
                handle_res.append(pos)
        return handle_res

    def get_valid_data(self, values: list):
        if not values:
            # 未找到对应值
            return ""
        elif len(values) == 1:
            return values[0].get("text", "")
        else:
            # 根据probability获取最大值
            max_pro = 0.0
            text = ""
            for val in values:
                logger.info(val)
                tmp = val.get("probability", 0.0)
                if tmp > max_pro:
                    max_pro = tmp
                    text = val.get("text", "")
            return text

    def get_pos_data(self, values: list) -> list:
        if not values:
            # 未找到对应值
            return []
        pos_list = []
        for val in values:
            pos = val.get("text", "")
            relation = val.get("relation", {})
            describe = ""
            depth = ""
            if relation:
                describe = self.get_valid_data(relation.get("描述", ""))
                depth = self.get_valid_data(relation.get("深度值", ""))
            pos_list.append(
                {"position": pos, "description": describe, "depth_value": depth}
            )
        return pos_list