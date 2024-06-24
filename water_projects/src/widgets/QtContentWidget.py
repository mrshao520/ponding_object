from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QUrl, QTimer
from loguru import logger
import re

from src.widgets.Ui_content import Ui_Form
from src.utils.ServerThread import ServerThread, ServerTypes
from src.utils.Server import ServerBase
from src.utils.Path import current_path
from src.utils.JsonParser import JsonParser
from src.utils.ReptilesProcess import ReptilesProcess


def info_box(parent, title, value, delay=5):
    """
    消息盒子
    :param value: 显示的信息内容 
    :param title: 弹窗的标题 
    :param widget: 父窗口
    :param delay: 弹窗默认关闭时间， 单位：秒
    """
    msgBox = QMessageBox(parent=parent)
    
    msgBox.setStyleSheet('''
        QMessageBox {
            background-color: #F2F2F2; /* QMessageBox背景颜色 */
        }

        QMessageBox QLabel { /* textLabel */
            font: bold 20px;
            color: #298DFF;
            background-color: transparent;
            min-width: 310px; /* textLabel设置最小宽度可以相应的改变QMessageBox的最小宽度 */
            min-height: 60px; /* textLabel和iconLabel高度保持一致 */
        }

    ''')
    
    # 设置默认ICON
    msgBox.setWindowIcon(QtGui.QIcon(current_path + '/resources/images/warning.png'))
    
    msgBox.setWindowTitle(title)
    msgBox.setText(value)
    
    msgBox.setStandardButtons(QMessageBox.StandardButton.Yes)
    msgBox.setDefaultButton(QMessageBox.StandardButton.Yes)
    msgBox.button(QMessageBox.StandardButton.Yes).setMinimumSize(80, 45)
    # 设置 QMessageBox 自动关闭时长
    msgBox.button(QMessageBox.StandardButton.Yes).animateClick(1000 * delay)
    
    msgBox.exec()


