# @-*- coding = utf-8 _*_
# @Time : 2021/4/18 18:03
# @Author : 杨昌军
# @File : liziqi_评论文本挖掘.py
# @Software : PyCharm

import sys #导入sys模块，以实现在指定地方结束程序。
import pandas as pd #导入pandas库以读取excel文件。
import numpy as np #导入numpy库以将excel中的数据转换为列表。
import jieba #导入jieba库以进行分词。
import re #导入re库以利用正则表达式进行文本清理。
from collections import Counter  #导入collections中的counter库以进行词频统计。
import textwrap #导入textwrap库以实现长字符串换行输出。

'''
注意事项：
    1.函数data_sources()中可选择是否自动导入数据。
    2.函数excel_to_list()中可选择是否自动输入列名。同时此函数会返回两个值，一个是包含导入的excel指定列数据的list列表，一个是包含导入的excel全部数据的dataframe。
    3.函数judge_whether_sort_word_frequency_for_original_corpus()中可选择是否先对原始语料进行排序
    4.函数judge_whether_filter()中可选择是否筛选数据。
    5.函数judge_whether_save_filtered_all_data()中可选择是否保存筛选后的数据。
    6.函数save_all_filtered_data_to_excel()中可选择是否自动输入保存筛选后数据的文件名。
    7.函数judge_whether_seg_sentence()中可设置是否自动选择进行分词及下一步操作。
    8.函数filter_sentence()中可选择是否自动输入筛选词。
    9.函数text_clean()中可选择是否输入正则表达式。
    10.函数judge_whether_inspect_cleaned_text()中可选择是否检查清理后的文本。
'''

def data_sources():
    excel_file = 'liziqi_total_comments.xlsx'  #如要手动输入文件名，请将这里设为空，否则请直接填文件名。
    if excel_file == '':
        excel_file = (input("\033[1;33m注意：要在python中处理excel数据，首先应将excel里要处理的数据转换为list列表。\n     要转换的excel文件后缀名必须为.xlsx，后缀名不用输入，且要转换的excel必须有表头，否则会出错。\033[0m\n请输入要转换的excel文件名：")).strip() + '.xlsx'
    else:
        print("\033[5;30;47m…………你选择了自动导入Excel数据…………\033[0m")
    return excel_file
def excel_to_list(excel_file):  #定义一个函数，将excel中的某一列转化为list列表。注意，第二个参数必须为数字，是列数。
    col_name = 'text' #不自动输入要进行数据文本挖掘的列的列名，这里就设为空，否则请输入列名。
    if col_name == '':
        col_name = (input("请输入要将数据导入list列表，以进行文本挖掘的此excel中某列的列名：")).strip()
    else:
        print(f'\033[5;30;47m…………已自动输入要进行数据文本挖掘的列名”{col_name}“…………\033[0m')
    comments_text_dataframe = pd.read_excel(excel_file,converters={'id':str})  #读取excel_file所指称的文件，并将此文件第二列的数据存入comments_text变量。此时comments_text是个dataframe。
    comment_array = np.array(comments_text_dataframe[col_name])  #这一步和下一步是把pandas里的数据转换为列表，这里是先调用一个numpy里的array函数将dataframe里指定列的数转为数组。一行一个数据(子元素)。此时comment_array的类型为数组，dataframe指定列里有多少行，这个数组就包含多少个数据。
    comment_list = comment_array.tolist()  #这一步是将用array函数调用的数组通过.tolist()方法转化为列表。此时comments_list为列表，列表中每个元素都是一条字符串形式的评论。
    print(f"\033[5;30;47m…………Excel中{col_name}列的数据已全部导入list列表…………\033[0m")
    return comment_list,comments_text_dataframe,col_name  #返回一个包含指定列数据的列表、一个包含导入的excel全部内容的dataframe、指定列的列名。
