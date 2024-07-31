# @-*- coding = utf-8 _*_
# @Time : 2024/6/2 2:32
# @Author : 杨昌军
# @File : AllUniversity.py
# @Software : PyCharm


import json
import pandas as pd
import re
from IPython.display import display

# 读取JSON文件
with open('院校信息库_中国研究生招生信息网.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# 清理和提取数据的函数
def clean_data(entry):
    title = entry["标题"].strip()
    tag = entry.get("标签", "").strip()

    schdepartment = entry["schdepartment"]
    schdepartment = re.sub(r'\n', '', schdepartment)  # 去掉换行符
    schdepartment = re.sub(r'\s+', ' ', schdepartment).strip()  # 去掉多余的空格

    # 提取隶属信息
    affiliation_match = re.search(r'隶属：\s*([^ ]+)', schdepartment)
    affiliation = affiliation_match.group(1) if affiliation_match else ''

    # 提取研究生院和自划线信息
    postgraduate_institute = '研究生院' in schdepartment
    self_delineation = '自划线' in schdepartment

    return {
        "Title": title,
        "Tag": tag,
        "Affiliation": affiliation,
        "Postgraduate Institute": postgraduate_institute,
        "Self Delineation": self_delineation
    }


# 清理所有数据
cleaned_data = [clean_data(entry) for entry in data]

# 转换为DataFrame
df = pd.DataFrame(cleaned_data)

# 存储为Excel文件
df.to_excel('cleaned_university_data.xlsx', index=False)

# 存储为JSON文件
df.to_json('cleaned_university_data.json', orient='records', force_ascii=False)

print("Data has been saved to 'cleaned_university_data.xlsx' and 'cleaned_university_data.json'")

