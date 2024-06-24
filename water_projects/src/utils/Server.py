from loguru import logger
import requests
import json


from src.utils.JsonParser import JsonParser

class ServerBase():
    headers = {'Content-type': 'application/json;charset=UTF-8'}
    login_url = JsonParser.server_dict.get('login', 'http://local:5000/login')
    predict_url = JsonParser.server_dict.get('predict', 'http://local:5000/predict')
    query_url = JsonParser.server_dict.get('query', 'http://local:5000/query')
    delete_url = JsonParser.server_dict.get('delete', 'http://local:5000/delete')
    query_summary_url = JsonParser.server_dict.get('query_summary', 'http://local:5000/query_summary')
    
    @staticmethod
    def update():
        ServerBase.headers = {'Content-type': 'application/json;charset=UTF-8'}
        ServerBase.login_url = JsonParser.server_dict.get('login', 'http://local:5000/login')
        ServerBase.predict_url = JsonParser.server_dict.get('predict', 'http://local:5000/predict')
        ServerBase.query_url = JsonParser.server_dict.get('query', 'http://local:5000/query')
        ServerBase.delete_url = JsonParser.server_dict.get('delete', 'http://local:5000/delete')
        ServerBase.query_summary_url = JsonParser.server_dict.get('query_summary', 'http://local:5000/query_summary')

class Server(ServerBase):
    def __init__(self) -> None:
        logger.info(f'login_url : {self.login_url}')
        logger.info(f'predict_url : {self.predict_url}')
        logger.info(f'query_url : {self.query_url}')
        logger.info(f'delete_url : {self.delete_url}')
    
    # @return true 与服务建立连接
    def connect(self)->bool:
        try:
            results = requests.get(self.login_url, headers=self.headers)
        except:
            return False
        if results.status_code == 200:
            return True
        else:
            return False
        
    def predict(self, city, texts:list)->list:
        json_str = json.dumps({'city': city, 'content' : texts})
        results = requests.post(self.predict_url, json=json_str, headers=self.headers)
        res_json = json.loads(results.text)
        if res_json['status'] == 'success':
            return res_json['info']
        else:
            return []

    def query(self, city, startTime, endTime):
        json_str = json.dumps({'city': city, 'start_time' : startTime, 'end_time' : endTime})
        results = requests.post(self.query_url, json=json_str, headers=self.headers)
        res_json = json.loads(results.text)
        if res_json['status'] == 'success':
            return res_json['info']
        else:
            return []
        
    def query_summary(self):
        results = requests.post(self.query_summary_url, headers=self.headers)
        res_json = json.loads(results.text)
        if res_json['status'] == 'success':
            return res_json['info']
        else:
            return {}
    
    def delete(self, id_list:list):
        json_str = json.dumps({'content' : id_list})
        results = requests.post(self.delete_url, json=json_str, headers=self.headers)
        res_json = json.loads(results.text)
        if res_json['status'] == 'success':
            return True
        else:
            return False
    
# if __name__ == "__main__":
#     jsonParser = JsonParser()
#     jsonParser.prepare()
#     server = Server()
#     server.connect()
#     res = server.predict(['丰台区看丹南路积水最深达60厘米，下午2点恢复通行 #北京暴雨 #强降雨 #丰台区看丹南路积水最深达60厘米,发布时间：2023-07-31 18:42'])
#     # {'info': [{'地点': '丰台区看丹南路', '城市': '北京', '描述': '', '日期': '2023-07-31 18:42', 
#     # '时间': '2023-07-31 18:42', '深度值': '60厘米', '经纬度': '116.407387,39.904179'}], 'status': 
#     # 'success'}    
# print(res)
    
    