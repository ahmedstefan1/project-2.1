from threading import *


# maakt een nieuwe thread aan
def background(func):
    global thread
    thread = Thread(target=func)
    thread.start()


def backgroundarg(func, arg):
    global thread
    thread = Thread(target=func, args=arg)
    thread.start()


