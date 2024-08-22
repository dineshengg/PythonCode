#this code shares the samples of decorators and generators
#closure captures outerscope function variables under cell that will be shared between outscope and innner scope under __closure__ dictionary
#closure is used for data hiding when we want to create less no of functions but want data hiding then closure can be used for this
def incrementby(var):
    def wrapper(n):
        return n + var
    return wrapper

def multiplier(i):
    def wrapper(j):
        return i*j
    return wrapper
#data hiding of i which will be used by the wrapper function object as a closure variable or free-variable
def increment():
    inc = 0
    def wrapper():
        nonlocal inc
        inc += 1
        return inc
    return wrapper

#example of combining closure and decorator to track the number of times a call for a function has been made
def count_func_calls(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        print(f"calling {wrapper.count} of {func.__name__}")
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper

@count_func_calls
def db_connections(url):
    print(f"connection to database {url}")

if __name__ == "__main__":
    db_connections("http://localhost:80")
    db_connections("http://localhost:443")

    i1 = increment()
    for _ in range(0, 10):
        print(i1())

    i2 = increment()
    for _ in range(0, 10):
        print(i2())
    

    f1 = incrementby(10)
    f2 = incrementby(2)
    l1 = [f1, f2]
    print([[f(i) for i in range(2)] for f in l1])

    # example to show using lambda functions wont capture the outerscope environment variables as whe closure is created below it will capturing i but when exceuting lambda it take the last value 9
    multipliers = []
    for i in range(1,2):
        multipliers.append(lambda x: i*x)
    for m in multipliers:
        print(m(10)) # all the 9 interations print only 90 since lambda wont capture the outerscope environment variables as it is while its executing it take the last value of x which is 9

    m1 = multiplier(1)
    m2 = multiplier(2)
    #multiply all the input by 1
    print(m1(10))
    print(m1(20))
    #muliply all the input by 2
    print(m2(10))
    print(m2(20))
