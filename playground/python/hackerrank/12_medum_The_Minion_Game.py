from pprint import pprint

def minion_game(string):
    v=['A','E','I','O','U']
    total_len=len(string)
    kevin=0
    stuart=0
    for str_pos in range(total_len):
            if string[str_pos] in v:
                kevin+=(len(s) -str_pos)
            else:
                stuart+=(len(s) - str_pos)

    if kevin>stuart:
        print(f'Kevin {kevin}')
    elif stuart>kevin:
        print(f'Stuart {stuart}')
    else:
        print('Draw')
    #print(f'kevin:{kevin} stuart:{stuart}')
if __name__ == '__main__':
    #s = input()
    s = 'BANANA'
    minion_game(s)
