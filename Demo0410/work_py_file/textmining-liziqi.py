# @-*- coding = utf-8 _*_
# @Time : 2021/4/18 18:03
# @Author : 杨昌军
# @File : textmining-liziqi.py
# @Software : PyCharm

import sys #导入sys模块，以实现在指定地方结束程序。
sys.path.append("..")  #将此文件所在的上级目录添加到工作路径中，以导入自建的模块。
import os #导入os模块以选择文件或文件夹路径。
import pandas as pd #导入pandas模块以读取excel文件。
import numpy as np #导入numpy模块以将excel中的数据转换为列表。
import jieba #导入jieba模块以进行分词。
import jieba.posseg as pseg #导入jieba.posseg模块以实现词性标注。
import jieba.analyse
import re #导入re模块以利用正则表达式进行文本清理。
from collections import Counter  #导入collections模块中的counter动作以进行词频统计。
import textwrap #导入textwrap模块以实现长字符串换行输出。

from a_libs.y_folder import get_this_file_parent_folder as get_pf,select_folder_path as slc_pth,in_or_not_in_file_list as is_ifl #从自建模块里导入。

'''
注意事项：
    1.函数excel_to_list()会返回两个值，第一个是包含导入的excel指定列数据的list列表，第二个是包含导入的excel全部数据的dataframe。
    2.函数clean_text()中可选择是否检查清理后的文本。
    3.函数word_segment_and_pos_tagging()会返回两个值，皆为list列表，第一个既包含词又包含词性，是个pair列表，第二只包含词。
'''

def excel_to_list(excel_file,col_name):  #定义一个函数，将excel中的某一列转化为list列表。
    comments_text_dataframe = pd.read_excel(excel_file, converters={
        'id': str})  # 读取excel_file所指称的文件，并将id列内容转换为字符串格式（此前为数值格式）。此时comments_text_dataframe是个dataframe。
    comment_array = np.array(comments_text_dataframe[
                                 col_name])  # 这里调用一个numpy里的array函数将dataframe里指定列的内容转换为数组。一行一个数据(子元素)，dataframe指定列里有多少行，这个数组就包含多少个数据。
    comment_list = comment_array.tolist()  # 这一步是将用array函数调用的数组通过.tolist()方法转化为列表。此时comments_list为列表，列表中每个元素都是一条字符串形式的评论。
    print(f"\033[5;30;47m…………Excel中指定的{col_name}列的数据已全部导入list列表…………\033[0m")
    return comment_list,comments_text_dataframe  #返回一个包含指定列数据的列表、一个包含导入的excel全部内容的dataframe、指定列的列名。
def filter_sentence(data,filter_word): #定义一个函数，筛选包含指定词语的句子。
    comment_filtered_list = []
    for screen in data:
        screen = str(screen)
        if screen.find(filter_word) != -1:
            comment_filtered_list.append(screen)
    return comment_filtered_list
def save_all_filtered_data_to_excel(data_df,col_name,filter_word,save_filename):  #定义一个函数，将筛选过的数据存入excel。
    if save_filename == '':
        save_filename = (input("请输入你存储筛选过的数据的Excel文件名，不用输入后缀名“.xlsx”：")).strip()
        print(f"你准备将筛选过的数据存入{save_filename}.xlsx文件中，请选择此文件的保存路径。")
        save_path = slc_pth(get_pf()) #选择保存路径。
    data_frame = data_df.loc[data_df[col_name].str.contains(filter_word, na=False)] #在text列中查找有“生活”字符串的数据。
    data_frame.to_excel(f'{save_path}\\{save_filename}.xlsx',index=False)
    print(f'\033[5;30;47m…………筛选后的数据已保存至\033[1;46m{save_path}\033[0m下的“{save_filename}.xlsx”中…………\033[0m')
