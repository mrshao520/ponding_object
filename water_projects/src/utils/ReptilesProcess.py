from multiprocessing import Process, Manager
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from PyQt5.QtCore import QThread
from PyQt5 import QtCore
from datetime import datetime
from loguru import logger
import asyncio

import src.pachong.weibo.middlewares
import src.pachong.weibo.pipelines
from  src.pachong.weibo.middlewares import WeiboSpiderMiddleware
from src.pachong.weibo.pipelines import WeiboPipeline

from src.pachong.weibo.spiders.weibo_data import WeiboDataSpider
from src.pachong.souhu.spiders.souhu_data import SouhuDataSpider
from src.pachong.tengxun.spiders.tx_data import TxDataSpider
from src.pachong.douyin.douyin import start_DrissionPage
from src.pachong.baidu.baidu import get_data
from src.pachong.toutiao.toutiao import scrape_flood_news
from src.utils.JsonParser import JsonParser


def souhu_crawl(queue, city, startTime, endTime, headless):
    # crawle process
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'WARNING',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
    })
    process.crawl(SouhuDataSpider, Queue=queue, 
                  cityName=city + '积水点', startTime=startTime, 
                  endTime=endTime, headless=headless)
    process.start()
    pass
    
def tencent_crawl(queue, city, startTime, endTime, headless):
    # crawle process
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'WARNING',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
    })
    process.crawl(TxDataSpider, Queue=queue, 
                  cityName=city + "积水点", startTime=startTime, 
                  endTime=endTime, headless=headless)
    process.start()
    pass

def weibo_crawl(queue, city, startTime, endTime, headless):
    # crawle process
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'WARNING',
        'DOWNLOADER_MIDDLEWARES': {'src.pachong.weibo.middlewares.WeiboDownloaderMiddleware': 543},
        'ITEM_PIPELINES': {"src.pachong.weibo.pipelines.WeiboPipeline": 300},
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
    
    })
    process.crawl(WeiboDataSpider, Queue=queue, 
                  cityName=city + '积水点', startTime=startTime, 
                  endTime=endTime, headless=headless)
    process.start()
    pass
 
def douyin_crawl(queue, city, startTime, endTime, headless):
    start_date = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
    start_DrissionPage(city + '积水点', start_date, queue.put)
    pass

def baidu_crawl(queue, city, startTime, endTime, headless):
    logger.info(f'开始检索百度渠道!')
    logger.info(f'start_time:{startTime}')
    logger.info(f'end_time:{endTime}')
    # start_date = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
    # end_date = datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
    get_data(startTime, endTime, city + '积水点', queue.put)
    pass

def toutiao_crawl(queue, city, startTime, endTime, headless):
    logger.info(f'开始检索头条渠道!')
    logger.info(f'start_time:{startTime}')
    logger.info(f'end_time:{endTime}')
    # start_date = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
    # end_date = datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
    asyncio.run(scrape_flood_news(startTime, endTime, city + '积水点', queue.put))
    pass
    
    
def process_lancher(queue, channel_dict, city, channel_list, 
                    startTime, endTime, headless):
    try:
        for chan in channel_list:
            if chan in channel_dict:
                channel_dict[chan](queue, city, startTime, 
                                   endTime, headless)
            else:
                queue.put(f'暂不支持采集 {chan} 渠道!')
    except:
        pass
    finally:
        # queue.put('检索失败-warning-百度-未检索到信息')
        queue.put('采集结束')
    
class ReptilesProcess(QThread):
    update_text = QtCore.pyqtSignal(str)
    quit_thread = QtCore.pyqtSignal(str, str)
    # stop_timer = QtCore.pyqtSignal()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.reptileQueue = Manager().Queue()
        self.cityName = ''
        self.channelList = []
        self.startTime = ''
        self.endTime = ''
        self.channel_dict = {
                                '搜狐': souhu_crawl,
                                '腾讯': tencent_crawl,
                                '抖音': douyin_crawl,
                                '微博': weibo_crawl,
                                '百度': baidu_crawl,
                                '头条': toutiao_crawl
                             }
        # 防止进程中断 导致线程死锁
        # self.killThreadTimer = QtCore.QTimer()
        # self.killThreadTimer.timeout.connect(self.slotKillThread)
        # self.killThreadTimer.setSingleShot(True)
        # self.killThreadTimer.start(10 * 60 * 1000)
        # self.stop_timer.connect(self.slotStopTimer)
        
        
    
    def start_process(self):
        self.start()
        headless = JsonParser.config.get('headless', False)
        logger.info(f'headless : {headless}')
        self.reptileProcess = Process(target=process_lancher, 
                                      args=(self.reptileQueue, self.channel_dict, 
                                            self.cityName, self.channelList, 
                                            self.startTime, self.endTime, headless))
        # self.reptileProcess = Process(target=souhu_crawl, 
        #                               args=(self.reptileQueue, self.cityName, 
        #                                     self.startTime, self.endTime))
        self.reptileProcess.start()
        pass
    
    def end_process(self):
        logger.info('正在退出检索进程！')
        try:
            if self.isRunning():
                self.terminate()
            self.reptileProcess.terminate()
            # self.stop_timer.emit()
            logger.info('退出检索进程成功！')
        except:
            logger.debug('退出检索进程失败！')
    
    def run(self) -> None:
        while True:
            if not self.reptileQueue.empty():
                results = self.reptileQueue.get()
                
                self.update_text.emit(str(results))
                
                if results == '采集结束':
                    break
                
                # 睡眠10毫秒，否则太快会导致闪退或者显示乱码
                self.msleep(10)
                
        # self.reptileProcess.join()
        # self.stop_timer.emit()
        
    def updateData(self, city, channel, startTime, endTime):
        self.cityName = city
        self.channelList = channel
        self.startTime = startTime
        self.endTime = endTime
        
    # def slotKillThread(self):
    #     try:
    #         if self.isRunning():
    #             self.terminate()
    #             self.reptileProcess.terminate()
    #             print('退出进程和线程！')
    #     except:
    #         print('退出进程和线程！')
    
    # def slotStopTimer(self):
    #     # print('停止killThreadTimer')
    #     self.killThreadTimer.stop()