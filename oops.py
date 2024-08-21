"""Example class for all oops related concepts"""
# constructor and destructor methods
#static functions
#class functions
#properties 
#Multiple inheritance and multilevel inheritance
#magic methods and operator overloading
#overloading methods using @dispatch
#class inheritance is nothing but overriding methods and using method resolution order 


import sys
from functools import singledispatch, singledispatchmethod
from typing import Any

class Person:
    #class variable 
    name: str = "John"
    age: int = 10
    languages: list[str] =[]

    def getname(self):
        return Person.name #this gets the class variable which is immutable
    
    def setname(self, data):
        self.name = data # this creates a new instance variable for that object p1 and set the value and return it to caller. p2 wont have it yet

    def __init__(self, name:str, age:int):
        print(f"creating new instance variable {name}")
        self._name: str = name #this creates a private instance variable 
        self.age: int = age #call the setter property for age dont use self._age = age instead use like this so that it will validate the age
    
    def __del__(self):
        print(f"object getting deleted for {self._name}")
        #clean up all resources here

    #class method are used to access the class variables
    @classmethod
    def change_language(cls, language:list[str]):
        cls.languages = language    
    
    #class method returns an object
    @classmethod
    def from_list(cls, lst):
        name, age = lst
        return cls(name, age)
    
    #static methods are normal functions that are used in class scope instead of having a different module
    @staticmethod
    def check_age(age):
        return age > 40
    
    @staticmethod
    def create_person():
        return Person.from_list(["No name", 11])
    
    #Code to explain about property
    def get_age(self):
        return self.age
    
    @property
    def age(self):
        print("get property for age")
        return self._age
    
    @age.setter
    def age(self, age: int) -> None:
        try:
            int(age)
            if age >= 10:
                self._age = age #create a instance variable and assign the age value using property
                #self.age = age #this code will go for infinite loop of calling this setter property again and again untill stack overflow happens
            else:
                raise ValueError("Invalid age")
        except ValueError:
            raise TypeError("Pass a valid type of age parameter")
    
    @age.deleter
    def age(self):
        #del self._age
        #self._age = None
        raise AttributeError("Age is a private variable can't be deleted")
    
    def __repr__(self):
        return f"Person is {self._name} with {self._age}"
    
    #__str__() is having preference in print and str() than __repr__() unless used explicitly like repr()
    def __str__(self):
        return f"{self._name} and {self._age}"
    
    def __lt__(self, other):
        return self._age < other._age

    def __bool__(self):
        return True if self._name and self._age else False

class A:
    def __init__(self, val):
        print("A class")
        self._a = val
class B(A):
    def __init__(self, val1, val2):
        print("B class")
        super().__init__(val1, val2) # this calls C as per MRO
        self._b = val2
class C(A):
    def __init__(self, val1, val2):
        print("C class")
        super().__init__(val1) # this calls A as per MRO
        self._c = val2

class D(B, C):
    def __init__(self, val1, val2, val3, val4):
        print("D class")
        super().__init__(val1, val2) # this calls B as base
        self._d = val4

##code to show how to avoid overriding the method of derived class while calling the functions overriden by derived classes.
class Base(object):
    def __init__(self, val):
        print("Base init")
        self._base_val = val
        self.__method_cal1() #this will call the base class method
        self.method_cal1() #method_cal1 of the derived class will be called here not the base class method_cal1 method

    def method_cal1(self):
        print("Base method_cal1")

    __method_cal1 = method_cal1 # we are creating a class private variable that has the object of base class method_cal1

#sample code to avoid overriding the method_cal1 is derived class
class Derived(Base):
    def __init__(self, val):
        super().__init__(val)
        print("Derived init")
        self._derived_val = val
        self.__method_cal1() #we are creating a class private variable that has the object of derived class method so it not overridding while calling the class(
        
    def method_cal1(self):
        print("Derived method_cal1")

    __method_cal1 = method_cal1

class MetaClass(type):
    def __new__(cls, clsname, bases, values, kwargs = 1):
        print(f"calling new {cls}")
        for attr, val in values.items():
            print(attr, val)
        return super().__new__(cls, clsname, bases, values)

class MyClass(metaclass=MetaClass):
    class_attr1 = 10
    class_attr2 = "hello world"    
    def __new__(cls, *args, **kwargs):
        print(f"Myclass __new__ {cls}")
        for attr, val in cls.__dict__.items():
            print(f"instance attribute {attr} and value {val}")
        for i in args:
            print(i)
        for key, value in kwargs.items():
            print(key, value)
        return super().__new__(cls)

    def __init__(self, value1, value2):
        print("init function")
        self.instance_value1 = 10
        self._instance_value2 = "hello world"
        print(f"value1 = {value1} and value2 = {value2}")

    def func1(self):
        print("func1")
    
    @classmethod
    def classfunc1(cls):
        print("classfunc1")

    @staticmethod
    def staticfunc1():
        print("static func1")