def clean_text(comments_list,regular_expression): #定义一个函数，进行文本清理。
    if regular_expression == '':
        regular_expression = (input('请输入你要剔除的字符或符号的正则表达式，以“|”隔开：')).strip()
    text_str = ''.join(str(comments_list))  #通过.join方法合并。
    pattern = re.compile(f'{regular_expression}')
    text_str = re.sub(pattern,'',text_str)
    # 选择是否检查清理过的文本。
    judge_whether_inspect_cleaned_text = 'n'  #不检查清理后的文本，设为n，否则设为y。
    if judge_whether_inspect_cleaned_text == 'y': #如果此变量为空。
        judge_whether_inspect_cleaned_text = ((input("文本清理已结束，是否检查清理后的文本，以决定是否修正自己的正则表达式（y/n）:")).strip()).lower()
        if judge_whether_inspect_cleaned_text == 'y':
            inspect_regular = text_str[0:5000]  # 这里是获得comments这个字符串的前10000个字符。
            print(textwrap.fill(inspect_regular, 100))  # 这里是用textwrap库里的.fill方法实现长字符串的换行输出，每行100个字符。
            t = ((input("\033[5;30;47m文本清理结果已展示，是否进行下一步操作（y/n）：\033[0m")).lower())
            if t == 'n':
                sys.exit()
        else:
            print("你相信自己的正则表达式，选择不检查清理后的文本。")
    elif judge_whether_inspect_cleaned_text == 'n':
        print("你相信自己的正则表达式，自动选择不检查清理后的文本。")
    return text_str
def word_segment_and_pos_tagging(new_words, stop_words, text_str):  #定义一个函数，先加载自定义词典，再加载停用词词典，然后对输入的字符串text_str进行分词，最终输出为列表。
    jieba.enable_paddle()  #利用飞桨Paddle深度学习框架，训练序列标注（双向GRU）网络模型实现分词及词性标注。
    jieba.load_userdict(new_words)    #加载自定义词典。
    stopwords = [line.strip() for line in open(stop_words, encoding='UTF-8').readlines()]   #加载停用词词典，并创建一个停用词列表。此时，stopwords是一个列表。
    print("正在利用飞桨paddle模式对文本进行分词和词性标注，需要一定时间，请稍等。")
    seg_and_tagging_all_word_list = pseg.lcut(text_str,use_paddle=True) #分词并标注词性，默认开启飞桨paddle模式下的分词与词性标注功能，因为对比过开与不开的效果，感觉确实开后分词与标注更精确，具体如何还要研究。
    segged_and_tagged_word_pair_list = []  #既包含词又包含词性的列表。
    for tagging_word in seg_and_tagging_all_word_list:
        if tagging_word.word not in stopwords:  #去除停用词，tagging_word.word为取tagging_word这个pair元组里word的值。
            segged_and_tagged_word_pair_list.append(tagging_word)
    segged_word_list = []  #只包含词，不包含词性。
    for seged_and_tagged_word in segged_and_tagged_word_pair_list:
        seged_word = seged_and_tagged_word.word
        segged_word_list.append(seged_word)
    return  segged_and_tagged_word_pair_list,segged_word_list  #segged_and_tagged_word_pair_list是一个既包含词又包含词性的list，segged_word_list仅包含词，不包含词性。
def sort_word_frequency(data):  #此函数用于统计词频并进行排序。返回的是一个排好序的列表。
    word_frequency_dic = dict(Counter(data))  # 用Counter()统计列表word_list中的词频，并转化为字典word_frequency_dic。注意，这里的Counter的首字母必须大写，否则会出错。
    word_frequency_dic_sorted = sorted(word_frequency_dic.items(), key=lambda x: x[1],reverse=True)  # [:100] #这里是先用字典的.items()方法将字典转换为列表，然后用列表的sorted方法对列表中的元素进行排序，后面的都是参数。
    return word_frequency_dic_sorted
def show_the_highest_ranked_word(data): #此函数用于直接显示排序最高的单词，可以不用。
    num = int(input("你想显示前多少个词频最高的单词/词语："))
    for i in range(num):
        word, count = sort_word_frequency(data)[i]
        print("{0:<10}{1:>5}".format(word, count))  #{0:<10}{1:>5}指定变量值的输出格式，其含义为输出第一个（0）变量时，左对齐（<），最小宽度为10，第二个（1）右对齐（>），最小宽度为5。


