from PyQt5 import QtCore, QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import QSize
from loguru import logger


from src.utils.JsonParser import JsonParser

class QtWebView(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.data = []  # 表格数据
        self.webView = QWebEngineView(self)
        self.webView.page().setBackgroundColor(QtCore.Qt.GlobalColor.transparent)
        self.webView.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        layout.addWidget(self.webView)
        self.zoomFactor = 0.8
        self.resizeZoomFactor = 0.1
        # self.webView.loadFinished.connect(self.loadFinished)
        
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        try:
            size = QSize(a0.size().width(), a0.size().height())
            content_size = self.webView.page().contentsSize()
            # print(f"content width : {content_size.width()}  height : {content_size.height()}")
            # print(f"widget width : {size.width()}  height : {size.height()}")
            factor = min(size.width() / content_size.width(), size.height() / content_size.height())
            # print(f"factor : {factor}")
            self.webView.setZoomFactor(factor - self.resizeZoomFactor)
        except:
            logger.debug("webview : not set url!!!")
            
    # def paintEvent(self, a0: QtGui.QResizeEvent) -> None:
    #     try:
    #         size = QSize(a0.size().width(), a0.size().height())
    #         content_size = self.webView.page().contentsSize()
    #         # print(f"content width : {content_size.width()}  height : {content_size.height()}")
    #         # print(f"widget width : {size.width()}  height : {size.height()}")
    #         factor = min(size.width() / content_size.width(), size.height() / content_size.height())
    #         # print(f"factor : {factor}")
    #         self.webView.setZoomFactor(factor - 0.1)
    #     except:
    #         print("not set url!!!")
        
    def load(self, url: QtCore.QUrl) -> None:
        self.url = url
        self.webView.load(url)
        self.webView.setZoomFactor(self.zoomFactor)
    
    def updateData(self, data):
        jscode = f"updateData({data})"
        # 更新数据
        self.webView.page().runJavaScript(jscode, self.jsCallBack)
    
    # 只用于地图显示页面
    '''
    data  example {{'北京':{depth:15}},}
    '''
    def setOverThresholdData(self, data):
        for res,value in data.items():
            logger.info(f'key : {res}')
            tmpValue = JsonParser.city_volume_dict.get(res, {})
            logger.info(f'value : {tmpValue}')
            if tmpValue:
                data[res]['position'] = tmpValue['position']
                logger.info(f'position : {tmpValue}')
        logger.info(f'获取位置信息后的数据 : {data}')
        
        self.updateOverThresholdData(data)
        
    # 只用于地图显示页面
    def updateOverThresholdData(self, data):
        jscode = f"setOverThresholdData({data})"
        # 更新数据
        self.webView.page().runJavaScript(jscode, self.jsCallBack)
        
    # 只用于地图显示页面
    def message(self, info, info_type, duration):
        """
        MESSAGE: 'message', // 普通
        SUCCESS: 'success', // 成功
        ERROR: 'error', // 错误
        WARNING: 'warning' // 警告
        """
        information = {'content':info, 'type': info_type, 'duration': duration}
        jscode = f"message({information})"
        # 更新数据
        self.webView.page().runJavaScript(jscode, self.jsCallBack)
        
    def setData(self, data):
        self.data = data
    
    def jsCallBack(self, result):
        logger.info(f'result : {result}')

    def loadFinished(self):
        self.updateData(self.data)