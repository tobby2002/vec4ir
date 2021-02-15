# https://www.programiz.com/python-programming/global-local-nonlocal-variables

x = "global "

def foo():
    global x
    y = "local"
    x = x * 2
    print(x)
    print(y)
foo()

def init():
    global x
    x = 'init' + ' ' + x
    print('x on init: %s' % x)
init()
