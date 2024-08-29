import sys
import time
import functools

def profiling(func, timestamp):
    #documents will be updated with the actual function __doc__ string
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if timestamp:            
            start = time.time()
        result = func(self, *args, **kwargs)
        if timestamp:
            end = time.time()        
        if timestamp:
            print(f"{func.__name__} called at time {start} takes {end-start} seconds")
        return result
    return wrapper

class Profiling:
    #this function will be called while the class is going to get inherited from parent
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        timestamp = kwargs.get("timestamp", False)
        funcs = kwargs.get("funcs", [])
        for name, obj in cls.__dict__.items():
            if hasattr(obj, "__call__"):
                func = obj
                #check to add profiling for certain function if the funcs list is not empty otherwise add for functions in the list
                if funcs and func.__name__ in funcs:                 
                    setattr(cls, name, profiling(func, timestamp))

                if not funcs:
                    setattr(cls, name, profiling(func, timestamp))   

class DBConnection(Profiling, timestamp=True, funcs= ["connect"]):
    def __init__(self, connection):
        self._connection = connection

    def connect(self, DBinstance):
        """connects to DB instance"""
        print("connection to DB instance", DBinstance)
        time.sleep(1)

    def disconnect(self):
        """disconnects from DB instance"""
        print("disconnecting from DB instance")
        time.sleep(1)


if __name__ == "__main__":
    db = DBConnection("sqllite://organization")
    db.connect("Employee")
    db.disconnect()
