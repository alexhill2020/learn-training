# @-*- coding = utf-8 _*_
# @Time : 2021/4/17 15:28
# @Author : 杨昌军
# @File : 合并excel文件.py
# @Software : PyCharm

import os

def get_this_file_parent_folder(): #此函数是从此文件所在的文件夹返回工作文件夹。
    style_head = '\033[5;30;47m'  #设置提示信息显示格式。
    style_end = '\033[0m' #设置提示信息显示格式。
    parent_dirname = os.path.abspath('..')  #获得此文件所在父目录的绝对路径。
    (filepath,dirname) =os.path.split(parent_dirname)  #将父目录的绝对路径分割成基础路径和父目录的目录名。
    print(f"{style_head}此.py文件的上级目录{dirname}中有以下工作文件夹，你可以选择进入其中一个。{style_end}")
    list = os.listdir(parent_dirname)  #在父目录中查找所有文件和文件夹，并形成列表。
    list_display = []
    for name in list:
        if '.' not in name:
            list_dir = ['venv','a_tools_diy','a__learn_python','a_libs','a__py文件备份','work_py_file',]
            if name not in list_dir:
            #if name != 'venv' and name != 'y__tools_diy' and name != 'y___learn_python' and name != 'y__libs' and name != :
                print('     '+str(name))  #逐行打印父目录中的文件和文件夹名称。
                list_display.append(name)
    current_dirname = input(f'{style_head}请输入你要进入的文件夹的名称：{style_end}')
    while True:
        if current_dirname not in list_display:
            current_dirname = input(f"\033[1;31m你输入的文件夹名称不在以上列表中，请仔细检查后重新输入：\033[0m{style_end}")
        else:
            break
    work_dirname = os.path.join(parent_dirname,current_dirname)
    return work_dirname

