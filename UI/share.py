import datetime
import time


class SI:
    mainWin = None
    loginWin = None
    token = None
    className = None

    suchClass_page_now = None
    suchClass_page = None
    suchClass_name = None

    curr_time = datetime.datetime.now()
    print(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))