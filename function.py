# 对文本进行特殊处理
keyword = [
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
    'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
    'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
]


def edit_text(lines):
    # 删除注释和头文件
    notes_flag = False
    for line in lines[::-1]:
        lines_index = lines.index(line)
        line_str = list(line)

        # 删除单行注释
        if '//' in line:
            del lines[lines_index]

        # 删除多行注释
        elif '*/' in line:
            notes_flag = True
            del lines[lines_index]
        elif '/*' in line:
            notes_flag = False
            del lines[lines_index]
        elif notes_flag is True:
            del lines[lines_index]

        # 删除头文件
        elif '#include' in line or '#define' in line or '#undef' in line \
                or '#ifdef' in line or '#ifndef' in line or '#endif' in line:
            del lines[lines_index]

    # 删除引号间的内容以及一些不必要的标点符号
    for line in lines:
        lines_index = lines.index(line)
        # 将字符串转化为列表方便修改
        line_str = list(line)
        # 删除引号间的内容
        if '"' in line:
            i = line.find('"')
            j = line.rfind('"')
            line_str[i:j + 1] = " "
        # 将不重要的标点符号变为空格
        for unit in line_str:
            str_index = line_str.index(unit)
            if unit == '(' or unit == ')' or unit == '[' or unit == ']' or unit == ':' or unit == ';':
                line_str[str_index] = ' '
        # 将列表转化为字符串
        line = ''.join(line_str)
        # 更新文本
        lines[lines_index] = line

    # 如果遇到 ‘{’，让其前后增加空格
    for line in lines:
        lines_index = lines.index(line)
        # 将字符串转化为列表方便修改
        line_list = list(line)
        index = line.find('{')
        if index >= 0:
            line_list.insert(index + 1, ' ')
            line_list.insert(index, ' ')
            # 将列表转化为字符串
            line = ''.join(line_list)
            # 更新文本
            lines[lines_index] = line

    # 将每行结尾换行前加上空格
    for line in lines:
        lines_index = lines.index(line)
        # 将字符串转化为列表方便修改
        line_list = list(line)
        line_list[len(line_list) - 1] = ' '
        line_list.append('\n')
        # 将列表转化为字符串
        line = ''.join(line_list)
        # 更新文本
        lines[lines_index] = line
    return lines


# 计算关键字个数
def count_keyword(lines):
    total_num = 0
    for line in lines:
        str = line.split(' ')
        for i in str:
            for j in keyword:
                if i == j:
                    total_num += 1
                    break
    return total_num


# 计算 switch 和 case 个数
def count_switch(lines):
    flag = False    # 判断当前是否处在一个 switch case 结构中
    temp_num = 0    # 每次一组 switch case 中 case 的个数
    stack_num = 0   # 栈中元素个数
    switch_num = 0
    case_num = []
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
    return switch_num, case_num


# 计算 if-else 和 if-elseif-else 的个数
def count_if_else(lines):
    if_else_num = 0
    if_elseif_else_num = 0
    if_else_stack = []  # 用栈完成匹配
    else_if_flag = False    # 是否有 else if
    else_flag = False       # 是否有 else
    for line in lines:
        lines_index = lines.index(line)
        str = line.split(' ')
        # 当遇到 if，else if，else，{ 直接入栈
        if 'else' in str and 'if' in str:
            if_else_stack.append('else if')
        elif 'if' in str:
            if_else_stack.append('if')
        elif 'else' in str:
            if_else_stack.append('else')
        if '{' in str:
            if_else_stack.append('{')
        # 当遇到 } 需要出栈，直到匹配到 {
        if '}' in str:
            temp = if_else_stack.pop()
            if temp == '{':
                continue
            while True:
                if temp == 'else':
                    # 存在else
                    else_flag = True
                    temp = if_else_stack.pop()
                elif temp == 'else if':
                    # 存在 else if
                    else_if_flag = True
                    temp = if_else_stack.pop()
                elif temp == 'if':
                    # 遇到 if，判断是else if结构还是
                    if else_flag is True and else_if_flag is True:
                        if_elseif_else_num += 1
                    elif else_flag is True and else_if_flag is False:
                        if_else_num += 1
                    temp = if_else_stack.pop()
                elif temp == '{':
                    else_if_flag = False
                    else_flag = False
                    break
    # 栈中还会存在 if，else if,else，需要全部出栈匹配
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
    return if_else_num, if_elseif_else_num