def select_folder_path(path):  #此函数是选择文件夹路径。

    style_head = '\033[5;30;47m'  #
    style_end = '\033[0m'

    def in_or_not_in(input_vale, list):
        while True:
            if input_vale not in list:
                input_vale = input(f"\033[1;31m你输入的不在列表中，请仔细检查后重新输入：\033[0m")
            else:
                break
        return input_vale
    def select_operate(s,path,list_folder,list_file):
        if s == 'p':
            (filepath, dirname) = os.path.split(path)
            path = filepath
        elif s == 's':
            if list_folder:
                print(f"{style_head}当前目录的子文件夹为：{style_end}")
                for name1 in list_folder:
                    print("     " + name1)
                s1 = input(f"{style_head}输入“***”重新选择操作，或者输入你要进入的子文件夹（区分大小写，请自己检查）：{style_end}")
                if s1 == '***':
                    pass
                else:
                    s1 = in_or_not_in(s1,list_folder)
                    path = os.path.join(path,s1)
            else:
                print(f"\033[1;33m当前目录没有子文件夹，请重新输入。\033[0m")
        elif s == '*list':
            if list_file:
                print(f"{style_head}当前目录下的文件为：{style_end}")
                for name1 in list_file:
                    print("     " + name1)
                s1 = input(f"{style_head}文件展示完毕，输入“***”可重新选择操作：{style_end}")
                s1 = (s1.strip()).lower()
                while True:
                    if s1 == '***':
                        break
                    else:
                        s1 = input(f"\033[1;31m你的输入有误，请重新输入：\033[0m")
                        s1 = (s1.strip()).lower()

            else:
                print(f"\033[1;33m当前目录没有文件，请重新输入。\033[0m")
        return path
    def assess_input(s):
        while s != 'p' and s != 's' and s != '*list' and s != 'n':
            s = input("\033[1;31m你的输入有误，只能输入英文字符“p”、“s”、“*list”、“n”，请重新输入：\033[0m")
            if s == 'p' or  s == 's' or s == '*list' or s == 'n':
                break
        return s
    def is_not_hidden_folder(path):
        import win32file, win32con
        file_attr = win32file.GetFileAttributes(path)
        if file_attr & win32con.FILE_ATTRIBUTE_HIDDEN:
            return False
        return True

    try:
        while os.path.isdir(path):
            (filepath, dirname) = os.path.split(path)
            list = os.listdir(path)

            list_folder = []  #当前文件夹下的子文件夹列表。
            for name in list:
                path1 = os.path.join(path,name)
                if os.path.isdir(path1):
                    if is_not_hidden_folder(path1):
                        list_folder.append(name)

            list_file = [] #list_file为dirname目录下全部文件的列表。
            for name_file in list:
                path2 = os.path.join(path,name_file)
                if os.path.isfile(path2):
                    if is_not_hidden_folder(path2):
                        list_file.append(name_file)

            if len(path) == 3:
                if (list_folder and list_file):
                    s1 = input(f"你当前已在\033[1;46m{path[0]}盘（{path}）\033[0m根目录下，不能返回上级目录。此根目录下共拥有\033[1;33m{len(list_folder)}个子目录\033[0m和\033[1;33m{len(list_file)}个文件\033[0m。\n{style_head}进入其它盘请输入“*disc”，进入文件夹输入“s”，列出当前根目录下所有文件输入“*list”，不进行任何操作输入“n”:{style_end}")
                elif (list_folder and not list_file):
                    s1 = input(f"你当前已在\033[1;46m{path[0]}盘（{path}）\033[0m根目录下，不能返回上级目录。此根目录下共拥有\033[1;33m{len(list_folder)}个子目录\033[0m，\033[1;33m没有文件\033[0m。\n{style_head}进入其它盘请输入“*disc”，进入文件夹输入“s”，不进行任何操作输入“n”:{style_end}")
                elif (list_file and not list_folder):
                    s1 = input(f"你当前已在\033[1;46m{path[0]}盘（{path}）\033[0m根目录下，不能返回上级目录。此根目录下共拥有\033[1;33m{len(list_file)}个文件\033[0m。\n{style_head}进入其它盘请输入“*disc”，列出当前根目录下所有文件输入“*list”，不进行任何操作输入“n”:{style_end}")
                else:
                    s1 = input(f"你当前已在\033[1;46m{path[0]}盘（{path}）\033[0m根目录下，不能返回上级目录。此根目录下\033[1;33m没有子目录\033[0m，\033[1;33m没有文件\033[0m。\n{style_head}进入其它盘请输入“*disc”，不进行任何操作输入“n”:{style_end}")
                s1 = (s1.strip()).lower()
                while s1.lower() != '*disc' and s1.lower() != 's' and s1.lower() != '*list' and s1.lower() != 'n':
                    s1 = input("\033[1;31m你的输入有误，只能输入英文字符“*disc”、“s”、“*list”、“n”，请重新输入：\033[0m")
                    if s1.lower() == '*disc' or s1.lower() == 's' or s1.lower() == '*list' or s1.lower() == 'n':
                        break
                if s1 == '*disc':
                    s2 = (input(f"{style_head}请输入你要进入的磁盘名称（C/D/E/……），不用输入“:\”符号：{style_end}")).upper()
                    path = s2+':\\'
                    while True:
                        try:
                            os.listdir(path)
                            break
                        except FileNotFoundError:
                            s2 = (input(f"\033[1;46m{s2.upper()}盘（{path}）\033[0m\033[1;31m不存在，请重新输入：\033[0m")).upper()
                            path = s2 + ':\\'
                elif s1 == 's':
                    if list_folder:
                        print(f"{style_head}当前磁盘的文件夹为：{style_end}")
                        for name1 in list_folder:
                            print("     " + name1)
                        s3 = input(f"{style_head}输入“***”重新选择操作，或者输入你要进入的文件夹（区分大小写，请自己检查）：{style_end}")
                        if s3 == '***':
                            pass
                        else:
                            s3 = in_or_not_in(s3, list_folder)
                            path = os.path.join(path, s3)
                    else:
                        print(f"\033[1;33m当前磁盘没有子文件夹，请重新输入。\033[0m")
                elif s1 == '*list':
                    if list_file:
                        print(f"{style_head}当前{style_end}\033[1;46m{path[0]}盘（{path}）\033[0m{style_head}根目录下的文件为：{style_end}")
                        for name1 in list_file:
                            print("     " + name1)
                        s1 = input(f"{style_head}文件展示完毕，输入“***”可重新选择操作：{style_end}")
                        s1 = (s1.strip()).lower()
                        while True:
                            if s1 == '***':
                                break
                            else:
                                s1 = input(f"\033[1;31m你的输入有误，请重新输入：\033[0m")
                                s1 = (s1.strip()).lower()

                    else:
                        print(f"\033[1;33m当前目录没有文件，请重新输入。\033[0m")

                elif s1 == 'n':
                    print(f"{style_head}…………你选择不进入其它盘，将执行下一步骤…………{style_end}")
                    break
            else:
                if (list_folder and list_file):
                    s = input(f"你当前文件夹的绝对路径为\033[1;46m{path}\033[0m，共拥有\033[1;33m{len(list_folder)}个子目录\033[0m和\033[1;33m{len(list_file)}个文件\033[0m。\n{style_head}返回上级目录输入“p”，进入下级目录输入“s”，列出当前目录下所有文件输入“*list”，不进行任何操作输入“n”:{style_end}")
                elif (list_folder and not list_file):
                    s = input(f"你当前文件夹的绝对路径为\033[1;46m{path}\033[0m，共拥有\033[1;33m{len(list_folder)}个子目录\033[0m，\033[1;33m没有文件\033[0m。\n{style_head}返回上级目录输入“p”，进入下级目录输入“s”，不进行任何操作输入“n”:{style_end}")
                elif (list_file and not list_folder):
                    s = input(f"你当前文件夹的绝对路径为\033[1;46m{path}\033[0m，\033[1;33m没有子目录\033[0m，共拥有\033[1;33m{len(list_file)}个文件\033[0m。\n{style_head}返回上级目录输入“p”，列出当前目录下所有文件输入“*list”，不进行任何操作输入“n”:{style_end}")
                else:
                    s = input(f"你当前文件夹的绝对路径为\033[1;46m{path}\033[0m，\033[1;33m没有子目录\033[0m，\033[1;33m没有文件\033[0m。\n{style_head}返回上级目录输入“p”，不进行任何操作输入“n”:{style_end}")
                s = (s.strip()).lower()  #将输入的值去空格，并全部转为小写。
                s = assess_input(s)  #这个函数限定了只能输入字符p，s，*list，n。
                path = select_operate(s,path,list_folder,list_file)  #这个函数是要根据选择实行某种特定操作。
                if s.lower() == 'n':
                    print(f"{style_head}…………你选择不进行任何操作，将执行下一步骤…………{style_end}")
                    break
    except TypeError:
        print("你输入的是文件路径，而不是文件夹路径。")
    return path