def judge_whether_sort_word_frequency_for_original_corpus(data):  #定义一个函数，判断是否先对原始语料进行排序。
    a = 'n'  #如果不先对原始语料进行排序，这里设为空，否则设为n。
    if a == '':
        a = (input("是否要对未筛选过的原始语料进行词频排序，以找出对评论进行筛选的关键词（y/n）:")).lower()
        if a == 'y':
            print("     \033[5;30;47m……你选择了先对原始语料进行词频排序，正在对原始语料进行清理……\033[0m")
            comments = text_clean(data)
            print("     \033[5;30;47m……清理完成，正在对原始语料进行分词……\033[0m")
            word_list = seg_sentence("new_words.txt", "stop_words.txt", comments)
            print("     \033[5;30;47m……分词完成，正在对原始语料进行词频排序……\033[0m")
            show_the_highest_ranked_word(word_list)
            print("     \033[5;30;47m…………已对原始语料进行词频排序，如要进行评论筛选，可输入上面某一个关键词…………\033[0m")
        else:
            print("\033[5;30;47m…………你选择不对原始语料进行词频排序，如要进行评论筛选，可直接输入一个词…………\033[0m")
    else:
        print("\033[5;30;47m…………你自动选择了不先对原始语料进行词频排序，如要进行评论筛选，可直接输入一个词…………\033[0m")
def filter_sentence(data): #定义一个函数，筛选包含指定词语的句子。
    filter_word = '生活' #不自动输入筛选词，就将这里设为空，否则请输入要筛选的词。
    if filter_word == '':
        filter_word = input("你想筛选出的评论应包含何词？请输入：")
    else:
        print(f"\033[5;30;47m…………你自动输入了筛选词“{filter_word}”，筛选正在进行中…………\033[0m")
    comment_filtered_list = []
    for screen in data:
        screen = str(screen)
        if screen.find(filter_word) != -1:
            comment_filtered_list.append(screen)
    return comment_filtered_list,filter_word
def judge_whether_filter(option): #定义一个函数，判断是否对所有数据进行筛选。
    a = 'y'   #不自动进行筛选，就将这里设为空，否则请输入y。
    if a == '':
        a = (input("\033[5;30;47m是否根据某一关键词对原始语料进行筛选（y/n）：\033[0m")).lower()
    else:
        print("\033[5;30;47m…………你自动选择了对评论进行筛选…………\033[0m")
    if a == 'y':
        comment_filtered_list,filter_word = filter_sentence(option)  #调用一开始定义的screen_sentence函数，按指定的词对评论进行筛选，并输出为列表。
            # 注意，screen_sentence()这个函数返回了两个值，外层judge_whether_filter这个函数里其实只用了前一个comment_filtered_list，后一个filter_word原样返回，以做他用。相当于filter_word只是经过这个函数进行了传输，值不变。
        print(f'共{len(option)}条评论，根据输入词筛选出{len(comment_filtered_list)}条评论。')
        option = comment_filtered_list
    else:
        print(f"你未对评论进行筛选，将对全部{len(option)}条评论进行文本清理。\n\033[5;30;47m…………正在对所有评论进行文本清理…………\033[0m")
    return option,filter_word
def save_all_filtered_data_to_excel(word,col_name):  #定义一个函数，将筛选过的数据存入excel。
    filename = 'liziqi_生活_comments'  #如果不自动输入想保存的文件名，就将这里设为空，否则请填写文件名。
    if filename == '':
        filename = input("请输入你存储筛选过的数据的Excel文件名，不用输入后缀名“.xlsx”：")
    data_frame = df.loc[df[col_name].str.contains(word,na=False)] #在text列中查找有“生活”字符串的数据。
    data_frame.to_excel(f'{filename}.xlsx',index=False)
    print(f'\033[5;30;47m…………筛选后的数据已保存至“{filename}.xlsx”中…………\033[0m')
def judge_whether_save_filtered_all_data(word,col_name):
    c = 'y' #不自动选择对筛选后的数据进行保存，就将这里设为空，否则设为y。
    if c == '':
        c = (input(f'\033[5;30;47m评论筛选完毕，是否要保存筛选后的数据（y/n）:\033[0m')).lower()
        if c =='y':
            save_all_filtered_data_to_excel(word,col_name)
            print('\033[5;30;47m…………筛选后的数据保存完毕，正在对指定列的数据进行文本清理…………\033[0m')
        else:
            print('\033[5;30;47m…………你选择不保存筛选后的数据，正在对指定列的数据进行文本清理…………\033[0m')
    else:
        print('\033[5;30;47m…………你自动选择了对筛选后的数据进行保存…………\033[0m')
        save_all_filtered_data_to_excel(word,col_name)
