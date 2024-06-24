from flask import Flask
from flask import request
from flask import jsonify
from UIE_Model import UIE_Model
from UIE_Model2 import UIE_Model as UIE_Model2
from JsonParser import JsonParser
from loguru import logger
from PondingTable import OperatePonding
import json

app = Flask(__name__)
app.json.ensure_ascii = False

@app.route('/')
def default():
    return jsonify({'status':'success'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    return jsonify({'status':'success'})

"""
application/json
"""
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if request.content_type.startswith('application/json'):
            # 获取前端传来的json数据
            data = json.loads(request.get_json())
            # print(data)
            # 获取待模型提取的文本
            city = data['city']
            content = data['content']
            logger.info(f'城市 : {city}')
            logger.info(f'待模型提取的文本 : {content}')
            # 模型提取后并过滤的文本
            uie = UIE_Model()
            results = uie.predict(city, content) 
            logger.info(f'模型提取并过滤的结果 : {results}')
            if not results:
                return jsonify({'status' : 'fail',
                            'info' : '未抽取相应结果'})
            # 保存到数据库  
            op = OperatePonding()
            op.insert_ponding_data_dedup(results)
            return jsonify({'status' : 'success',
                            'info' : results})
        else:
            return jsonify({'status' : 'fail',
                            'info' : '错误的数据格式'})
    
    else:
        return jsonify({'status':'fail',
                        'info' : '错误的请求方式'})

"""
application/json
"""
@app.route('/extract/', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        if request.content_type.startswith('application/json'):
            # 获取前端传来的json数据
            data = json.loads(request.get_json())
            # print(data)
            # 获取待模型提取的文本
            city = data['city']
            content = data['content']
            logger.info(f'城市 : {city}')
            logger.info(f'待模型提取的文本 : {content}')
            # 模型提取后并过滤的文本
            uie = UIE_Model2()
            results = uie.predict(city, content) 
            logger.info(f'模型提取并过滤的结果 : {results}')
            if not results:
                return jsonify({'status' : 'fail',
                            'info' : '未抽取相应结果'})
            # 保存到数据库  
            # op = OperatePonding()
            # op.insert_ponding_data_dedup(results)
            return jsonify({'status' : 'success',
                            'info' : results})
        else:
            return jsonify({'status' : 'fail',
                            'info' : '错误的数据格式'})
    
    else:
        return jsonify({'status':'fail',
                        'info' : '错误的请求方式'})

"""
application/json
"""
@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        if request.content_type.startswith('application/json'):
            # 获取前端传来的json数据
            data = json.loads(request.get_json())
            # print(data)
            # 获取待模型提取的文本
            city = data['city']
            startTime = data['start_time']
            endTime = data['end_time']
            logger.info(f'城市 : {city}')
            logger.info(f'开始时间 : {startTime}')
            logger.info(f'结束时间 : {endTime}')
            # 查询数据库  
            op = OperatePonding()
            results = op.query_ponding_data(city, startTime, endTime)
            return jsonify({'status' : 'success',
                            'info' : results})
        else:
            return jsonify({'status' : 'fail',
                            'info' : '错误的数据格式'})
    
    else:
        return jsonify({'status':'fail',
                        'info' : '错误的请求方式'})
        
"""
application/json
"""
@app.route('/query_summary', methods=['GET', 'POST'])
def query_summary():
    if request.method == 'POST':
        if request.content_type.startswith('application/json'):
            # # 获取前端传来的json数据
            # data = json.loads(request.get_json())
            # # print(data)
            # # 获取待模型提取的文本
            # city = data['city']
            # startTime = data['start_time']
            # endTime = data['end_time']
            # logger.info(f'城市 : {city}')
            # logger.info(f'开始时间 : {startTime}')
            # logger.info(f'结束时间 : {endTime}')
            # 查询数据库  
            op = OperatePonding()
            results = op.query_summary_data()
            return jsonify({'status' : 'success',
                            'info' : results})
        else:
            return jsonify({'status' : 'fail',
                            'info' : '错误的数据格式'})
    
    else:
        return jsonify({'status':'fail',
                        'info' : '错误的请求方式'})
        
"""
application/json
"""
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        if request.content_type.startswith('application/json'):
            # 获取前端传来的json数据
            data = json.loads(request.get_json())
            # print(data)
            # 获取待模型提取的文本
            content = data['content']
            logger.info(f'要删除的内容 : {content}')
            # 查询数据库  
            op = OperatePonding()
            results = op.delete_ponding_data(content)
            return jsonify({'status' : 'success',
                            'info' : results})
        else:
            return jsonify({'status' : 'fail',
                            'info' : '错误的数据格式'})
    
    else:
        return jsonify({'status':'fail',
                        'info' : '错误的请求方式'})

if __name__ == "__main__":
    
    trace = logger.add('./log/waterlogging.log', rotation = '00:00', retention = '7 days',
                       format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}")
    
    logger.info('----------大城市暴雨积水多源数据实时采集处理系统----------')
    
    JsonParser.prepare()
    app.run(host='0.0.0.0', port=8886)