class QtContentWidget(QWidget, Ui_Form):
    
    start_process = QtCore.pyqtSignal()
    
    
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        
        self.cityName = ""
        self.cityNameList = []
        
        ServerBase.update()
        
        self.setObjectName("QtContentWidget")
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("QTextEdit,QWebEngineView{background-color:rgba(0, 0, 0, 0.1);\
                                background-image:url(" + current_path + "/resources/images/line.png);  \
                                font-size: 16px; \
                                color: rgb(70,130,180)\
                            } \
                            QSplitter::handle{background-color:rgba(0, 0, 0, 0);} \
                            QPushButton{border-image:url("+current_path+"/resources/images/button.png);color:white; \
                                        font:bold 'DS-Digital';font-size:23px;} \
                            QPushButton:pressed{border-image:url("+current_path+"/resources/images/button_press.png);}  \
                            QCheckBox, QRadioButton{spacing: 5px;font-size: 23px; color:#aaaaff;font:'DS-Digital';} \
                            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked{image:url("+current_path+"/resources/images/uncheck.png);}\
                            QCheckBox::indicator:checked, QRadioButton::indicator:checked{image:url("+current_path+"/resources/images/check.png);} \
                            QScrollBar:Vertical{border-width:0px;border:none;background:rgba(64, 65, 79, 0); \
                                                width:12px;margin:0px 0px 0px 0px;} \
                            QScrollBar::handle:vertical{background: qlineargradient(x1:0, y1:0, x2:1, y2:0, \
                                                        stop: 0 #aaaaff, stop: 0.5 #aaaaff, stop: 1 #aaaaff);\
                                                        margin: 0 0px 0 0px;border-radius: 6px;}\
                            QScrollBar::add-line:vertical{background: qlineargradient(x1:0, y1:0, x2:1, y2:0, \
                                                            stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0)); \
                                                            height: 0px;border: none;subcontrol-position: bottom;subcontrol-origin: margin;} \
                            QScrollBar::sub-line:vertical {background: qlineargradient(x1:0, y1:0, x2:1, y2:0, \
                                                            stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0)); \
                                                            height: 0 px;border: none;subcontrol-position: top;subcontrol-origin: margin;} \
                            QScrollBar::sub-page:vertical {background: rgba(64, 65, 79, 0);} \
                            QScrollBar::add-page:vertical {background: rgba(64, 65, 79, 0);} \
                            QGroupBox{font:bold 19px; color:#aaaaff;font:'DS-Digital';border: 2px solid  #aaaaff;\
                                      border-radius:5px; margin-top:0px; } \
                            QGroupBox{subcontrol-origin:margin;subcontrol-position:top;padding:0 0px} \
                            QTableWidget{font:bold 15px; color:#aaaaff;font:'DS-Digital';border: 2px solid  #aaaaff;\
                                    border-radius:15px;background-color:rgba(0, 0, 0, 0);} \
                            QHeaderView::section{background-color:#aaaaff;} \
                            QDateTimeEdit, QDateEdit, QComboBox, QSpinBox{font:bold 20px; color:#aaaaff;font:'DS-Digital';border: 2px solid  #aaaaff;\
                                      border-radius:5px;background-color:rgba(0, 0, 0, 0.1)}   \
                        ")
        self.setupUi(self)
        
        self.contentSplitter.setSizes([2000, 4000, 2000])
        self.leftSplitter.setSizes([8000, 1000, 8000])
        self.centerSpplitter.setSizes([1000, 6000, 3000])  # 1 6 3
        self.splitter.setSizes([6000, 1000, 1000])
        self.rightSplitter.setSizes([1000, 3000, 1000, 3000])
        
        # chart 1
        path = current_path + "/resources/html/city_volume_pie.html"
        # self.chart1.setData(JsonParser.city_data_pie)
        self.chart1.setData(JsonParser.city_volume_dict)
        # 页面完全加载后调用loadFinished
        self.chart1.webView.loadFinished.connect(self.chart1.loadFinished)
        self.chart1.load(QUrl(path))
        
        
        # chart 2
        # path = current_path + "/resources/html/wordcloud.html"
        # self.chart2.load(QUrl(path))
        
        path = current_path + "/resources/html/map.html"
        logger.info(f'QtMainWidget : width {parent.width()}  -  height {parent.height()}')
        self.chinaMap.zoomFactor = parent.height() / 900
        self.chinaMap.resizeZoomFactor = -0.6
        self.chinaMap.setData(JsonParser.city_volume_dict)
        # 页面完全加载后调用loadFinished
        self.chinaMap.webView.loadFinished.connect(self.chinaMap.loadFinished)
        self.chinaMap.load(QUrl(path))
        
        
        # city chart
        path = current_path + "/resources/html/city_year_bar.html"
        self.cityChart.setData(JsonParser.city_volume_dict)
        # 页面完全加载后调用loadFinished
        self.cityChart.webView.loadFinished.connect(self.cityChart.loadFinished)
        self.cityChart.load(QUrl(path))
        
        
        # 绑定 city button 槽函数
        self.cityRadioButtonGroup.buttonClicked[int].connect(self.slotButtonGroupClicked)
        
        # 自动检索绑定槽函数
        self.autoSearchCheckBox.stateChanged.connect(self.slotAutoSearchCheckBox)
        self.autoSearchTimer = QTimer()
        self.autoSearchTimer.timeout.connect(self.slotAutoSearch)
        self.autoTime = 0
        
        self.start_process.connect(self.startReptile)
        
        # 绑定槽函数
        
        # self.reptileThread = ReptilesThread(self)
        self.reptileThread = ReptilesProcess(self)
        self.reptileThread.update_text.connect(self.updateText)
        self.reptileThread.started.connect(self.startThread)
        self.reptileThread.finished.connect(self.finishThread)
        
        self.reptileThread.quit_thread.connect(self.info_box)
        
        self.start.clicked.connect(self.startReptile)
        self.end.clicked.connect(self.endReptile)
        
        self.serverThread = ServerThread(self, ServerTypes.PredictServer)
        self.serverThread.return_results_list.connect(self.updateResults)
        self.serverThread.started.connect(self.startServerThread)
        self.serverThread.finished.connect(self.finishServerThread)
        # self.connectTimes = 0
        
        self.startHandle.clicked.connect(self.startHandleTexts)
        self.saveResults.clicked.connect(self.saveResultsTexts)
        
        # -------------------- 查询与删除 -----------------
        self.queryServer = ServerThread(self, ServerTypes.QueryServer)
        self.queryServer.return_results_list.connect(self.queryUpdateResults)
        
        self.deleteServer = ServerThread(self, ServerTypes.DeleteServer)
        self.deleteServer.return_results_bool.connect(self.deleteUpdateResults)
        
        self.queryButton.clicked.connect(self.queryByCityTime)
        self.deleteButton.clicked.connect(self.deleteChosedData)
        
        # ----------------- query summary table ------------------
        self.querySummaryServer = ServerThread(self, ServerTypes.QuerySummaryServer)
        self.querySummaryServer.return_results_dict.connect(self.querySummaryResults)
        
        # 预处理文本
        self.pretreatTexts = []
        # 处理后结果
        self.processResults = []
        
        
        # 定时检索 循环次数
        self.cycleIndex = 0
        # 定时检索 循环总数
        self.cycleCount = 0
        
        self.autoUpdateTimer = QTimer()
        self.autoUpdateTimer.timeout.connect(self.slotUpdateTime)
        self.autoUpdateTimer.start(1000)
        
        self.serverThread.info_box.connect(self.info_box)
        self.queryServer.info_box.connect(self.info_box)
        self.deleteServer.info_box.connect(self.info_box)
        self.querySummaryServer.info_box.connect(self.info_box)
        
        self.querySummaryServer.start()
        
        # self.querySummaryTimer = QTimer(self)
        # self.querySummaryTimer.setSingleShot(True)
        # self.querySummaryTimer.timeout.connect()
    
    def updateText(self, content):
        # cursor = self.result.textCursor()
        # cursor.movePosition(QTextCursor.MoveOperation.End)
        # self.result.setTextCursor(cursor)
        # self.result.insertPlainText(str(content))
        # 保存检索到的数据
        content = str(content)
        logger.info(f'检索到的数据 : {content}')
        if content[:4] == '检索失败':
            info_list = content.split('-')
            if len(info_list) == 4:
                time = JsonParser.config['message'].get(info_list[1], 10)
                logger.info(f'message duration : {time}')
                self.chinaMap.message(f'检索渠道:{info_list[2]}\n具体信息:{info_list[3]}', 
                                      info_list[1], time * 1000)
        else:
            if len(content) > 20:
                self.pretreatTexts.append(content)
            self.result.append(content)
        
    def updateResults(self, results):
        
        overValue = {}
        max_value = JsonParser.config['depth_threhold']
        logger.info(f'depth_threhold : {max_value}')

        self.processResults = results
        for result in results:
            row_count = self.process.rowCount()
            # print(f"row_count : {row_count}")
            self.process.insertRow(row_count)
            # ['日期', '时间', '城市', '地点', '经纬度', '积水深度值','备注信息']
            self.process.setItem(row_count, 0, QTableWidgetItem(result.get('日期', '')))
            self.process.setItem(row_count, 1, QTableWidgetItem(result.get('时间', '')))
            self.process.setItem(row_count, 2, QTableWidgetItem(result.get('城市', '')))
            self.process.setItem(row_count, 3, QTableWidgetItem(result.get('地点', '')))
            #self.process.setItem(row_count, 4, QTableWidgetItem(result.get('经纬度', '')))
            self.process.setItem(row_count, 4, QTableWidgetItem(result.get('深度值', '')))
            self.process.setItem(row_count, 5, QTableWidgetItem(result.get('描述', '')))
            
            tmpDepth = result.get('深度值', '')
            # tmpDepth = '50cm'
            if tmpDepth != '':
                value = self.uniteValue(tmpDepth)
                # value = 20
                if value > max_value:
                    overValue[result.get('城市', '')] = {'depth' : value}
                    
        if overValue:
            # 更新地图
            logger.info(f'超过阈值的数据 : {overValue}')
            time = JsonParser.config['message'].get('warning', 10)
            logger.info(f'duration : {time}')
            self.chinaMap.message(f'积水深度值超过阈值:{overValue}', 'warning', time * 1000)
            self.chinaMap.setOverThresholdData(overValue)
            
    def queryUpdateResults(self, results):
        logger.info('查询到的数据')
        for result in results:
            
            logger.info(result)
            
            row_count = self.queryResults.rowCount()
            # print(f"row_count : {row_count}")
            self.queryResults.insertRow(row_count)
            # ['id', '日期', '时间', '城市', '地点', '经纬度', '积水深度值','备注信息']
            self.queryResults.setItem(row_count, 0, QTableWidgetItem(str(result.get('id', ''))))
            self.queryResults.setItem(row_count, 1, QTableWidgetItem(result.get('日期', '')))
            self.queryResults.setItem(row_count, 2, QTableWidgetItem(result.get('时间', '')))
            self.queryResults.setItem(row_count, 3, QTableWidgetItem(result.get('城市', '')))
            self.queryResults.setItem(row_count, 4, QTableWidgetItem(result.get('地点', '')))
            #self.process.setItem(row_count, 5, QTableWidgetItem(result.get('经纬度', '')))
            self.queryResults.setItem(row_count, 5, QTableWidgetItem(result.get('深度值', '')))
            self.queryResults.setItem(row_count, 6, QTableWidgetItem(result.get('描述', '')))
            
    def deleteUpdateResults(self, results):
        if results:
            self.info_box('info', '删除成功！！！')
        else:
            self.info_box('error', '删除失败！！！')
            
    def querySummaryResults(self, results:dict):
        logger.info('查询summary table数据')
        tmp = {}
        for k in results.keys():
            if k in JsonParser.city_volume_dict:
                if 'position' in JsonParser.city_volume_dict[k]:
                    tmp[k] = results[k]
                    tmp[k]['position'] = JsonParser.city_volume_dict[k]['position']
                
        JsonParser.city_volume_dict = tmp
        JsonParser.save_city_volume()
        self.update_webview()
            
    # 开始检索
    def startReptile(self):
        # 获取选择的渠道
        channelList = self.getCheckBoxList()
        
        # 获取开始时间和结束时间
        startTime = ''
        endTime = ''
        
        if self.realTimeCheckBox.isChecked(): 
            if self.cycleIndex == 0:
                pass
            else:
                total = self.autoTime * self.cycleCount # 总共间隔的时间
                hour = total // 60
                min = total % 60
                if hour >= 24:
                    self.cycleCount = 0
                time = QtCore.QDateTime(QtCore.QDate.currentDate(), QtCore.QTime(hour, min, 0))
                self.cycleCount += 1
                print(time.toString())
                self.startRelTimeDate.setDateTime(time)
            startTime = self.startRelTimeDate.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            endTime = self.endRelTimeTimeDate.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            if startTime > endTime:
                info_box(self, "定时采集", "开始时间已超出结束时间，停止定时采集！")
                self.autoSearchCheckBox.setCheckState(QtCore.Qt.CheckState.Unchecked)
                return
            
        elif self.historyTimeCheckBox.isChecked():
            startTime = self.startHisTimeDate.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            endTime = self.endHisTimeTimeDate.dateTime().toString('yyyy-MM-dd HH:mm:ss')
            
        else:
            info_box(self, "采集属性设置", "请选择想要的采集属性！")
            return
        
        
        if self.reptileThread.isRunning():
            # QMessageBox.warning(self, "error", "请耐心等候检索完成！！！", QMessageBox.StandardButton.Yes)    
            info_box(self, "error", "请耐心等候采集完成！！！")
            return 
        
        if self.serverThread.isRunning():
            info_box(self, "error", "请耐心等候模型处理!！！")
            return 
        
        if self.cityName == "" or not channelList:
            # QMessageBox.warning(self, "info", "请选择城市和检索渠道！！！", QMessageBox.StandardButton.Yes)    
            info_box(self, "info", "请选择城市和采集渠道！！！")
            return
        
        if startTime and endTime and startTime > endTime:
            # QMessageBox.warning(self, "info", "开始时间大于结束时间，请重新选择！", QMessageBox.StandardButton.Yes)  
            info_box(self, "info", "开始时间大于结束时间，请重新选择！")
            return
        
        # 表格 ： 清空所有行
        self.process.setRowCount(0)
        # self.process.clear()
        # self.process.setHorizontalHeaderLabels(['时间', '地点', '经纬度', '备注信息'])
        
        # 文本框 ：清空所有内容
        self.result.clear()
        self.result.append("开始采集")
        
        # 清空检索到的数据
        self.pretreatTexts = []
        # 清空处理后的结果
        self.processResults = []
        
        logger.info(f'开始检索')
        logger.info(f'选取的城市: {self.cityName}')
        logger.info(f'检索渠道: {channelList}')
        logger.info(f'开始时间: {startTime}')
        logger.info(f'结束时间: {endTime}')
        
        # self.reptileThread.updateData(self.cityName, channelList, startTime, endTime)
        # self.reptileThread.start()
        self.reptileThread.updateData(self.cityName, channelList, startTime, endTime)
        self.reptileThread.start_process()
    
    # 停止检索
    def endReptile(self): 
        if self.autoSearchCheckBox.isChecked():
            self.autoSearchCheckBox.setCheckState(QtCore.Qt.CheckState.Unchecked)
        logger.info("结束检索")     
        if self.reptileThread.isRunning():
            logger.info("reptileThread isRunning 结束检索")   
            self.reptileThread.end_process()
            
    def startHandleTexts(self):
        if self.reptileThread.isRunning():
            info_box(self, 'info', '请耐心等待采集完成！！！')
            return
        
        if self.serverThread.isRunning():
            info_box(self, "error", "请耐心等候模型处理！！！")
            return 
        
        if not self.pretreatTexts and self.processResults:
            info_box(self, 'info', '已处理完成，请点击保存！')
            return

        if not self.pretreatTexts:
            info_box(self, 'info', '暂无预处理数据，请稍后尝试！')
            return
            
        # if not self.serverThread.connect():
        #     if self.connectTimes == 0:
        #         self.connectTimes += 1
        #         info_box(self, "info", "无法连接服务，请检查网络！！！")
        #     else:
        #         self.connectTimes = 0
        #         info_box(self, "info", "无法连接服务，请检擦配置文件！！！")
        #     return
                
        self.serverThread.setTexts(self.cityName, self.pretreatTexts)
        self.pretreatTexts = []
        self.serverThread.start()
        
    def update_webview(self):
        self.chart1.updateData(JsonParser.city_volume_dict)
        self.chinaMap.updateData(JsonParser.city_volume_dict)
        self.cityChart.updateData(JsonParser.city_volume_dict)
    
    def saveResultsTexts(self):
        if self.reptileThread.isRunning():
            info_box(self, 'info', '请耐心等待采集完成！！！')
            return
        
        if self.serverThread.isRunning():
            info_box(self, "error", "请耐心等候模型处理！！！")
            return 
        
        if not self.processResults and self.pretreatTexts:
            info_box(self, 'info', '请先进行模型处理！')
            return
        
        if not self.processResults:
            info_box(self, 'info', '暂无可保存数据，请稍后尝试！')
            return
        
        logger.info('保存结果')
        for res in self.processResults:
            city = res.get('城市', '')
            date = res.get('日期', '')[0: 4]
            
            if city in JsonParser.city_volume_dict:
                tmp_dict = JsonParser.city_volume_dict[city]
                if date in tmp_dict:
                    tmp_dict[date] += 1
                else:
                    tmp_dict[date] = 1
                tmp_dict['total'] += 1
        self.update_webview()
        JsonParser.save_city_volume()
        self.processResults = []
        print(JsonParser.city_volume_dict)
            
    
    def slotButtonGroupClicked(self, id):
        cityname = ""
        try:
            if id < len(self.bigCityList):
                cityname = self.bigCityList[id]
            else:
                cityname = self.normalCityList[id - len(self.bigCityList)]
        except:
            logger.debug("can't find the city name!")
        # print(f"button group clicked : {id} - {cityname}")
        
        # 只选择一个城市
        self.cityName = cityname
        logger.info(f'选取城市: {cityname}')
        
        # 可以选择多个城市
        # temRadioButton = self.cityRadioButtonMap[cityname]
        # if temRadioButton.isChecked():
        #     self.cityNameList.append(cityname)
        #     print(f"button group clicked : {id} - {cityname}")
        # else:
        #     if cityname in self.cityNameList:
        #         self.cityNameList.remove(cityname)
        #     print(f"button group unclicked : {id} - {cityname}")
        # print(f'city name list: {self.cityNameList}')
        
    def getCheckBoxList(self):
        tempList = []
        for i in range(len(self.checkBoxList)):
            temp = self.checkBoxList[i]
            if temp.isChecked():
                tempList.append(temp.text())
        logger.info(f"checked check box : {tempList}")    
        return tempList
    
    def startThread(self):
        self.result.append(f"采集线程正在运行!!!")
        
    def finishThread(self):
        logger.info(f'采集线程运行结束')
        self.result.append(f"采集线程运行结束!!!")
        
        # 爬虫结束，如果是自动检索，就进行模型处理
        if self.cycleIndex != 0:
            self.startHandleTexts()
            
    def startServerThread(self):
        self.result.append(f"上传服务线程正在运行!!!")
        
    def finishServerThread(self):
        self.result.append(f"上传服务线程运行结束!!!")
        
        # 模型处理结束，如果是自动检索，就保存结果
        if self.cycleIndex != 0:
            self.saveResultsTexts()
       
    # 自动检索槽函数 
    def slotAutoSearchCheckBox(self):
        autoTime = self.autoTimeSpinBox.value()
        logger.info(f'定时采集时间 : {autoTime}')
        
        if self.autoSearchCheckBox.isChecked():
            logger.info(f'auto search check box checked!')
            if not self.autoSearchTimer.isActive() or self.autoTime != autoTime:
                self.autoTime = autoTime
                self.autoSearchTimer.start(self.autoTime * 60 * 1000)
                self.slotAutoSearch()
        else:
            logger.info(f'auto search check box unchecked!')
            self.cycleIndex = 0
            self.autoSearchTimer.stop()
            
    def slotAutoSearch(self):
        if self.reptileThread.isRunning():
            info_box(self, '定时采集' , '正在采集，等待一个周期！')
        else:
            logger.info(f'开始采集！')
            self.cycleIndex += 1
            # self.startReptile()
            self.start_process.emit()
            
    def slotUpdateTime(self):
        self.endRelTimeTimeDate.setDateTime(QtCore.QDateTime.currentDateTime())
            
    def info_box(self, title, value):
        info_box(self, title, value)
        
    def update(self):
        logger.info('正在更新主页面')
        ServerBase.update()
        
        self.querySummaryServer.start()  
        
        for i in range(self.checkBoxLayout.count()):
            self.checkBoxLayout.itemAt(i).widget().deleteLater()
        
        self.checkBoxList.clear()
        self.channelsList = JsonParser.channels_dict.get("采集渠道", [])
        for i in range(len(self.channelsList)):
            row = i // 2
            col = i % 2
            tempCheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
            tempCheckBox.setObjectName(self.channelsList[i])
            tempCheckBox.setText(self.channelsList[i])
            self.checkBoxButtonGroup.addButton(tempCheckBox, i)
            self.checkBoxList.append(tempCheckBox)
            self.checkBoxLayout.addWidget(tempCheckBox, row, col, 1, 1)
        
        for i in range(self.bigCityBoxLayout.count()):
            self.bigCityBoxLayout.itemAt(i).widget().deleteLater()
            
        for i in range(self.normalCityBoxLayout.count()):
            self.normalCityBoxLayout.itemAt(i).widget().deleteLater()
            
        self.cityRadioButtonMap.clear()
        
        index = 0
        self.bigCityList = []
        self.bigCityList = JsonParser.cities_dict.get("超大型城市", [])
        for i in range(len(self.bigCityList)):
            row = i // 5
            col = i % 5
            tempRadioButton = QtWidgets.QRadioButton()
            tempRadioButton.setObjectName(self.bigCityList[i])
            tempRadioButton.setText(self.bigCityList[i])
            self.cityRadioButtonGroup.addButton(tempRadioButton, index)
            index += 1
            self.bigCityBoxLayout.addWidget(tempRadioButton, row, col, 1, 1)
            self.cityRadioButtonMap[self.bigCityList[i]] = tempRadioButton
            
        self.normalCityList = []
        self.normalCityList = JsonParser.cities_dict.get("大型城市", [])
        for i in range(len(self.normalCityList)):
            row = i // 5
            col = i % 5
            tempRadioButton = QtWidgets.QRadioButton()
            tempRadioButton.setObjectName(self.normalCityList[i])
            tempRadioButton.setText(self.normalCityList[i])
            self.cityRadioButtonGroup.addButton(tempRadioButton, index)
            index += 1
            self.normalCityBoxLayout.addWidget(tempRadioButton, row, col, 1, 1)
            self.cityRadioButtonMap[self.normalCityList[i]] = tempRadioButton
            
            
    def queryByCityTime(self):
        logger.info('开始查询')
        
        # self.chinaMap.message('12346', 'success', 1000)
        
        startTime = self.queryStartTimeDate.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        endTime = self.queryEndTimeTimeDate.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        if self.cityName == "" :
            info_box(self, "info", "请选择城市！！！")
            return
        
        if startTime > endTime:
            # QMessageBox.warning(self, "info", "开始时间大于结束时间，请重新选择！", QMessageBox.StandardButton.Yes)  
            info_box(self, "info", "开始时间大于结束时间，请重新选择！")
            return
        
        # if not self.queryServer.connect():
        #     if self.connectTimes == 0:
        #         self.connectTimes += 1
        #         info_box(self, "info", "无法连接服务，请检查网络！！！")
        #     else:
        #         self.connectTimes = 0
        #         info_box(self, "info", "无法连接服务，请检擦配置文件！！！")
        #     return
        
        if self.queryServer.isRunning():
            # QMessageBox.warning(self, "error", "请耐心等候检索完成！！！", QMessageBox.StandardButton.Yes)    
            info_box(self, "error", "请耐心查询结束！！！")
            return
        
        logger.info(f'-------按条件查询---------')
        logger.info(f'城市: {self.cityName}')
        logger.info(f'开始时间: {startTime}')
        logger.info(f'结束时间: {endTime}')
        
        # 表格 ： 清空所有行
        self.queryResults.setRowCount(0)
        
        self.queryServer.setQueryData(self.cityName, startTime, endTime)
        self.queryServer.start()
        
    
    def deleteChosedData(self):
        # 获取被选中的行
        indexs = self.queryResults.selectionModel().selectedRows()
        # 创建一个空list用于存放需要删除的行号
        index_list = []
        
        id_list = []
        
        # if not self.deleteServer.connect():
        #     if self.connectTimes == 0:
        #         self.connectTimes += 1
        #         info_box(self, "info", "无法连接服务，请检查网络！！！")
        #     else:
        #         self.connectTimes = 0
        #         info_box(self, "info", "无法连接服务，请检擦配置文件！！！")
        #     return
        
        if self.deleteServer.isRunning():
            # QMessageBox.warning(self, "error", "请耐心等候检索完成！！！", QMessageBox.StandardButton.Yes)    
            info_box(self, "error", "请耐心删除结束！！！")
            return
        
        # 获得需要删除的行号的list
        for index in indexs:
            tmp = index.row()
            index_list.append(tmp)
            id_list.append({'id' : self.queryResults.item(tmp, 0).text()})
        # 用sort方法将list进行降序排列
        index_list.sort(key=int, reverse=True)
        
        logger.debug(f'选中的行 : {index_list}')
        logger.debug(f'选中的行的id : {id_list}')
        
        for i in index_list: # 按照index_list删除对应行
            self.queryResults.removeRow(i)
            
        self.deleteServer.setDeleteData(id_list)
        self.deleteServer.start()
        
    """
    根据深度值，获取统一深度值，单位cm
    """ 
    def uniteValue(self, depth):
        logger.info(f'深度值 : {depth}')
        numbers = re.findall(r"\d+\.\d+|\d+", depth)
        logger.info(f'获取深度值 : {numbers}')
        if not numbers:
            return 0
        number = float(numbers[0]) # 获取第一个数字
        
        if 'cm' in depth or 'CM' in depth or '厘米' in depth or '公分' in depth:
            return number
        if 'mm' in depth or 'MM' in depth or '毫米' in depth:
            return number // 100
        elif 'm' in depth or 'M' in depth or '米' in depth:
            return number * 100
        else:
            return 0
        
        