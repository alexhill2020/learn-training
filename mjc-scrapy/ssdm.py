# @-*- coding = utf-8 _*_
# @Time : 2024/6/2 3:09
# @Author : 杨昌军
# @File : ssdm.py
# @Software : PyCharm

import json
import pandas as pd
import re
from urllib.parse import unquote


# # 读取JSON文件
# with open('getSs.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
#
# # 转换为DataFrame
# df = pd.DataFrame(data)
#
# # 存储为Excel文件
# df.to_excel('getSs.xlsx', index=False)
#
# print("Data has been saved to 'getSs.xlsx'")


#
# # 读取文件内容
# with open('yx.txt', 'r', encoding='utf-8') as file:
#     data = file.read()
#
# # 定义正则表达式模式
# pattern = re.compile(r'\((\d+)\)(.*?)\n\((\d+)\)(.*?)\s')
#
# # 使用正则表达式查找匹配项
# matches = pattern.findall(data)
#
# # 创建一个数据框
# df = pd.DataFrame(matches, columns=['学校代码', '学校名称', '省市代码', '省市名称'])
#
# # 移除多余的空白字符
# df['学校名称'] = df['学校名称'].str.strip()
# df['省市名称'] = df['省市名称'].str.strip()
#
# # 将数据框保存到Excel文件
# df.to_excel('yx.xlsx', index=False)
#
# print("Data has been saved to 'yx.xlsx'")



# 读取Excel文件
file_path = 'xs-yjfx.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')

# 去掉括号和括号内的内容
def remove_parentheses(text):
    return re.sub(r'\(\d+\)', '', text).strip()

# 应用到所有需要的列
df['院系所'] = df['院系所'].apply(remove_parentheses)
df['专业'] = df['专业'].apply(remove_parentheses)
df['研究方向'] = df['研究方向'].apply(remove_parentheses)

# 创建一个新列来存储解码后的内容
def decode_url(url):
    start = url.find("dwmc=") + 5
    end = url.find("&", start)
    encoded_str = url[start:end]
    decoded_str = unquote(encoded_str)
    return decoded_str

df['学校名称'] = df['页面网址'].apply(decode_url)

# 保存结果到新的Excel文件
output_file_path = 'xs-yjfx_decoded.xlsx'
df.to_excel(output_file_path, index=False)

print("Data has been saved to 'xs-yjfx_decoded.xlsx'")