def judge_whether_seg_sentence(data):
    print('\033[5;30;47m…………筛选后的数据保存完毕，你可以选择是否进行更多操作…………\033[0m')
    d = 'y'  #如果不自动选择进行分词，则将这里设为空，否则设为y。
    if d == '':
        operation_item_selected = (
            input("你现在有几种操作可以选择：\n\t1.进行分词，以备进一步的文本挖掘。\n\t2.不再进行其它操作，直接结束程序。\n请选择你的操作，直接输入序号即可：")).strip()
        if operation_item_selected == '1':
            #对是否筛选进行判断并处理完成后将指定列的列表数据合并为一个字符串，并利用正则表达式进行文本清理。
            print("\033[5;30;47m…………你选择了进行分词，正在进行文本清理…………\033[0m")
            comments = text_clean(data) #这里先调用一个开始定义的judge_whether_filter函数判断是否进行数据筛选，再调用text_clean函数对已筛选或未筛选的列表数据进行文本清理。
            #选择是否检查清理过的文本。
            judge_whether_inspect_cleaned_text(comments)  #调用一开始定义的函数judge_whether_inspect选择是否检查清理后的文本。
            #对清理后的文本进行分词。
            word_list = seg_sentence("new_words.txt","stop_words.txt",comments)  #调用之前定义的seg_sentence函数对清理后的字符串进行分词，输出为一个列表。
            print("\033[5;30;47m…………分词完毕…………\033[0m")
        elif operation_item_selected == '2':
            print("\033[5;30;47m…………你选择不进行分词，直接结束程序…………\033[0m")
            sys.exit()
    else:
        print("\033[5;30;47m…………你自动选择了进行分词，正在进行文本清理…………\033[0m")
        comments = text_clean(data)
        judge_whether_inspect_cleaned_text(comments)
        word_list = seg_sentence("new_words.txt", "stop_words.txt", comments)
        print("\033[5;30;47m…………分词完毕…………\033[0m")
    return word_list
def text_clean(text): #定义一个函数，进行文本清理。
    regular_expression = '\n|\[.{1,8}\]|[^\u4e00-\u9fa5]'  #\n|\[.{1,8}\]|[^\u4e00-\u9fa5]  不自动输入正则表达式，将这里设为空。
    if regular_expression == '':
        regular_expression = (input('请输入你要剔除的字符或符号的正则表达式，以“|”隔开：')).strip()
    else:
        print(f"\033[5;30;47m…………你自动输入了需剔除的字符或符号的正则表达式，清理正在进行中…………\033[0m")
    text_str = ''.join(text)  #通过.join方法合并。
    pattern = re.compile(f'{regular_expression}')  #正则表达式"\n"表示去除换行符，"\[.{1,8}\]"表示方括号内任意1-8个字符，如[赞][泪目]等,"[^\u4e00-\u9fa5]"表示非中文字符。皆不包括引号。
    text_str = re.sub(pattern,'',text_str)
    return text_str
def judge_whether_inspect_cleaned_text(option):
    s = 'n' #不检查清理后的文本，就将这里设为空，否则设为n。
    if s == '':
        s = (input("\033[5;30;47m文本已清理完毕，是否检查（y/n）：\033[0m")).lower()
        if s == 'y':
            inspect_regular = option[0:5000]  #这里是获得comments这个字符串的前10000个字符。
            print(textwrap.fill(inspect_regular, 100))   #这里是用textwrap库里的.fill方法实现长字符串的换行输出，每行100个字符。
            t = (input("\033[5;30;47m文本清理结果已展示，是否进行下一步操作（y/n）：\033[0m")).lower()
            if t == 'n':
                sys.exit()
        else:
            print("\033[5;30;47m…………已进行文本清理，正在进行分词…………\033[0m")
    else:
        print(f"\033[5;30;47m…………你自动选择了不检查清理后的文本…………\033[0m")
