#from itertools import product
#def iter_local(A,B):
#    print(A)
#    i=0
#    last = len(A) * len(B)
#    for a in A:
#        for b in B:
#            print(f'({a}, {b})',end='')
#            i+=1
#            if i < last :print(' ',end='')
#if __name__ == '__main__':
#    A = input().split()
#    B = input().split()
#    iter_local(A,B)


### -elegant solution
from pprint import pprint
from itertools import product

a = map(int, input().split())
b = map(int, input().split())
pprint(a)
print(*product(a, b))
