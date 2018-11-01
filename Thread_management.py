from threading import *

# maakt een nieuwe thread aan
def background(func):
    global thread
    thread = Thread(target=func)
    thread.start()
