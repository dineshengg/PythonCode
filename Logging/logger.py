""""
Author: Dinesh Kumar K

Problem: Trying to create logger class using context manager but the problem is file will be opened everytime log function is called

Solution: We create a customer context manager and make it singleton so that it will not create file object again and 
again yet get the benefit of context manager.

Note: This implementation is not thread safe need to be used in single threaded environments only.
"""


import os
import sys

class Logger:
    def __init__(self, path: str = os.path.join("/documents","logging.txt")):
        self._path = path

    def __del__(self):
        if hasattr(Logger.FileContext, "instance"):
           delattr(Logger.FileContext, "instance")
    
   
    def log(self, level: int = 0, severity: int = 0, message: str = ""):        
        if message is None or message == "":
            print("Empty message not logging")
            return None
        try:
            with Logger.FileContext(self._path) as file:
                file.write(str(level) + str(severity) + message + "\n")
        except IOError as e:
            print(f"Error while opening the file for logging {e}")
        finally:
            print("logging in done")
    

    class FileContext:
        """creating a singleton filecontext object so that contextmanager will not create new instance again"""
        _opened = None
        def __new__(cls, *args, **kwargs):
            if not hasattr(cls, "instance"):
                print("single object of filecontext class created")
                obj = super().__new__(cls)
                cls.instance = obj
            return cls.instance
        
        def __del__(self):
            ###this will be close the file only once when the singleton goes out of scope collected by gc
            print("closing the file from context manager")
            self._file.close()
            
        def __init__(self, filepath=None):    
            print("filecontext constructor called")
            if type(self)._opened is None:
                print("file context init called")
                self._filepath = filepath

        def __enter__(self):
            if type(self)._opened is None:
                try:
                    print("opening file for writting into log file")
                    self._file = open(self._filepath, "a+t")
                except IOError as e:
                    print(f"Error opening the file for logging {e}")
            type(self)._opened = True
            return self._file
        
        def __exit__(self, *args):
            ###not closing the file here as it will be closed by the destructor when the \
            #class object get destroyed hence point this instance as a member of class so that \
            # gc will not collect and call del when the class stack of the log functions returns
            return True


if __name__ == "__main__":
    log = Logger("D:\\Dinesh\\Project\\Django\\logging_sample.txt")
    log.log(1, 2, "Connecting to network")
    log.log(1, 2, "Connecting to network again")
    log.log(1, 2, "Connecting to network")
    log.log(1, 2, "Connecting to network again")
    del log
    print("completed cleanup")
    
