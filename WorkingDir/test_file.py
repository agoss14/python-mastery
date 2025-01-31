# test_file.py

def some_func(x,y,*args,**kwargs):
    print(sum(args))
    #print(x + y + z)


some_func(1,2,3,z=4)
