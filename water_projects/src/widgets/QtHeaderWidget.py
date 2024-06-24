from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QApplication,
    QAction,
    QMenu,
    QPushButton,
)
from PyQt5.QtGui import QPainter, QPixmap, QFont, QCursor
from PyQt5.QtCore import QTimer, QDateTime, QThread
from threading import Thread


from src.utils.Path import current_path
from src.widgets.QtContentWidget import info_box
from src.utils.JsonParser import JsonParser
from src.utils.LoginWeibo import login_weibo


class QtHeaderWidget(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.initUi()

        # self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
        # self.addRightBtnAction()

        # self.setStyleSheet("QMenu{background:LightSkyBlue;}"  # 选项背景颜色
        #                    "QMenu{border:1px solid lightgray;}"  # 设置整个菜单框的边界高亮厚度
        #                    "QMenu{border-color:green;}"  # 整个边框的颜色

        #                    "QMenu::item{padding:0px 5px 0px 5px;}"  # 以文字为标准，右边距文字40像素，左边同理
        #                    "QMenu::item{height:20px;}"  # 显示菜单选项高度
        #                    "QMenu::item{color:blue;}"#选项文字颜色
        #                    "QMenu::item{background:white;}"  # 选项背景
        #                    "QMenu::item{margin:1px 1px 1px 1px;}"  # 每个选项四边的边界厚度，上，右，下，左

        #                    "QMenu::item:selected:enabled{background:lightgray;}"
        #                    "QMenu::item:selected:enabled{color:red;}"  # 鼠标在选项上面时，文字的颜色
        #                    "QMenu::item:selected:!enabled{background:transparent;}"#鼠标在上面时，选项背景为不透明

        #                    "QMenu::separator{height:1px;}"  # 要在两个选项设置self.groupBox_menu.addSeparator()才有用
        #                    "QMenu::separator{width:50px;}"
        #                    "QMenu::separator{background:blue;}"
        #                    "QMenu::separator{margin:0px 0px 0px 0px;}")

    def initUi(self):
        self.setStyleSheet(
            "QLabel{color:white;font:'DS-Digital';font-weight:bold;} \
            QPushButton{color:rgb(70,130,180);font:bold 'DS-Digital';font-size:23px;} \
            QPushButton:pressed{;}  \
            "
        )
        headerLayout = QHBoxLayout(self)
        headerLayout.setContentsMargins(0, 0, 0, 0)

        self.imageLabel = QLabel(self)
        image = current_path + "/resources/images/title.png"
        pixmap = QPixmap(image)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setMaximumSize(120, 120)
        headerLayout.addWidget(self.imageLabel, 1)

        self.textLabel = QLabel(self)
        self.textLabel.setObjectName("header_test")
        self.textLabel.setText("大城市暴雨积水点多源数据实时采集处理系统")
        self.textLabel.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        headerLayout.addWidget(self.textLabel, 8)

        self.loginButton = QPushButton("登录微博")
        self.loginButton.clicked.connect(self.login_weibo)
        self.refreshButton = QPushButton("刷新")
        self.refreshButton.clicked.connect(self.signalRefreshAction)
        self.quitButton = QPushButton("退出")
        self.quitButton.clicked.connect(self.signalQuitAction)
        headerLayout.addWidget(self.loginButton, 1)
        headerLayout.addWidget(self.refreshButton, 1)
        headerLayout.addWidget(self.quitButton, 1)
        
        self.hide_button()
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.addRightButtonAction)
        self.buttonTimer = QTimer(self)
        self.buttonTimer.timeout.connect(self.hide_button)
        self.buttonTimer.setSingleShot(True)
        
        headerLayout.setSpacing(0)

        self.timeLabel = QLabel(self)
        self.timeLabel.setObjectName("header_time")
        self.timeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        headerLayout.addWidget(self.timeLabel, 2)

        # 设置每秒更新时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

    def showTime(self):
        datetime = QDateTime.currentDateTime()
        self.timeLabel.setText(datetime.toString("yyyy/MM/dd hh:mm:ss"))

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # 背景图
        painter = QPainter(self)
        pixmap = QPixmap(current_path + "/resources/images/header.png")
        painter.drawPixmap(self.rect(), pixmap)
        return super().paintEvent(a0)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        # 自适应窗口大小，修改文字大小
        print(f"width : {a0.size().width()}")
        size = a0.size().width() // 80
        font = QFont("DS-Digital", size)
        self.textLabel.setFont(font)
        size = a0.size().width() // 120
        font.setPointSize(size)
        self.timeLabel.setFont(font)
        self.quitButton.setFont(font)
        self.refreshButton.setFont(font)
        self.loginButton.setFont(font)
        return super().resizeEvent(a0)

    def addRightButtonAction(self):
        self.show_button()
        self.buttonTimer.start(3000)
        

    # 添加右键动作
    def addRightBtnAction(self):
        self.menu = QMenu(self)
        # self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)

        self.quitAction = QAction(
            QtGui.QIcon(current_path + "/resources/images/exit.png"), "退出", self
        )
        self.quitAction.triggered.connect(self.signalQuitAction)

        self.refreshAction = QAction(
            QtGui.QIcon(current_path + "/resources/images/refresh.png"), "刷新", self
        )
        self.refreshAction.triggered.connect(self.signalRefreshAction)

        self.loginAction = QAction(
            QtGui.QIcon(current_path + "/resources/images/login_weibo.png"),
            "登录微博",
            self,
        )
        self.loginAction.triggered.connect(self.login_weibo)

        # self.addAction(self.loginAction)
        # self.addAction(self.refreshAction)
        # self.addAction(self.quitAction)

        self.menu.addAction(self.loginAction)
        self.menu.addAction(self.refreshAction)
        self.menu.addAction(self.quitAction)

        self.menu.popup(QCursor.pos())

    # 退出槽函数
    def signalQuitAction(self):
        if self.reptileThread.isRunning():
            # QMessageBox.warning(self, "error", "请耐心等候检索完成！！！", QMessageBox.StandardButton.Yes)
            info_box(self, "error", "请耐心等候采集完成！！！")
            return

        if self.serverThread.isRunning():
            info_box(self, "error", "请耐心等候模型处理！！！")
            return
        # print("quit action!!!")

        info_box(self, "info", "正在退出，请勿操作！！！")
        app = QApplication.instance()
        app.quit()

    # 刷新槽函数
    def signalRefreshAction(self):
        if self.reptileThread.isRunning():
            # QMessageBox.warning(self, "error", "请耐心等候检索完成！！！", QMessageBox.StandardButton.Yes)
            info_box(self, "error", "请耐心等候采集完成！！！")
            return

        if self.serverThread.isRunning():
            info_box(self, "error", "请耐心等候模型处理！！！")
            return
        # print("quit action!!!")

        try:
            JsonParser.prepare()
        except:
            info_box(self, "error", "配置文件解析出错，请检查！！！")

        info_box(self, "info", "正在刷新，请勿操作！！！")

        self.content.update()

        app = QApplication.instance()
        app.processEvents()

    def setControls(self, content, reptileThread, serveThread):
        self.content = content
        self.reptileThread = reptileThread
        self.serverThread = serveThread

    def login_weibo(self):
        t = Thread(target=login_weibo)
        t.start()
        
    def hide_button(self):
        self.quitButton.hide()
        self.loginButton.hide()
        self.refreshButton.hide()
    
    def show_button(self):
        self.quitButton.show()
        self.loginButton.show()
        self.refreshButton.show()