def seg_sentence(new_words_file,stop_words_file,data):  #定义一个函数，先加载自定义词典，再加载停用词词典，然后对输入的字符串sentence进行分词，最终输出的是一个列表。
    jieba.load_userdict(new_words_file)    #加载自定义词典。
    stopwords = [line.strip() for line in open(stop_words_file, encoding='UTF-8').readlines()]   #加载停用词词典，并创建一个停用词列表。此时，stopwords是一个列表。
    sentence_seged = jieba.cut(data.strip(),cut_all=False,HMM=True)  #jieba.cut生成一个生成器，generator，也就是可以通过for循环来取里面的每一个词。jieba.lcut 直接生成的就是一个list。参数cut_all=False指分词模式为精确，HMM为开启隐马尔科夫链，用于发现未登录的新词。
    word_list = []  #先设置一个空字符串，以用来存储下面过词的字符串。
    for word in sentence_seged:   #从分完词的sentence_seged中取出一个词
        if word not in stopwords: #如果取出的这个词不在停用词列表中
            if word != '\t':  #如果取出的词不是缩进符
                word_list.append(word)  #就把这个词加入字符串outstr
    return word_list   #此时，返回的是一个列表。
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

    #导入文件以进行处理。
    excel_file = data_sources()

    #将excel中要处理的数据转换为列表。
    comment_list,df,col_name = excel_to_list(excel_file)  #调用一开始定义的excel_to_list函数。注意，此函数会返回两个值，一个是包含导入的excel指定列数据的列表，一个是包含导入的excel全部数据的dataframe，一个是指定列的列名。

    #判断是否先对指定列的原始语料进行词频排序，以找出对评论进行筛选的关键词。
    judge_whether_sort_word_frequency_for_original_corpus(comment_list)  #定义一个函数，判断是否先对原始语料进行排序。

    #判断是否对导入的Excel指定列的数据进行筛选，判断并处理完成后将列表数据合并为一个字符串，并利用正则表达式进行文本清理。
    comment_filtered_list,filter_word = judge_whether_filter(comment_list)  #注意，这里返回了两个值，后一个filter_word其实只是其里面的函数filter_sentence的filter_word（筛选关键词）的传递。

    #判断是否保存筛选后的数据。
    judge_whether_save_filtered_all_data(filter_word,col_name)

    #判断是否进行分词。
    word_list = judge_whether_seg_sentence(comment_filtered_list)

    e = 'y'  #如果不自动结束程序，就将这里设置为空，否则设置为y。
    if e == '':
        operation_item_selected = (input("已分词完毕，你现在可以进行以下操作：\n\t1.按指定数量检查词频最高的词。\n\t2.创建词云。\n\t3.进行情感分析。\n\t4.直接结束程序。\n请选择你的操作，直接输入序号即可：")).strip()
        if operation_item_selected == '1':
            print(f'\033[5;30;47m…………你选择了{operation_item_selected}，正在对词频进行排序…………\033[0m')
            show_the_highest_ranked_word(word_list)
        elif operation_item_selected == '2':
            print(f'你选择了{operation_item_selected}，但很抱歉，此功能仍在开发中，将结束程序。')
        elif operation_item_selected == '3':
            print(f'你选择了{operation_item_selected}，但很抱歉，此功能仍在开发中，将结束程序。')
        elif operation_item_selected == '4':
            print(f'\033[5;30;47m…………你选择了直接结束程序，程序结束…………\033[0m')
            sys.exit()
        else:
            print(f'\033[5;30;47m…………你未在以上选项中进行选择，直接结束程序…………\033[0m')
            sys.exit()
        print(f'\033[5;30;47m…………全部操作执行完毕，程序结束…………\033[0m')
    else:
        print(f'\033[5;30;47m…………你自动选择了结束程序，程序结束…………\033[0m')
        sys.exit()



