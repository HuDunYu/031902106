keyword = [
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for',	'goto', 'if',
    'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
    'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
]

file_path = 'c.txt'
with open(file_path) as file_object:
    lines = file_object.readlines()

for line in lines:
    lines_index = lines.index(line)
    line_str = list(line)

    # 删除单行注释
    if '//' in line:
        del lines[lines_index]

    # 删除多行注释
    # elif '/*' in line:
    #     index = lines.index(line)
    #     lines.remove(line)
    #     for line_temp in lines[index:]:
    #         if '*/' not in line:
    #             lines.remove(line)
    #         else:
    #             lines.remove(line)
    #             break

    elif '#include' in line or '#define' in line or '#undef' in line or '#ifdef' in line or '#ifndef' in line or '#endif' in line:
        del lines[lines_index]

for line in lines:
    lines_index = lines.index(line)
    line_str = list(line)
    # 删除引号间的内容
    if '"' in line:
        i = line.find('"')
        j = line.rfind('"')
        line_str[i:j+1] = " "
    # 将不重要的标点符号变为空格
    for unit in line_str:
        str_index = line_str.index(unit)
        if unit == '(' or unit == ')' or unit == '[' or unit == ']' or unit == ':' or unit == ';':
            line_str[str_index] = ' '
    line = ''.join(line_str)
    lines[lines_index] = line

# 如果遇到 ‘{’，让其前后增加空格
for line in lines:
    lines_index = lines.index(line)
    line_list = list(line)
    index = line.find('{')
    if index >= 0:
        line_list.insert(index+1,' ')
        line_list.insert(index, ' ')
        line = ''.join(line_list)
        lines[lines_index] = line

# 将每行结尾换行前加上空格
for line in lines:
    lines_index = lines.index(line)
    line_list = list(line)
    line_list[len(line_list)-1] = ' '
    line_list.append('\n')
    line = ''.join(line_list)
    lines[lines_index] = line

for line in lines:
    print(line)

total_num = 0
switch_num = 0
case_num = []
if_else_num = 0
if_elseif_else_num = 0
if_else_stack = []
stack_num = 0
flag = False
temp_num = 0

# 计算关键字个数
for line in lines:
    str = line.split(' ')
    for i in str:
        for j in keyword:
            if i == j:
                total_num += 1
                break

# 计算 switch 和 case 个数
for line in lines:
    lines_index = lines.index(line)
    str = line.split(' ')
    if 'switch' in str:
        temp_num = 0
        flag = True
        switch_num += 1
    if 'case' in str:
        temp_num += 1
    if '{' in str and flag is True:
        stack_num += 1
    if '}' in str and flag is True:
        stack_num -= 1
        flag = False
        if stack_num == 0:
            case_num.append(temp_num)
# 计算 if-else 和 if-elseif-else 的个数
if_flag = False
else_if_flag = False
else_flag = False
for line in lines:
    lines_index = lines.index(line)
    str = line.split(' ')
    print(if_else_stack, end=' ')
    print(if_else_num, end=' ')
    print(if_elseif_else_num)
    if 'else' in str and 'if' in str:
        if_else_stack.append('else if')
    elif 'if' in str:
        if_flag = True
        if_else_stack.append('if')
    elif 'else' in str:
        if_else_stack.append('else')
    if '{' in str and if_flag is True:
        if_else_stack.append('{')
    if '}' in str and if_flag is True:
        temp = if_else_stack.pop()
        if temp == '{':
            continue
        while True:
            if temp == 'else':
                else_flag = True
                temp = if_else_stack.pop()
            elif temp == 'else if':
                else_if_flag = True
                temp = if_else_stack.pop()
            elif temp == 'if':
                if else_flag is True and else_if_flag is True:
                    if_elseif_else_num += 1
                elif else_flag is True and else_if_flag is False:
                    if_else_num += 1
                temp = if_else_stack.pop()
            elif temp == '{':
                else_if_flag = False
                else_flag = False
                break
while len(if_else_stack) > 0:
    temp = if_else_stack.pop()
    if temp == 'else':
        else_flag = True
    elif temp == 'else if':
        else_if_flag = True
if else_flag is True and else_if_flag is True:
    if_elseif_else_num += 1
elif else_flag is True and else_if_flag is False:
    if_else_num += 1

print('total num: %d' % total_num)
print('switch num: %d' % switch_num)
print('case num: ', end='')
for num in case_num:
    print(num, end=' ')
print('\nif-else num: %d' % if_else_num)
print('if-elseif-else num: %d' % if_elseif_else_num)
