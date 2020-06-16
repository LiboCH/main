def merge_the_tools(string, k):
    # your code goes here
    str_len=len(string)
    parts = str_len // k
    part_list=[]
    for part in range(parts):
        part_list.append(string[part*k:part*k+k])
    #print(f'{part_list}')
    for part in part_list:
        seen_list=[]
        tmp_string=''
        for char_pos in range(k):
            if part[char_pos] not in seen_list:
                seen_list.append(part[char_pos])
                tmp_string+=part[char_pos]
        print(tmp_string)

if __name__ == '__main__':
    #string, k = input(), int(input())
    string='AABCAAADA'
    k=3
    merge_the_tools(string, k)
