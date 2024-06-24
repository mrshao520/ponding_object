import sys
from PyQt5.QtWidgets import QApplication
from src.widgets.QtMainWidget import QtMainWidget
from src.utils.Path import current_path
from src.utils.JsonParser import JsonParser
from loguru import logger
import multiprocessing


def main():
    import sys
    logger.debug(f"New process:{sys.argv}")
    trace = logger.add(current_path + '/log/waterlogging.log', rotation = '00:00', retention = '7 days',
                       format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}")
    
    logger.info("大城市暴雨积水多源数据实时采集处理系统")
    
    try:
        JsonParser.prepare()
    except:
        logger.debug("json 格式解析错误！")
        
    app = QApplication(sys.argv)
    widget = QtMainWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    
    import sys
    logger.debug(f"New process:{sys.argv}")
    # Pyinstaller 多进程代码打包 exe 出现多个进程解决方案
    # parallel_backend('threading')
    multiprocessing.freeze_support()
    logger.debug(f"current_path : {current_path}")
    multiprocessing.Process(target=main).start()
    
    # trace = logger.add(current_path + '/log/waterlogging.log', rotation = '00:00', retention = '7 days',
    #                    format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}")
    
    # logger.info("大城市暴雨积水多源数据实时采集处理系统")
    
    # try:
    #     JsonParser.prepare()
    # except:
    #     logger.debug("json 格式解析错误！")
        
    # app = QApplication(sys.argv)
    # widget = QtMainWidget()
    # widget.show()
    # sys.exit(app.exec_())