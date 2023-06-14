# @-*- coding = utf-8 _*_
# @Time : 2023/6/14 21:06
# @Author : 杨昌军
# @File : GreenLifeIdea.py
# @Software : PyCharm

import os
import json
import pandas as pd

directory = r"E:\OneDrive - cqut.edu.cn\Desktop\抖音数据"

def scan_files(directory):
    directory_name_list = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            directory_name_list.append(filename)
    return directory_name_list


def data(directory,directory_name):
    path = directory + '\\' + directory_name
    #print(path)
    data_list = []
    for filename in os.listdir(path):
        #print(filename)
        if filename.endswith(".txt"):
            path_file = os.path.join(path, filename)
            #print(path_file)
            with open(path_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                #print(data)

                item_list = []
                for data in data['data']:
                    item = {}  # 注意，item空字典一定要在循环里面，否则会出错，因为每循环一次就要传递一次参数，所以必须在里面。排查了好久。
                    item['search_word'] = directory_name
                    item['video_id'] = data['aweme_info']['aweme_id']
                    item['video_title'] = data['aweme_info']['desc']
                    item['video_create_time'] = data['aweme_info']['create_time']
                    item['video_duration'] = data['aweme_info']['video']['duration']
                    item['video_play_count'] = data['aweme_info']['statistics']['play_count']
                    item['video_digg_count'] = data['aweme_info']['statistics']['digg_count']
                    item['video_comment_count'] = data['aweme_info']['statistics']['comment_count']
                    item['video_share_count'] = data['aweme_info']['statistics']['share_count']
                    item['video_collect_count'] = data['aweme_info']['statistics']['collect_count']
                    item['video_download_count'] = data['aweme_info']['statistics']['download_count']
                    item['author_uid'] = data['aweme_info']['author']['uid']
                    item['author_nickname'] = data['aweme_info']['author']['nickname']
                    item['aweme_count'] = data['aweme_info']['author']['aweme_count']
                    item['author_follower_count'] = data['aweme_info']['author']['follower_count']
                    item['is_verified'] = data['aweme_info']['author']['is_verified']
                    item['verification_type'] = data['aweme_info']['author']['verification_type']
                    item['enterprise_verify_reason'] = data['aweme_info']['author']['enterprise_verify_reason']
                    item['author_signature'] = data['aweme_info']['author']['signature']
                    item['author_sec_uid'] = data['aweme_info']['author']['sec_uid']
                    data_list.append(item)  # 将每次循环生成的item字典添加到列表中
    return data_list
            #data_list.append(data)

data_whole_list = []
for directory_name in scan_files(directory):
    for accurate_data in data(directory,directory_name):
        data_whole_list.append(accurate_data)

# 将列表转换为 DataFrame
df = pd.DataFrame(data_whole_list)

# 将 DataFrame 写入到 Excel 文件
df.to_excel("green_life_video.xlsx", index=False)


'''  #ChatGpt对上面代码的注释。
# 导入所需的模块
import os
import json
import pandas as pd

# 定义数据所在的目录
directory = r"E:\OneDrive - cqut.edu.cn\Desktop\抖音数据"

# 定义一个函数，用于扫描指定目录下的所有子目录
def scan_files(directory):
    directory_name_list = []  # 初始化一个空列表，用于存储子目录名
    for filename in os.listdir(directory):  # 遍历指定目录下的所有文件和子目录
        path = os.path.join(directory, filename)  # 获取完整的文件或子目录路径
        if os.path.isdir(path):  # 如果这是一个子目录
            directory_name_list.append(filename)  # 将子目录名添加到列表中
    return directory_name_list  # 返回存储有所有子目录名的列表

# 定义一个函数，用于处理指定目录下的数据
def data(directory,directory_name):
    path = directory + '\\' + directory_name  # 获取完整的子目录路径
    data_list = []  # 初始化一个空列表，用于存储数据
    for filename in os.listdir(path):  # 遍历子目录下的所有文件
        if filename.endswith(".txt"):  # 如果文件是一个.txt文件
            path_file = os.path.join(path, filename)  # 获取完整的.txt文件路径
            with open(path_file, 'r', encoding='utf-8') as f:  # 以读模式打开.txt文件
                data = json.load(f)  # 加载.txt文件中的json数据
                for data in data['data']:  # 遍历json数据中的每一个数据项
                    item = {}  # 初始化一个空字典，用于存储数据
                    # 以下是提取json数据的过程，将所需的数据存储到字典中
                    item['search_word'] = directory_name
                    # 省略了一部分字段，因为item字典的项注释都相同...
                    item['author_sec_uid'] = data['aweme_info']['author']['sec_uid']
                    data_list.append(item)  # 将字典添加到列表中
    return data_list  # 返回存储有所有数据的列表

data_whole_list = []  # 初始化一个空列表，用于存储所有的数据
for directory_name in scan_files(directory):  # 遍历所有子目录
    for accurate_data in data(directory,directory_name):  # 遍历子目录中的所有数据
        data_whole_list.append(accurate_data)  # 将数据添加到总的列表中

df = pd.DataFrame(data_whole_list)  # 将包含所有数据的列表转换为 DataFrame

df.to_excel("output.xlsx", index=False)  # 将 DataFrame 写入到 Excel 文件中，不包含索引列
'''