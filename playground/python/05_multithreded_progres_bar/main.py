import time
from lib.progresbar import monMaster

def some_task():
    monitor.start("Some task")
    for i in range(3):
        time.sleep(1)
    monitor.stop("Some task",'success')
    monitor.start("Some task 2")
    for i in range(3):
        time.sleep(1)
    monitor.stop("Some task 2",'error')



if __name__ == '__main__':
    monitor=monMaster();
    some_task()
