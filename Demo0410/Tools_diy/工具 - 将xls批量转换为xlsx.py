# @-*- coding = utf-8 _*_
# @Time : 2021/4/18 15:27
# @Author : 杨昌军
# @File : 将xls批量转换为xlsx.py
# @Software : PyCharm

import win32com.client as win32
import os

from y_folder import get_this_file_parent_folder as get_p_f,select_folder_path as slc_pth

def xls_to_xlsx(path):
    print(f"…………你正在将{path}文件夹中的.xls文件转为.xlsx文件…………")
    list_file = os.listdir(path)
    print(list_file)
    excel_list = []
    for name in list_file:
        if name[-4:] == '.xls':
            excel_list.append(name)
            print(name)
    print(excel_list)
    for excel_name in excel_list:
        file = os.path.join(path,excel_name)
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(file)
            # xlsx: FileFormat=51
            # xls:  FileFormat=56,
            # 后缀名的大小写不通配，需按实际修改：xls，或XLS
        wb.SaveAs(file.replace('xls','xlsx'),FileFormat=51)  # 我这里原文件是大写
        wb.Close()
        excel.Application.Quit()
        print(f"{excel_name}转换完毕！")
    print("…………全部转换结束，请打开原xls文件所在文件夹查看………………")

if __name__ == "__main__":

    current_file_path = get_p_f()

    path = slc_pth(current_file_path)

    xls_to_xlsx(path)


