from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QAction, QApplication
from PyQt5.QtGui import QPainter, QPixmap
from loguru import logger

from src.widgets.QtContentWidget import QtContentWidget
from src.widgets.QtHeaderWidget import QtHeaderWidget
from src.utils.Path import current_path
from src.utils.JsonParser import JsonParser


class QtMainWidget(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        id = QtGui.QFontDatabase.addApplicationFont(current_path + "/resources/font/DS-DIGIT.ttf")
        logger.info(f'加载字体 : {QtGui.QFontDatabase.applicationFontFamilies(id)}')
        
        self.setWindowIcon(QtGui.QIcon(current_path + '/resources/images/title.png'))
        
        self.setObjectName("QtMainWidget")
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        topHint = JsonParser.config.get('WindowStaysOnTopHint', False)
        if topHint:
            self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        #self.setGeometry(0, 0, 720, 576)
        #self.setGeometry(0, 0, 1920, 1080)
        self.showFullScreen()
 
        # self.addQuitAction()
        self.initUi()
        
    def initUi(self):
        mainLayout = QVBoxLayout(self)
        self.headerWidget = QtHeaderWidget(self)
        self.contentWidget = QtContentWidget(self)
        self.headerWidget.setControls(self.contentWidget, self.contentWidget.reptileThread, self.contentWidget.serverThread)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.headerWidget, 1)
        mainLayout.setSpacing(0)
        mainLayout.addWidget(self.contentWidget, 8)
        
    
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # draw background image
        painter = QPainter(self)
        pixmap = QPixmap(current_path + "/resources/images/background.jpg")
        painter.drawPixmap(self.rect(), pixmap)
    
    # 添加右键动作
    def addQuitAction(self):
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
        quitAction = QAction("Quit", self)
        quitAction.triggered.connect(self.signalQuitAction)
        self.addAction(quitAction)
    
    # 退出槽函数
    def signalQuitAction(self):
        # print("quit action!!!")
        app = QApplication.instance()
        app.quit()