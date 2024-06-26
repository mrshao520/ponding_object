import os
import multiprocessing

debug = False  # 开启 debug 模式

bind = "0.0.0.0:5000"  # 绑定IP和端口号
# worker_class = "gevent"  # 使用 gevent 模式
# worker_class = "eventlet"  # 使用 eventlet 模式
# workers = multiprocessing.cpu_count()  # 进程数
workers = 1
# threads = 10  # 线程数
# daemon = True  # 后台运行
# preload_app = True  # 解决多worker运行定时任务重复执行问题


# raw_env = ['PATH=/user/local/ffmpeg/bin'] # 设置环境变量
