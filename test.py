a, b = 2, 5

def foo(a, b):
    w=1
    while b>0:
        c=a
        d=w
        print(b, "|", end=" ")
        while c>1:
            print(c, end=" ")
            w+=d
            c-=1
        b-=1
        print("\t", w)
    return w

foo(a, b)

def goo(a, b):
    w=1
    while b>0:
        print(b, "|", end=" ")
        b+=1000*a
        d=w
        while b>2000:
            print(b, end=" ")
            w+=d
            b-=1000
        b-=1000
        b-=1
        print()
    return w

print(goo(a, b))