if __name__ == "__main__":
    #……………………………………必要配置，如需自动完成分析工作，下面必须填写……………………………………
    excel_file = 'E:\\PycharmProjects\\Demo0410\\work_data_liziqi\\liziqi_total_comments.xlsx' #可以直接填写要处理的excel文件的绝对路径。
    col_name = 'text'  #可以直接填写此excel文件中要处理的数据所在的列名。
    filter_word = '生活'  #筛选词
    news_words = 'E:\\PycharmProjects\\Demo0410\\work_data_liziqi\\new_words.txt'    #自定义词典。
    stop_words = 'E:\\PycharmProjects\\Demo0410\\work_data_liziqi\\stop_words.txt'    #停用词词典。
    re_expression = '\n|\[.{1,8}\]|[^\u4e00-\u9fa5]'  #清理文本的正则表达式。一般为“\n|\[.{1,8}\]|[^\u4e00-\u9fa5]”，“\n“表示去除换行符，”\[.{1,8}\]“表示方括号内任意1-8个字符，如[赞][泪目]等,”[^\u4e00-\u9fa5]“表示非中文字符。皆不包括引号。
    #……………………………………必要配置，如需自动完成分析工作，上面必须填写……………………………………

    #……………………………………………………………………开始对数据进行基础性处理……………………………………………………………………
    #0.进程开始。
    print("…………即将开始处理Excle数据。")

    #1.判断是否手动输入文件名和列名。
    if not excel_file:  #如果excel_file变量为空，则通过以下函数和步骤输入要处理的excel文件的绝对路径。
        print("你未指定要处理的excel文件，请通过以下步骤指定。")
        work_dir = get_pf()  #获取工作数据所在的绝对目录
        dir_path = slc_pth(work_dir)  #自主选择数据所在的目录
        file_name = (input("请输入你要进行文本挖掘的Excel文件的名称，不用输入后缀名“.xlsx”：")).strip()  #
        file_name = is_ifl(dir_path,file_name,'.xlsx')
        excel_file = os.path.join(dir_path, file_name)
    else:
        print("…………已指定要处理的Excel文件。")
    if not col_name:  #如果col_name变量为空，则输入列名。
        col_name = (input("请输入要将数据导入list列表，以进行文本挖掘的此excel中某列的列名：")).strip()
    else:
        print("…………已指定此Excel文件中要处理的数据所在的列名。")

    #2.将excel中要处理的数据转换为列表。
    comment_list, data_df = excel_to_list(excel_file, col_name)  #调用一开始定义的excel_to_list函数。注意，此函数会返回两个值，一个是包含导入的excel指定列数据的列表，一个是包含导入的excel全部数据的dataframe，一个是指定列的列名。

    #3.判断是否先对指定列的原始语料进行词频排序，以找出对评论进行筛选的关键词。
    find_key_word_from_original_data = 'n'  #不对原始语料进行词频排序设为n，否则设为y。
    if find_key_word_from_original_data == 'y':
        print(f"…………已自动选择对原始语料指定的{col_name}列的数据进行词频排序，以找出筛选关键词。")
        if not news_words and not stop_words:  #如果事先未指定自定义词典和停用词词典。
            print("你未指定自定义词典和停用词词典，请通过以下步骤指定。")
            work_dir = get_pf()  # 获取工作数据所在的绝对目录
            dir_path = slc_pth(work_dir)  # 自主选择数据所在的目录
            news_words_file = (((input("请输入你要使用的\033[1;33m自定义词典\033[0m名称（不用输入后缀名“.txt”）：")).strip()).lower())+'.txt'
            news_words_file = is_ifl(dir_path,news_words_file,'.txt')   #检查是否输入正确。
            news_words = os.path.join(dir_path,news_words_file)
            stop_words_file = (((input("请输入你要使用的\033[1;33m停用词词典\033[0m名称（不用输入后缀名“.txt”）：")).strip()).lower())+'.txt'
            stop_words_file = is_ifl(dir_path,stop_words_file,'.txt')    #检查是否输入正确。
            stop_words = os.path.join(dir_path,stop_words_file)
        comments = clean_text(comment_list, re_expression)
        _,word_list = word_segment_and_pos_tagging(news_words, stop_words, comments)  #word_segment_and_pos_tagging函数返回两个值，故用下划线表示不接收第一个。
        print(f"已对原始语料指定的{col_name}列的数据进行词频排序。")
        show_the_highest_ranked_word(word_list)
        print("     \033[5;30;47m…………已对原始语料进行词频排序，如要进行评论筛选，可输入上面某一个关键词…………\033[0m")
    elif find_key_word_from_original_data == 'n':
        print(f"…………已自动选择不对原始语料指定的{col_name}列的数据进行词频排序。")

    #4.判断是否对导入的Excel指定列的数据进行筛选。
    whether_filter_from_original_data = 'y'  #对原始数据进行筛选设为y，否则设为n。
    if whether_filter_from_original_data == 'y':
        print(f"…………已自动选择对原始语料按指定关键词进行筛选。")
        if not filter_word:
             filter_word = str((input("你还未指定筛选关键词，请输入：")).strip())
        comment_filtered_list = filter_sentence(comment_list,filter_word)  # 注意，这里返回了两个值，后一个filter_word其实只是其里面的函数filter_sentence的filter_word（筛选关键词）的传递。
        print(f'共{len(comment_list)}条评论，根据关键词“{filter_word}”筛选出{len(comment_filtered_list)}条评论。')
    elif whether_filter_from_original_data == 'n':
        print(f"…………已自动选择不对原始语料按特定关键词进行筛选。")

    #5.判断是否保存筛选后的数据。
    save_filtered_data = 'n'  #不保存筛选后的数据设为n，否则设为y。
    save_filtered_data_filename = ''
    if save_filtered_data == 'y':
        print(f"…………已自动选择对筛选后的数据进行保存。")
        save_all_filtered_data_to_excel(data_df,col_name,filter_word,save_filtered_data_filename)
    elif save_filtered_data == 'n':
        print(f"…………已自动选择不保存筛选后的数据。")

    #6.判断是否进行分词及进行词性标注。
    whether_seg_sentence = 'y' #进行分词及词性标注设为y，否则设为n。
    if whether_seg_sentence == 'y':
        print("你自动选择了对要处理的文本进行分词与词性标注。")
        cleaned_txt = clean_text(comment_filtered_list,re_expression)
        segged_and_tagged_word_pair_list,segged_word_list = word_segment_and_pos_tagging(news_words, stop_words, cleaned_txt)
        print("分词与词性标注完成。")
    elif whether_seg_sentence == 'n':
        print("你自动选择了不对要处理的文本进行分词与词性标，不分词将无法进行其它操作，程序结束。")
        sys.exit()
    #……………………………………………………………………数据基础性处理结束……………………………………………………………………

    #…………………………………………………………………对数据进行功能性应用…………………………………………………………………
    select_operate_option = 'y'  #进行更多操作，这里设为y，否则设为n，设为n将直接结束程序。
    if select_operate_option == 'y':
        select_operate_option = (input("已分词并标注词性完毕，你现在可以进行以下操作：\n\t1.按指定数量检查词频最高的词。\n\t2.创建词云。\n\t3.进行情感分析。\n\t4.直接结束程序。\n请选择你的操作，直接输入序号即可：")).strip()
        if select_operate_option == '1':
            print(f'你选择了{select_operate_option}，正在对词频进行排序…………')
            show_the_highest_ranked_word(segged_word_list)
        elif select_operate_option == '2':
            print(f'你选择了{select_operate_option}，但很抱歉，此功能仍在开发中，将结束程序。')
        elif select_operate_option == '3':
            print(f'你选择了{select_operate_option}，但很抱歉，此功能仍在开发中，将结束程序。')
        elif select_operate_option == '4':
            print(f'…………你选择了直接结束程序，程序结束…………')
            sys.exit()
        else:
            print(f'…………你未在以上选项中进行选择，直接结束程序…………')
            sys.exit()
        print(f'…………全部操作执行完毕，程序结束…………')
    elif select_operate_option == 'n':
        print(f'…………你自动选择了结束程序，程序结束…………')
        sys.exit()



