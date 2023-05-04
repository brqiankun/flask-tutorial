# def hi(name = "bairui"):
#     print("now you are inside the hi() functon")

#     # nested function
#     def greet():
#         return "now you are in the greet() function"
    
#     def welcome():
#         return "now your are in the welcome() function"
    
#     print("now you are back in the hi() function")
#     if name == "bairui":
#         return greet
#     else:
#         return welcome

# greet() 

# a = hi()
# print(a)

# print(a())

# def hi():
#     return "hi yasoob!"

# def doSomethingBeforeHi(func):
#     print("I am doing some boring work before executing hi()")
#     print(func())

# doSomethingBeforeHi(hi)

# Decorators let you execute code before and after a function.

# def a_new_decorator(a_func):
#     def wrapTheFunction():
#         print("I am doing some boring work before executing a_func()")

#         a_func()

#         print("I am doing some boring work after executing a_func()")

#     return wrapTheFunction


# def a_function_requiring_decoration():
#     print("I am the function which needs some decoration to remove my foul smell")

# a_function_requiring_decoration()

# a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)

# a_function_requiring_decoration()

# @a_new_decorator
# def a_function_requiring_decoration():
#     print("I am the function which needs some decoration to remove my foul smell")

# a_function_requiring_decoration()


# @a_new_decorator
# def a_function_requiring_decoration():
#     print("I am the function which needs some decoration to remove my foul smell")
# # the @a_new_decorator is just a short way of saying
# # a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)

# print(a_function_requiring_decoration.__name__)
# # Output: wrapTheFunction

from functools import wraps

def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")

        a_func()

        print("I am doing some boring work after executing a_func()")
    
    return wrapTheFunction

@a_new_decorator
def a_function_requiring_decoration():
    print("I am the function which needs some decoration to remove my foul smell")

print(a_function_requiring_decoration.__name__)

from functools import wraps
def decorator_name(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)
    return decorated

@decorator_name
def func():
    return("Function is running")

can_run = True
print(func())
# Output: Function is running

can_run = False
print(func())
# Output: Function will not run


#use-cases

# from functools import wraps

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             authenticate()
#         return f(*args, **kwargs)
#     return decorated

# from functools import wraps

# def logit(func):
#     @wraps(func)
#     def with_logging(*args, **kwargs):
#         print(func.__name__ + " was called")
#         return func(*args, **kwargs)
#     return with_logging

# @logit
# def addition_func(x):
#    """Do some math."""
#    return x + x


# result = addition_func(4)
# # Output: addition_func was called

from functools import wraps

def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # Open the logfile and append
            with open(logfile, 'a') as opened_file:
                # Now we log to the specified logfile
                opened_file.write(log_string + '\n')
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator

@logit()
def myfunc1():
    pass

myfunc1 = logit()(myfunc1)  # logging_decorator(myfunc1) => wrapped_function

myfunc1()
# Output: myfunc1 was called
# A file called out.log now exists, with the above string

@logit(logfile='func2.log')
def myfunc2():
    pass

myfunc2()
# Output: myfunc2 was called
# A file called func2.log now exists, with the above string