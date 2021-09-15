global var

def funcA():
    global var
    var = 10

def funcB():
    print(var)
    
funcA()
funcB()