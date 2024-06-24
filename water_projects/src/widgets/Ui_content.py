# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Desktop\PyQtLearning\code\Waterlogging\content.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from loguru import logger


from src.widgets.QtWebView import QtWebView
from src.utils.JsonParser import JsonParser



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.contentLayout = QtWidgets.QHBoxLayout(Form)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setObjectName("contentLayout")
        self.contentSplitter = QtWidgets.QSplitter(Form)
        self.contentSplitter.setLineWidth(0)
        self.contentSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.contentSplitter.setHandleWidth(10)
        self.contentSplitter.setObjectName("contentSplitter")
        self.leftSplitter = QtWidgets.QSplitter(self.contentSplitter)
        self.leftSplitter.setLineWidth(0)
        self.leftSplitter.setOrientation(QtCore.Qt.Vertical)
        self.leftSplitter.setHandleWidth(10)
        self.leftSplitter.setObjectName("leftSplitter")
        
        self.chart1 = QtWebView(self.leftSplitter)
        self.chart1.setObjectName("chart1")
        
        # self.chart2 = QtWebView(self.leftSplitter)
        # self.chart2.setObjectName("chart2")
        
        # self.chart3 = QtWebView(self.leftSplitter)
        # self.chart3.setObjectName("chart3")
        
        self.queryGroupBox = QtWidgets.QGroupBox('数据检索设置')
        
        self.queryGroupBoxLayout = QtWidgets.QGridLayout(self.queryGroupBox)
        self.queryGroupBoxLayout.setContentsMargins(5, 12, 5, 0)
        self.queryGroupBoxLayout.setSpacing(0)
        self.queryGroupBoxLayout.setHorizontalSpacing(8)
        self.queryGroupBoxLayout.setObjectName("queryGroupBoxLayout")
        
        self.queryButton = QtWidgets.QPushButton('查询')
        self.queryButton.setObjectName("queryButton")
        self.queryButton.setMinimumSize(100, 50)
        self.queryButton.setMaximumSize(100, 50)
        self.queryGroupBoxLayout.addWidget(self.queryButton, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.deleteButton = QtWidgets.QPushButton('删除')
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setMinimumSize(100, 50)
        self.deleteButton.setMaximumSize(100, 50)
        self.queryGroupBoxLayout.addWidget(self.deleteButton, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.queryStartTimeLabel = QtWidgets.QLabel('开始时间')
        self.queryStartTimeLabel.setStyleSheet('QLabel{font:bold 15px; color:#aaaaff;font:"DS-Digital";border: 2px solid  #aaaaff; \
                                      border-radius:5px;background-color:rgba(0, 0, 0, 0.1)}')
        self.queryStartTimeLabel.setMargin(0)
        self.queryStartTimeLabel.setMaximumSize(76, 30)
        self.queryEndTimeLabel = QtWidgets.QLabel('结束时间')
        self.queryEndTimeLabel.setStyleSheet('QLabel{font:bold 15px; color:#aaaaff;font:"DS-Digital";border: 2px solid  #aaaaff; \
                                      border-radius:5px;background-color:rgba(0, 0, 0, 0.1)}')
        self.queryEndTimeLabel.setMargin(0)
        self.queryEndTimeLabel.setMaximumSize(76, 30)
        self.queryGroupBoxLayout.addWidget(self.queryStartTimeLabel, 0, 1, 1, 1)
        self.queryGroupBoxLayout.addWidget(self.queryEndTimeLabel, 1, 1, 1, 1)
        
        self.queryStartTimeDate = QtWidgets.QDateTimeEdit()
        self.queryGroupBoxLayout.addWidget(self.queryStartTimeDate, 0, 2, 1, 1)
        self.queryEndTimeTimeDate = QtWidgets.QDateTimeEdit()
        self.queryGroupBoxLayout.addWidget(self.queryEndTimeTimeDate, 1, 2, 1, 1)
        
        self.queryStartTimeDate.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.queryEndTimeTimeDate.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.queryStartTimeDate.setDateTime(QtCore.QDateTime.currentDateTime().addYears(-1))
        self.queryEndTimeTimeDate.setDateTime(QtCore.QDateTime.currentDateTime())
        
        
        self.leftSplitter.addWidget(self.queryGroupBox)
        
        # 数据库检索结果
        self.queryResults = QtWidgets.QTableWidget(self.leftSplitter)
        self.queryResults.setObjectName("queryResults")
        # self.process.setColumnCount(8)
        # self.process.setHorizontalHeaderLabels(['id', '日期', '时间', '城市', '地点', '经纬度', '深度值','备注'])
        self.queryResults.setColumnCount(7)
        self.queryResults.setHorizontalHeaderLabels(['id', '日期', '时间', '城市', '地点', '深度值','备注'])

        self.queryResults.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        # self.queryResults.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.queryResults.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        # self.process.horizontalHeader().setStretchLastSection(True) # 自适应表头
        # self.process.horizontalHeader().hide()  # 取消列号
        self.queryResults.verticalHeader().hide()   # 取消行号
        
        # 设置只能选择整行
        self.queryResults.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        
        
        
        #-------------------------------------
        self.centerSpplitter = QtWidgets.QSplitter(self.contentSplitter)
        self.centerSpplitter.setLineWidth(0)
        self.centerSpplitter.setOrientation(QtCore.Qt.Vertical)
        self.centerSpplitter.setHandleWidth(0)
        self.centerSpplitter.setObjectName("centerSpplitter")
        self.splitter = QtWidgets.QSplitter(self.centerSpplitter)
        self.splitter.setLineWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(8)
        self.splitter.setObjectName("splitter")
        
        # 城市部分 布局
        self.cityBoxWidget = QtWidgets.QWidget(self.splitter)
        self.cityBoxWidget.setObjectName("cityBoxWidget")
        self.cityBoxLayout = QtWidgets.QVBoxLayout(self.cityBoxWidget)
        self.cityBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.cityBoxLayout.setSpacing(0)
        
        self.cityRadioButtonGroup = QtWidgets.QButtonGroup(self.cityBoxWidget)
        self.cityRadioButtonGroup.setExclusive(True)
        
        self.bigCityGroupBox = QtWidgets.QGroupBox('超大型城市', self.cityBoxWidget)
        self.normalCityGroupBox = QtWidgets.QGroupBox('大型城市', self.cityBoxWidget)
        
        self.cityRadioButtonMap = {}
        
        self.bigCityBoxLayout = QtWidgets.QGridLayout(self.bigCityGroupBox)
        self.bigCityBoxLayout.setContentsMargins(0, 15, 0, 0)
        self.bigCityBoxLayout.setSpacing(0)
        self.bigCityBoxLayout.setObjectName("bigCityBoxLayout")
        
        self.normalCityBoxLayout = QtWidgets.QGridLayout(self.normalCityGroupBox)
        self.normalCityBoxLayout.setContentsMargins(0, 15, 0, 0)
        self.normalCityBoxLayout.setSpacing(0)
        self.normalCityBoxLayout.setObjectName("normalCityBoxLayout")
        
        index = 0
        self.bigCityList = []
        self.bigCityList = JsonParser.cities_dict.get("超大型城市", [])
        logger.info(f"超大型城市 : {self.bigCityList}")
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
        logger.info(f"大型城市 : {self.normalCityList}")
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
        
        self.cityBoxLayout.addWidget(self.bigCityGroupBox)
        self.cityBoxLayout.setSpacing(8)
        self.cityBoxLayout.addWidget(self.normalCityGroupBox)
        
        # self.cityBox = QtWidgets.QComboBox(self.splitter)
        # self.cityBox.setObjectName("cityBox")
        # self.cityBox.addItem("")
        # self.cityBox.addItem("")
        # self.cityBox.addItem("")
        
        
        # self.cityBoxWidget = QtWidgets.QWidget(self.splitter)
        # self.cityBoxWidget.setObjectName("cityBoxWidget")
        # self.cityLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        # self.cityLayout.setObjectName("cityLayout")
        # self.cityLayout.setContentsMargins(0, 0, 0, 0)
        # self.cityLayout.setSpacing(0)
        
        # 采集渠道布局
        self.gridLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        
        self.gridLayout = QtWidgets.QHBoxLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        
        self.checkGroupBox = QtWidgets.QGroupBox('采集渠道设置', self.gridLayoutWidget)
        
        self.checkBoxLayout = QtWidgets.QGridLayout(self.checkGroupBox)
        self.checkBoxLayout.setContentsMargins(0, 15, 0, 0)
        self.checkBoxLayout.setSpacing(0)
        self.checkBoxLayout.setObjectName("checkBoxLayout")
        
        self.checkBoxButtonGroup = QtWidgets.QButtonGroup(self.cityBoxWidget)
        self.checkBoxButtonGroup.setExclusive(True)
        
        self.checkBoxList = []
        self.channelsList = JsonParser.channels_dict.get("采集渠道", [])
        logger.info(f"采集渠道 : {self.channelsList}")
        for i in range(len(self.channelsList)):
            row = i // 2
            col = i % 2
            tempCheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
            tempCheckBox.setObjectName(self.channelsList[i])
            tempCheckBox.setText(self.channelsList[i])
            self.checkBoxButtonGroup.addButton(tempCheckBox)
            self.checkBoxList.append(tempCheckBox)
            self.checkBoxLayout.addWidget(tempCheckBox, row, col, 1, 1)
            
        self.gridLayout.addWidget(self.checkGroupBox)
        
        # 属性布局，如时间范围
        self.attributeLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.attributeLayoutWidget.setObjectName("attributeLayoutWidget")
        
        self.attributeLayout = QtWidgets.QHBoxLayout(self.attributeLayoutWidget)
        self.attributeLayout.setContentsMargins(0, 0, 0, 0)
        self.attributeLayout.setSpacing(0)
        
        self.attributeGroupBox = QtWidgets.QGroupBox('采集属性设置')
        
        self.attributeGroupBoxLayout = QtWidgets.QGridLayout(self.attributeGroupBox)
        self.attributeGroupBoxLayout.setContentsMargins(5, 12, 5, 0)
        self.attributeGroupBoxLayout.setSpacing(0)
        self.attributeGroupBoxLayout.setHorizontalSpacing(8)
        self.attributeGroupBoxLayout.setObjectName("attributeGroupBoxLayout")
        
        self.autoSearchCheckBox = QtWidgets.QCheckBox('定时采集')
        self.attributeGroupBoxLayout.addWidget(self.autoSearchCheckBox, 0, 1, 1, 1)
        
        self.realTimeCheckBox = QtWidgets.QCheckBox('实时数据采集')
        # self.realTimeCheckBox.setChecked(True)
        self.attributeGroupBoxLayout.addWidget(self.realTimeCheckBox, 1, 1, 1, 1)
        
        self.historyTimeCheckBox = QtWidgets.QCheckBox('历史数据采集')
        self.attributeGroupBoxLayout.addWidget(self.historyTimeCheckBox, 1, 2, 1, 1)
        
        self.timeButtonGroup = QtWidgets.QButtonGroup(self.attributeGroupBox)
        self.timeButtonGroup.addButton(self.realTimeCheckBox)
        self.timeButtonGroup.addButton(self.historyTimeCheckBox)
        self.timeButtonGroup.setExclusive(True)
        
        self.startTimeLabel = QtWidgets.QLabel('开始时间')
        self.startTimeLabel.setStyleSheet('QLabel{font:bold 15px; color:#aaaaff;font:"DS-Digital";border: 2px solid  #aaaaff; \
                                      border-radius:5px;background-color:rgba(0, 0, 0, 0.1)}')
        self.endTimeLabel = QtWidgets.QLabel('结束时间')
        self.endTimeLabel.setStyleSheet('QLabel{font:bold 15px; color:#aaaaff;font:"DS-Digital";border: 2px solid  #aaaaff; \
                                      border-radius:5px;background-color:rgba(0, 0, 0, 0.1)}')
        self.attributeGroupBoxLayout.addWidget(self.startTimeLabel, 2, 0, 1, 1)
        self.attributeGroupBoxLayout.addWidget(self.endTimeLabel, 3, 0, 1, 1)
        # self.autoTimeComboBox = QtWidgets.QComboBox()
        # self.attributeGroupBoxLayout.addWidget(self.autoTimeComboBox, 0, 1, 1, 1)
        # self.autoTimeComboBox.addItems(['10分钟', '20分钟', '30分钟', '1小时', '2小时'])
        
        self.autoTimeSpinBox = QtWidgets.QSpinBox()
        self.attributeGroupBoxLayout.addWidget(self.autoTimeSpinBox, 0, 2, 1, 1)
        self.autoTimeSpinBox.setMinimum(30)
        self.autoTimeSpinBox.setMaximum(360)
        self.autoTimeSpinBox.setSingleStep(10)
        self.autoTimeSpinBox.setProperty("value", 10)
        self.autoTimeSpinBox.setSuffix(' 分钟')
        self.autoTimeSpinBox.setObjectName("autoTimeSpinBox")
        
        self.startRelTimeDate = QtWidgets.QDateTimeEdit()
        self.attributeGroupBoxLayout.addWidget(self.startRelTimeDate, 2, 1, 1, 1)
        
        self.endRelTimeTimeDate = QtWidgets.QDateTimeEdit()
        self.attributeGroupBoxLayout.addWidget(self.endRelTimeTimeDate, 3, 1, 1, 1)
        
        self.startRelTimeDate.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.endRelTimeTimeDate.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.startRelTimeDate.setDate(QtCore.QDate.currentDate())
        self.endRelTimeTimeDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.startRelTimeDate.setEnabled(False)
        self.endRelTimeTimeDate.setEnabled(False)
        
        
        self.startHisTimeDate = QtWidgets.QDateTimeEdit()
        self.attributeGroupBoxLayout.addWidget(self.startHisTimeDate, 2, 2, 1, 1)
        
        self.endHisTimeTimeDate = QtWidgets.QDateTimeEdit()
        self.attributeGroupBoxLayout.addWidget(self.endHisTimeTimeDate, 3, 2, 1, 1)
        
        # self.endHisTimeTimeDate.dateTime().addMSecs(60).toString("yyyy-MM-dd HH:mm:ss")
        self.startHisTimeDate.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.endHisTimeTimeDate.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.startHisTimeDate.setDateTime(QtCore.QDateTime.currentDateTime().addYears(-1))
        self.endHisTimeTimeDate.setDateTime(QtCore.QDateTime.currentDateTime())
        
        self.attributeLayout.addWidget(self.attributeGroupBox)
        # self.sina = QtWidgets.QCheckBox(self.gridLayoutWidget)
        # self.sina.setObjectName("sina")
        # self.checkBoxLayout.addWidget(self.sina, 0, 1, 1, 1)
        # self.microBlog = QtWidgets.QCheckBox(self.gridLayoutWidget)
        # self.microBlog.setObjectName("microBlog")
        # self.checkBoxLayout.addWidget(self.microBlog, 1, 0, 1, 1)
        # self.sohu = QtWidgets.QCheckBox(self.gridLayoutWidget)
        # self.sohu.setObjectName("sohu")
        # self.checkBoxLayout.addWidget(self.sohu, 0, 0, 1, 1)
        # self.headlines = QtWidgets.QCheckBox(self.gridLayoutWidget)
        # self.headlines.setObjectName("headlines")
        # self.checkBoxLayout.addWidget(self.headlines, 1, 1, 1, 1)
        # self.netease = QtWidgets.QCheckBox(self.gridLayoutWidget)
        # self.netease.setObjectName("netease")
        # self.checkBoxLayout.addWidget(self.netease, 0, 2, 1, 1)
        # self.tencent = QtWidgets.QCheckBox(self.gridLayoutWidget)
        # self.tencent.setObjectName("tencent")
        # self.checkBoxLayout.addWidget(self.tencent, 1, 2, 1, 1)
        
        
        
        self.chinaMap = QtWebView(self.centerSpplitter)
        self.chinaMap.setObjectName("chinaMap")
        
        self.cityChart = QtWebView(self.centerSpplitter)
        self.cityChart.setObjectName("cityChart")
        
        
        # 右侧布局
        self.rightSplitter = QtWidgets.QSplitter(self.contentSplitter)
        self.rightSplitter.setLineWidth(0)
        self.rightSplitter.setOrientation(QtCore.Qt.Vertical)
        self.rightSplitter.setHandleWidth(15)
        self.rightSplitter.setObjectName("rightSplitter")
        
        # 采集按钮布局
        # self.seachGroupBox = QtWidgets.QGroupBox('采集按钮', self.rightSplitter)
        # self.buttonLayoutWidget = QtWidgets.QWidget(self.seachGroupBox)
        
        self.buttonLayoutWidget = QtWidgets.QWidget(self.rightSplitter)
        self.buttonLayoutWidget.setObjectName("buttonLayoutWidget")
        self.searchGroupLayout = QtWidgets.QHBoxLayout(self.buttonLayoutWidget)
        self.searchGroupLayout.setContentsMargins(0, 0, 0, 0)
        
        self.searchGroupBox = QtWidgets.QGroupBox('数据采集')
        
        self.buttonLayout = QtWidgets.QHBoxLayout(self.searchGroupBox)
        self.buttonLayout.setContentsMargins(0, 12, 0, 0)
        self.buttonLayout.setObjectName("buttonLayout")
        
        self.start = QtWidgets.QPushButton('开始采集')
        self.start.setObjectName("start")
        
        self.buttonLayout.addItem(QtWidgets.QSpacerItem(40, 20,  
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.buttonLayout.addWidget(self.start)
        self.buttonLayout.addItem(QtWidgets.QSpacerItem(40, 20,  
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.buttonLayout.setSpacing(0)
        
        self.end = QtWidgets.QPushButton('结束采集')
        self.end.setObjectName("end")
        self.buttonLayout.addWidget(self.end)
        self.buttonLayout.addItem(QtWidgets.QSpacerItem(40, 20,  
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.start.setMinimumSize(150, 85)
        self.end.setMinimumSize(150, 85)
        self.start.setMaximumSize(150, 85)
        self.end.setMaximumSize(150, 85)
        self.buttonLayout.setStretch(0, 1)
        self.buttonLayout.setStretch(1, 3)
        self.buttonLayout.setStretch(2, 1)
        self.buttonLayout.setStretch(3, 3)
        self.buttonLayout.setStretch(4, 1)
        
        self.searchGroupLayout.addWidget(self.searchGroupBox)
        
        # 显示爬虫爬取的结果
        self.result = QtWidgets.QTextEdit(self.rightSplitter)
        self.result.setObjectName("result")
        self.result.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        # self.result.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.result.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        # server按钮
        self.serverButtonLayoutWidget = QtWidgets.QWidget(self.rightSplitter)
        self.serverButtonLayoutWidget.setObjectName("serverButtonLayoutWidget")
        self.serverGroupLayout = QtWidgets.QHBoxLayout(self.serverButtonLayoutWidget)
        self.serverGroupLayout.setContentsMargins(0, 0, 0, 0)
        
        self.serverGroupBox = QtWidgets.QGroupBox('模型处理')
        
        self.serverButtonLayout = QtWidgets.QHBoxLayout(self.serverGroupBox)
        self.serverButtonLayout.setContentsMargins(0, 12, 0, 0)
        self.serverButtonLayout.setObjectName("serverButtonLayout")
        
        self.startHandle = QtWidgets.QPushButton('开始处理')
        self.startHandle.setObjectName("startHandle")
        
        self.serverButtonLayout.addItem(QtWidgets.QSpacerItem(40, 20,  
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.serverButtonLayout.addWidget(self.startHandle)
        self.serverButtonLayout.addItem(QtWidgets.QSpacerItem(40, 20,  
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.serverButtonLayout.setSpacing(0)
        
        self.saveResults = QtWidgets.QPushButton('保存结果')
        self.saveResults.setObjectName("saveResults")
        self.serverButtonLayout.addWidget(self.saveResults)
        self.serverButtonLayout.addItem(QtWidgets.QSpacerItem(40, 20,  
                    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.startHandle.setMinimumSize(150, 85)
        self.saveResults.setMinimumSize(150, 85)
        self.startHandle.setMaximumSize(150, 85)
        self.saveResults.setMaximumSize(150, 85)
        self.serverButtonLayout.setStretch(0, 1)
        self.serverButtonLayout.setStretch(1, 3)
        self.serverButtonLayout.setStretch(2, 1)
        self.serverButtonLayout.setStretch(3, 3)
        self.serverButtonLayout.setStretch(4, 1)
        
        self.serverGroupLayout.addWidget(self.serverGroupBox)
        
        # 显示模型处理后额结果
        self.process = QtWidgets.QTableWidget(self.rightSplitter)
        self.process.setObjectName("process")
        # self.process.setColumnCount(7)
        # self.process.setHorizontalHeaderLabels(['日期', '时间', '城市', '地点', '经纬度', '深度值','备注'])
        self.process.setColumnCount(6)
        self.process.setHorizontalHeaderLabels(['日期', '时间', '城市', '地点', '深度值','备注'])

        self.process.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.process.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.process.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        # self.process.horizontalHeader().setStretchLastSection(True) # 自适应表头
        # self.process.horizontalHeader().hide()  # 取消列号
        self.process.verticalHeader().hide()   # 取消行号
        
        self.contentLayout.addWidget(self.contentSplitter)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        
        
        # self.cityBox.setItemText(0, _translate("Form", "北京"))
        # self.cityBox.setItemText(1, _translate("Form", "上海"))
        # self.cityBox.setItemText(2, _translate("Form", "南京"))
        
        
        # self.sina.setText(_translate("Form", "新浪"))
        # self.microBlog.setText(_translate("Form", "微博"))
        # self.sohu.setText(_translate("Form", "搜狐"))
        # self.headlines.setText(_translate("Form", "今日头条"))
        # self.netease.setText(_translate("Form", "网易"))
        # self.tencent.setText(_translate("Form", "腾讯"))
        # self.start.setText(_translate("Form", "开始爬虫"))
        # self.end.setText(_translate("Form", "结束爬虫"))
