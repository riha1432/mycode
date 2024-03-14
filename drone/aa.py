def ca(p):
    a = p/101325
    b= 1/5.25588
    c = pow(a,b)
    c = 1 - c
    c = c/0.0000225577
    return c


def cp(A):
     c = A * 0.0000225577
     b = 1/5.25588
     c = 1-c
     a = pow(c,1/b)
     a= a*101325
     return a