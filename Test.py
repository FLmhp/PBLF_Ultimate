import re

# 示例字符串
text = "这里有123个苹果，456个橙子，789个香蕉。"

# 使用正则表达式提取所有数字
numbers = re.findall(r'\d+', text)

# 打印提取的数字
print("提取的数字:", numbers)

# 修改提取的数字（例如，每个数字加100）
modified_numbers = [str(int(num) + 100) for num in numbers]

# 打印修改后的数字
print("修改后的数字:", modified_numbers)

# 定义一个替换函数
def replace_numbers(match):
    # 获取匹配的数字
    num = match.group()
    # 找到对应的修改后的数字
    modified_num = modified_numbers[numbers.index(num)]
    return modified_num

# 使用re.sub()函数将修改后的数字重新写入字符串
modified_text = re.sub(r'\d+', replace_numbers, text)

# 打印修改后的字符串
print("修改后的字符串:", modified_text)