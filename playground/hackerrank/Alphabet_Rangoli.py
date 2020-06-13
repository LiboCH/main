def print_rangoli(size):
    for i in range(1,size*2):
        m_str=''
        k_size=(2*size-1)-2*abs(i-size)
        for k in range(0,k_size):
            print(i,k,abs(k-(size-1-abs(i-size))))
            mod=abs(k-(size-1-abs(i-size)))
            m_str=m_str+'-'+chr(96+size+size-abs(i-size) +mod)
        print(m_str)

if __name__ == '__main__':
    n = int(input())
    print_rangoli(n)