#using single dispatch to override first parameter of non class member functions

@singledispatch
def func1(val: Any, verbose = None)->None:
    print(f"func1 base class {val}")

@func1.register(str)
def func(val:str, verbose = None)->None:
    print(f"func1 str having value {val}")

@func1.register(int)
@func1.register(float)
def _(val:float|int, verbose = None)->None:
    print(f"func1 getting instance {type(val)} having {val}")

func1.register(type(None), lambda _, verbose=None: print("func1 getting none"))
#class single dispatch using singledispatch method
class classdispatch():
    @singledispatchmethod
    def func1(self, val: Any) -> None:
        print(f"func1 with generic value {val}")

    @func1.register
    def _(self, val:float)->None:
        print(f"func1 with float value {val}")

def decorator_func(func):
    print("calling decorator function 111")
    def func_type(typ):
        print("calling func_type")
        def wrapper(func1):
            def func_proxy(*args, **kwargs):  
                print("doing some operation")
                if isinstance(typ, int):
                    return func1(*args, **kwargs)
                else:
                    return TypeError("function parameter not defition")
            return func_proxy  
        return wrapper
    func_type.__name__ = func.__name__
    return func_type

@decorator_func
def my_func(a):
    return a

@my_func(int)
def func_1(a:int)->None:
    print("func_1")

def sample_dec1(name):
    def wrapper(func):
        print("changing name")
        func.__name__ = name
        return func
    return wrapper


def func_1(a, b):
    return a+b

###thing to note here is _ is used for protected variable and __is is used for private variables. Here the _methods are considered protected and can be overridden but the __method cant be overridden it was name mangled as per the class it was present
class B1:
    def __init__(self):
        pass

    def _dummy1(self):
        self.__dummy2()
        self._dummy3()
        print("B1 dummy1")

    def __dummy2(self):
        print("B1 dumm2")
    
    def _dummy3(self):
        print("B1 dummy3")

class B2(B1):
    # def _dummy1(self):
    #     self.__dummy2()
    #     print("B2 dummy")
    
    def __dummy2(self):
        print("B2 dummy2")

    def _dummy3(self):
        print("B2 dummy3")

if(__name__ == "__main__"):

    b1 = B2()
    b1._dummy1()
    #b1.__dummy2()

    obj = MyClass(1, "hello world")

    # person1 = Person("ganesh", 100)
    # print(person1.age)
    # person1.age = 100
    # #del person1.age raise the exception AttributeError

    # obj = Derived(10)
    # obj.method_cal1()





    # # sample_wrapper = sample_dec1("test1")
    # # f1 = sample_wrapper(func_1)
    # # f1(10, 20)

    # sys.exit(0)

    # d = D(1,2,3,4)
    # print(D.mro()) #method resolution order based on DFS

    # obj1 = classdispatch()
    # obj1.func1(float(10.1))
    # obj1.func1("hello world")


    # func1(10)
    # func1(11.1)
    # func1("hello")
    # func1([1,2,3])
    # func1(None)


    # p1 = Person("ganesh", 30)
    # p2 = Person("suresh", 41)

    # print(bool(p1))

    # print(p1.get_age())

    # print(p1)
    # print(str(p1)) # by default str is invoked if not provided repr is invoked

    # print(repr(p1))

    # #code for class method
    # Person.change_language(["English", "Tamil"])
    # print(p1.languages)
    # p1.change_language(["Tamil", "English"])
    # print(p1.languages)
    # print(Person.languages)
    # print(p1.check_age(41))

    # p3 = Person(*["Tamilarasan", 45])
    # p4 = Person.from_list(["Arasan", 50])

    # p5 = Person.create_person()



    # sys.exit(0)


    # p1 = Person()
    # p2 = Person()

    # print("-" * 80)
    # print(id(p1.name))
    # print(id(p2.name))

    # Person.name = "ganesh" # class variable is getting changed here

    # print(id(p1.name))
    # print(id(p2.name))
    # print("-" * 80)

    # print(p1.getname()) # gets the class variable name common for all instances
    # p1.setname("ganesh") #attaches the attribute name to the instance p1
    
    # print(p1.getname()) # this gets the instance variable created for p1  
    # p1.name = "suresh" # another way to create a instance variable for p1   
    # print(p2.getname()) # this get the class variable as instance variable is not yet created
    
    # p1.languages.append("English")
    # p1.languages.append("Tamil")

    # print(p1.languages) #updates the class variable
    # print(p2.languages) # updates the class variable
    
    # p1.languages = ["Tamil", "Hindi"] # crates a new instance variable for p1

    # print(p1.languages) #prints the instance variable
    # print(p2.languages) #prints the class variable
    # print(Person.languages) # prints the class variable

    # del p1.languages # delets the p1 instance variable
    # print(p1.languages) # now p1 language attribute deleted it prints the class variable
    # print("-" * 90)

    # ###constructor and destructor