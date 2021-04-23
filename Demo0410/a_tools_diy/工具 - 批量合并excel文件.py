# @-*- coding = utf-8 _*_
# @Time : 2021/4/17 15:28
# @Author : 杨昌军
# @File : 合并excel文件.py
# @Software : PyCharm

import sys
sys.path.append("..")
import pandas as pd
import os

from a_libs.y_folder import get_this_file_parent_folder as get_p_f,select_folder_path as slc_pth

def merge_excel_file(file_path,file_list):
    style_head = '\033[5;30;47m'  #
    style_end = '\033[0m'
    df_list = []
    print(f"{style_head}即将对{file_path}文件夹中的Excel文件进行合并，先读取Excel文件并将其内容添加到list列表。{style_end}")
    for excel_name in file_list:
        excel_name1 = file_path+'\\'+excel_name
        df_split = pd.read_excel(excel_name1)
        df_list.append(df_split)
        print(f'{excel_name}添加到列表完毕。')
    while True:
        if df_list:
            print(f'{style_head}…………正在合并…………{style_end}')
            df_merged = pd.concat(df_list)
            print(f'{style_head}…………合并完毕，正在输出到总Excel，请稍等…………{style_end}')
            filename = input(f"{style_head}请输入合并后的Excel文件的名称，不用输入后缀名“.xlsx”:{style_end}")
            print(f"{style_head}…………请选择你要存储合并后的Excel文件的文件夹…………{style_end}")
            dir_path = get_p_f()
            dir1_path = slc_pth(dir_path)
            print(f"{style_head}已选择存储文件夹，正在输出到Excel，如数据较多，等待时间可能较久，请耐心等待。{style_end}")
            df_merged.to_excel(dir1_path+'\\'+filename+'.xlsx',index=False)
            print(f"{style_head}输出到Excel完毕，全部流程结束，请打开文件夹{dir1_path}查看！！！{style_end}")
            break
        else:
            s = input(f"{style_head}当前目录下没有文件，无法合并。你可以输入“r”返回目录选择，或者输入“q”退出当前合并进程:{style_end}")
            if s == 'r':
                file_path = slc_pth(file_path)
            else:
                print(f"{style_head}…………你选择了退出当前合并进程…………{style_end}")
                break


if __name__ == "__main__":

    work_dirname = get_p_f()  #调用自建的y_folder库中的get_this_file_parent_folder获得工作文件夹的路径。

    file_path = slc_pth(work_dirname) #调用自建的y_folder库中的select_folder_path函数来选择

    file_list = os.listdir(file_path)

    merge_excel_file(file_path,file_list)
