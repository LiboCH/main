def print_formatted(number):
    for i in range(1,number+1):
        blen=len(str(bin(number+1))[2:])
        print("{:>{blen}} {:>{blen}} {:>{blen}} {:>{blen}}".format(i,str(oct(i))[2:],str(hex(i)).upper()[2:],str(bin(i))[2:], blen=blen))
    # your code goes here

if __name__ == '__main__':
    n = int(input())
    print_formatted(n)
