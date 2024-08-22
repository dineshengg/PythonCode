
import sys
import functools
from collections.abc import Iterable

def make_greet_happy(func):
    @functools.wraps(func) #wraps is used by pydoc to provide proper documentation for func passed otherwise the doc will be wrapper for func
    def wrapper(msg):        
        """this is a wrapper function"""
        #pre-processing the input parameters
        msg = msg.upper()
        #call the function
        return_value = func(msg)
        #post-processing the output parameters of the actual function
        if return_value < 0:
            return "Error happened which performing the operation"
        else:
            return "success" 
    return wrapper

@make_greet_happy
def my_tokenize(msg):
    """this is a tokenize function"""
    if isinstance(msg, str) and msg and msg.find(',') > 0:
        print(msg.split(","))
        return 0
    else:
        return -1
    
def sample_decorator(func):
    def wrapper(*args, **kwargs):
        print("calling a function for pre-processing")
        return_value = func(*args, **kwargs)
        print("calling post-processing function")
        return return_value
    return wrapper

#Generator for Logging
def logging(function):
    import time
    @functools.wraps(function)
    def wrapper(*args, **kwargs): #decorator accepting the variable arguments and passing it to actual function used by decorator
        t_str = time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", time.gmtime())
        return_value = function(*args, **kwargs)
        with open("logging.txt", "a+t") as f: #context manager that takes care of destroying the resource even when there is exception inside the context manager block
            name = function.__name__
            params = ""
            for i in [str(p) for p in args]:
                params = params + i + ", "
            for i in kwargs.values():
                params = params +  str(i) + ","        
            log_str = f"calling {name} with arguments{params}return value {return_value} at time - {t_str}\n"
            f.write(log_str)
        return return_value
    return wrapper

@logging
def sample_function(param1, param2, param3):
    print(f"hai from sample function {param1}, {param2}, {param3}")
    return str(param1) + str(param2) + str(param3)

class MyFlask():
    def __init__(self):
        self._route = {}

    def route(self, url):
        def wrapper(func):
            print(f"registering route with {url}")
            self._route[url] = func
            return func
        return wrapper
    
app = MyFlask()


@app.route("/index")
def index():
    return "Hello world"
#index = app.route("/index")(index)

class MyDecorator():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, preprocess, postprocess):
        print(f"calling constructor of mydecorator")
        self.__preprocess = preprocess
        self.__postprocess = postprocess
    
    def __preprocessing(self, *args, **kwargs):
        """converting all argurments into upper case strings"""
        print("preprocessing....")
        self._args = tuple([i.upper() if isinstance(i, str) else i for i in args])
        self._kwargs = {}
        for (k,v) in kwargs.items():
            if isinstance(v, str):
                self._kwargs[k] = v.upper()
            else:
                self._kwargs[k] = v
    
    def __postprocessing(self, values):
        """converting all the values into upper case strings"""
        print("postprocessing....")
        if(isinstance(values, str)):
            values = values.upper()
            return values
        elif (isinstance(values,Iterable)): # hasattribute(values, "__iter__")
            for i in range(len(values)):
                if isinstance(values[i], str):
                    values[i] = values[i].upper()
            
        return values
    
    def __call__(self, func):
        """this magic method will be called when calling the object()"""
        def wrapper(*args, **kwargs):
            if self.__preprocess:
                self.__preprocessing(*args, **kwargs)
            return_value = func(*args, **kwargs)
            if self.__postprocess:
                return_value = self.__postprocessing(return_value)
            return return_value
        return wrapper

@MyDecorator(False, True)
def processing_data(arg1, arg2, arg3, a = 2, b = 3, c = 4):
    print("processing data......")
    print(f"{arg1} {arg2} {arg3} a {a} b {b} c {c}")
    l1 = [arg1, arg2, arg3, a, b, c, "hello world", "abc", "def", "abcdef"]
    return l1

#processing_data = MyDecorator(processing_data, True, True)

def func(msg):
    print(f"this is the {msg}")

class MyProperty:
    def __init__(self, fg, fs = None, fd = None):
        print("calling myproperty")
        self._g = fg
        self._s = None
        self._d = None
    
    def __set_name__(self, owner, name):
        self.private_name = "_" + name
    
    def __set__(self, obj, value):
        self._s(obj, value)

    def __get__(self, obj, objtype):
        return self._g(obj)
    
    def getter(self, func):
        self._g = func
        return self
    
    def setter(self, func):
        self._s = func
        return self
    
    def deleter(self, func):
        self._d = func
        return self
    
    def __delete__(self, obj):
        if(self._d != None):
            self._d(obj)
        else:
            raise AttributeError()

class MyTest:
    def __init__(self):
        self._value = 0
    
    @MyProperty
    def value(self):
        print("getting value")
        return self._value
    
    @value.setter
    def setvalue(self, value):
        print("setting value")
        self._value = value

    @value.deleter
    def delvalue(self):
        print("deleting value")
        del self._value

    # value = MyProperty(value)
    # value = value.setter(setvalue)
    # value = value.deleter(delvalue)



if __name__ == "__main__":

    obj = MyTest()
    obj.value = 10
    print(obj.value)
    del obj.value

    sys.exit(0)

    print(processing_data("a",1, "b", 2, [1,2,3,4, "a", "b", "c"], {1:"a", "ABC":"123", "abc":"hello world"}))
    print(index())
    print(sample_function(10, "hello world", param3 = [1,2,3]))
    #sample_function = sample_decorator(sample_function)
    #sample_function(10, 20, param3=30)
    print(my_tokenize("this,is, a, sample"))
    print(my_tokenize("this is a sample"))
    print(dir(my_tokenize))