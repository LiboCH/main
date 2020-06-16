from pprint import pprint
def print_rangoli(size):
#    for i in range(1,size*2):
#        m_str=''
#        k_size=(2*size-1)-2*abs(i-size)
#        for k in range(0,k_size):
#            print(i,k,abs(k-(size-1-abs(i-size))))
#            mod=abs(k-(size-1-abs(i-size)))
#            m_str=m_str+'-'+chr(96+size+size-abs(i-size) +mod)
#        print(m_str)
    y=2*size-1
    x=y+2*(size-1)
    final_array = [ ( ['-'] * x) for i in range (y) ]
    i_x=0
    for t_x in  range (x):
        i_y=0
        if t_x % 2 == 0 :
            for t_y in range(y):
                if  t_y  >= size -1 -i_x and t_y <= size -1 +i_x :
                    final_array[t_y][t_x]=chr(96+ size -i_y )
                    if t_y < y/2-1 :
                        i_y+=1
                    else:
                        i_y-=1
            if t_x < x/2-1 :
                i_x+=1
            else:
                i_x-=1
    for x in range(len(final_array)):
        for y in range(len(final_array[x])):
            print(f'{final_array[x][y]}',end='')
        print()

if __name__ == '__main__':
    n = int(input())
    print_rangoli(n)
