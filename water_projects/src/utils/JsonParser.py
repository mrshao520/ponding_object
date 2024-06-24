import json
from loguru import logger


from src.utils.Path import current_path

class JsonParser():
    config = {}
    cities_dict = {} # 超大型城市和大型城市
    channels_dict = {} # 检索渠道
    city_volume_dict = {} # 城市近五年历史数据
    # city_data_pie = []
    # city_year_bar = []
    
    server_dict = {} # 服务器配置
    
    def __init__(self) -> None:
        pass

    @staticmethod
    def prepare():
        # 解析json文件，为后续做准备
        JsonParser.config = {}
        JsonParser.cities_dict = {} # 超大型城市和大型城市
        JsonParser.channels_dict = {} # 检索渠道
        JsonParser.city_volume_dict = {} # 城市近五年历史数据
        JsonParser.server_dict = {} # 服务器配置
        JsonParser.parse_config()
        JsonParser.parse_city_volume()
        
        
    @staticmethod
    def parse_config():
        with open(current_path + "/documents/config.json", 'r', encoding='utf-8') as f:
            load_dict = json.load(f)
            print(load_dict)
        JsonParser.config = load_dict
        JsonParser.cities_dict = load_dict['城市']
        JsonParser.channels_dict['采集渠道'] = load_dict['采集渠道']
        server_dict = load_dict['server']
        JsonParser.server_dict['url'] = server_dict['address'] + ':' + server_dict['port']
        JsonParser.server_dict['login'] = JsonParser.server_dict['url'] + server_dict['login']
        JsonParser.server_dict['predict'] = JsonParser.server_dict['url'] + server_dict['predict']
        JsonParser.server_dict['query'] = JsonParser.server_dict['url'] + server_dict['query']
        JsonParser.server_dict['delete'] = JsonParser.server_dict['url'] + server_dict['delete']
        JsonParser.server_dict['query_summary'] = JsonParser.server_dict['url'] + server_dict['query_summary']
        
        logger.info(f"城市信息： {JsonParser.cities_dict}")
        logger.info(f"检索渠道：{JsonParser.channels_dict}")
        logger.info(f"服务配置：{JsonParser.server_dict}")
    
    # def parse_cities(self):
    #     with open(current_path + "/documents/cities.json", 'r', encoding='utf-8') as f:
    #         load_dict = json.load(f)
    #     JsonParser.cities_dict = load_dict
        
    
    # def parse_channels(self):
    #     with open(current_path + "/documents/channels.json", 'r', encoding='utf-8') as f:
    #         load_dict = json.load(f)   
    #     JsonParser.channels_dict = load_dict
    #     print(f"channels : {JsonParser.channels_dict}")
    
    @staticmethod
    def parse_city_volume():
        with open(current_path + "/documents/city_volume.json", 'r', encoding='utf-8') as f:
            load_dict = json.load(f)   
        JsonParser.city_volume_dict = load_dict
        logger.info(f"积水点历史数据 : {JsonParser.city_volume_dict}")
        # # 解析json文件
        # for key, value in load_dict.items():
        #     # 画饼状图，获取总值
        #     temp = {'value' : value.get("total", 0), 'name' : key}
        #     # 画柱状图，获取每一年的值
        #     templist = {'name' : key, 'data' : [j  for i, j in value.items() if i != 'total']}
        #     print(f'templist : {templist}')
        #     JsonParser.city_data_pie.append(temp)
        #     JsonParser.city_year_bar.append(templist)
        # print(f'city_data_pie : {JsonParser.city_data_pie}')
        
    @staticmethod
    def save_city_volume():
        with open(current_path + "/documents/city_volume.json", 'w', encoding='utf-8') as f:
            json_str = json.dumps(JsonParser.city_volume_dict, ensure_ascii=False)
            f.write(json_str)   
        logger.info(f'积水点历史数据保存成功')
    
    # def parse_server(self):
    #     with open(current_path + "/documents/server.json", 'r', encoding='utf-8') as f:
    #         load_dict = json.load(f)
    #     server_dict = load_dict['server']
    #     JsonParser.server_dict['url'] = server_dict['address'] + ':' + server_dict['port']
    #     JsonParser.server_dict['login'] = JsonParser.server_dict['url'] + server_dict['login']
    #     JsonParser.server_dict['predict'] = JsonParser.server_dict['url'] + server_dict['predict']