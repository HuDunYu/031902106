from function import edit_text, count_keyword, count_switch, count_if_else

# 输入
file_path = input()
rank = int(input())

# 读取文件
with open(file_path) as file_object:
    lines = file_object.readlines()

# 对文件进行必要处理
lines = edit_text(lines)

if rank >= 1:
    total_num = count_keyword(lines)
    print('total num: %d' % total_num)
if rank >= 2:
    switch_num, case_num = count_switch(lines)
    print('switch num: %d' % switch_num)
    print('case num: ', end='')
    for num in case_num:
        print(num, end=' ')
if rank >= 3:
    if_else_num, if_elseif_else_num = count_if_else(lines)
    print('\nif-else num: %d' % if_else_num)
if rank >= 4:
    print('if-elseif-else num: %d' % if_elseif_else_num)
