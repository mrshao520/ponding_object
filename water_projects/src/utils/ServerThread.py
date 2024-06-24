from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread
from enum import Enum
import queue

from src.utils.Server import Server, ServerBase

queue.Queue()

class ServerTypes(Enum):
    PredictServer = 1
    QueryServer = 2
    DeleteServer = 3
    QuerySummaryServer = 4
    

class ServerThread(QThread):
    # update_text = QtCore.pyqtSignal(list)
    return_results_list = QtCore.pyqtSignal(list)
    return_results_dict = QtCore.pyqtSignal(dict)
    return_results_bool = QtCore.pyqtSignal(bool)
    
    info_box = QtCore.pyqtSignal(str, str)
    
    def __init__(self, parent: QObject = None, type: ServerTypes = None) -> None:
        super().__init__(parent)
        self.texts = []
        self.city = ''
        self.serverType = type
        self.server = Server()
        
        self.connectTimes = 0
        
    def run(self):
        
        if not self.server.connect():
            if self.connectTimes == 0:
                self.connectTimes += 1
                self.info_box.emit("info", "无法连接服务，请检查网络！！！")
            else:
                self.connectTimes = 0
                self.info_box.emit("info", "无法连接服务，请检擦配置文件！！！")
            return
        
        if self.serverType == ServerTypes.PredictServer:
            results = self.server.predict(self.city, self.texts)
            self.output(results)
        elif self.serverType == ServerTypes.QueryServer:
            results = self.server.query(self.city, self.startTime, self.endTime)
            self.output(results)
        elif self.serverType == ServerTypes.DeleteServer:
            results = self.server.delete(self.id_list)
            self.return_results_bool.emit(results)
        elif self.serverType == ServerTypes.QuerySummaryServer:
            results = self.server.query_summary()
            self.return_results_dict.emit(results)
        
    # 调用模型接口
    def setTexts(self, city, texts:list):
        self.city = city
        self.texts = texts
    
    # 查询数据库
    def setQueryData(self, city, startTime, endTime):
        self.city = city
        self.startTime = startTime
        self.endTime = endTime
    
    # 根据 id 进行删除
    def setDeleteData(self, id_list):
        self.id_list = id_list
        
    def connect(self)->bool:
        return self.server.connect()
        
    def output(self, content:list):
        self.return_results_list.emit(content)