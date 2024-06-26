import atexit
import platform
from flask_apscheduler.scheduler import APScheduler

scheduler = APScheduler()


def __scheduler_init(app, scheduler_):
    """多进程环境下，Flask-APScheduler重复运行解决方案

    Args:
        app (_type_): Flask App
        scheduler_ (_type_): scheduler_
    """
    # scheduler_ = APScheduler()

    if platform.system() != "Windows":
        # Linux 环境下
        fcntl = __import__("fcntl")
        f = open("scheduler_.lock", "wb")
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler_.init_app(app)
            scheduler_.start()
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock)
    else:
        # Window 环境下
        msvcrt = __import__("msvcrt")
        f = open("scheduler_.lock", "wb")
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            scheduler_.init_app(app)
            scheduler_.start()
        except:
            pass

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass

        atexit.register(_unlock_file)
