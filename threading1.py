import time
import threading
#this class implements threading 
#daemon thread will terminate if the module exits if daemon is false then main thread will not terminate until the worker thread is executed
#name parameter is used to identify the thread

def worker(name:str, num:int) ->None:
    for i in range(0, num):
        print(f"thread {name} with {i}")

def main():
    print("the name of the main thread", threading.main_thread().name) # get the main thread name
    threads = []
    name = ["ABD", "123"]
    for i in range(2):
        t = threading.Thread(target=worker, daemon=False, args=(name[i], 10), name="worker 1") 
        t.start()
        threads.append(t)
    
    # wait for threads to finish
    for _ in range(2):
        threads.pop().join()

#synchronization using critical section
x = 0

def increment():
    global x
    time.sleep(0.000001)
    x += 1

def worker_func():
    for _ in range(100):
        increment()

#locks are implemented using semaphores which uses signalling mechanism
def writter_func(writter_lock, reader_lock):
    global x
    for i in range(1000):
        try:
            writter_lock.acquire()
            x = x+1
        finally:
            reader_lock.release()

def reader_func(writter_lock, reader_lock):
    global x
    for i in range(1000):
        try:
            reader_lock.acquire()
            print(x)
        finally:
            writter_lock.release()


def eventfunctions():
    event1 = threading.Event()
    event1.is_set()
    event1.wait()
    event1.set()

def semaphore_functions():
    sem = threading.Semaphore(3) #having a count of 3 which will be decremented by acquire and incremented by release
    sem.acquire()
    sem.release()

class MyThread(threading.Thread):
    def __init__(self, val):
        super().__init__()
        self._counter = val
        self._data: int = 0
    def run(self):
        for i in range(0, self._counter):
            self._data += i
    

if (__name__ == "__main__"):
    
    t1 = MyThread(100)
    t1.start()
    t1.join()
    print("sum of all numbers from 1 t0 100", t1._data)
    print("the sum of numbers", sum(range(1, 100)))

    main()
    # for i in range(10):
    #     x = 0
        # t1 = threading.Thread(target=worker_func)
        # t2 = threading.Thread(target=worker_func)
        # t3 = threading.Thread(target=worker_func)

        # t1.start()
        # t2.start()
        # t3.start()

        # t1.join()
        # t2.join()
        # t3.join()

        #locks are implemented using semaphore in python
    writter_lock = threading.Lock()
    reader_lock = threading.Lock()
    writter_lock.acquire() # default True which will block the thread other wise False it will not block the thread will return False
    reader_lock.acquire()
    
    t1 = threading.Thread(target=writter_func, args=(writter_lock, reader_lock))
    t2 = threading.Thread(target=reader_func, args=(writter_lock, reader_lock))

   # t1.start()
   #  t2.start()

    #writter_lock.release()
    
    #print(x)