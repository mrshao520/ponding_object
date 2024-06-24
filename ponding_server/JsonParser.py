import json
from loguru import logger

class JsonParser():
    
    API_KEY = ''
    
    @staticmethod
    def prepare():
        with open("./config.json", 'r', encoding='utf-8') as f:
            load_dict = json.load(f)
        JsonParser.API_KEY = load_dict['API_KEY']
        logger.info(f'高德地图API_KEY : {JsonParser.API_KEY}')