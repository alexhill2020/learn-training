# @-*- coding = utf-8 _*_
# @Time : 2021/4/14 13:01
# @Author : 杨昌军
# @File : 西瓜视频李子柒爬虫.py
# @Software : PyCharm
import requests
import json
import xlwt

'''
注意事项：
    1.此代码能成功运行。
    2.此代码主要功能为取西瓜视频web网页上李子柒全部视频的一级和二级评论。
'''

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75'
    }  # 这里是构造一个请求头

#---------------------取一级评论的id、文本、用户名、点赞数等数据-----------------------------------------
    url = 'https://www.ixigua.com/tlb/comment/article/v5/tab_comments/?'
    id_list = []
    text_list = []
    name_list = []
    count_list = []

    main_id = int(input('请输入要爬取的视频页面id:'))

    for offset in range(0,1000):
        offset = offset*10

        param = {
             'tab_index': '0',
             'count': '10',
             'offset': offset,
             'group_id': main_id,
             'item_id': main_id,
             'aid': '1768',
         }

        reponse = requests.get(url=url,params=param,headers=headers)  #通过get方式请求网页，并返回响应对象给reponse
        list_data = reponse.json()  #将返回结果是json格式的内容存入list_data变量，以备后面利用
        #print(list_data)
        guodu = list_data['data'] #此时，guodu为一个列表。
        for guodu_dic in guodu: #此时，guodu_dic为一个字典。
            guodu_dic_list = guodu_dic['comment'] #此时，guodu_dic_list为一个字典。
            id_list.append(guodu_dic_list['id'])
            text_list.append(guodu_dic_list['text'])
            name_list.append(guodu_dic_list['user_name'])
            count_list.append(guodu_dic_list['digg_count'])


        #for dic in list_data['data']: #在取回的json内容中遍历其内容中包含的data列表
         #   id_list.append(dic['id']) #将data列表中每一个id键的值取回来，并添加到id_list列表中
            #text_list.append(dic['text'])

    #with open('N_a.txt', 'w', encoding='utf-8') as p:  # 这里及下面的循环是把列表id_list1中的数据分行写入txt文件中。
     #   for i in text_list:
      #      p.write(i.strip(''))
       #     p.write('\n')

    #print(id_list)
    #print(text_list)
        #上面要注意，什么放到循环中，什么不放到循环中。
        #这上面运行正确，取的是一级评论的ID，并加入列表id_list中

#---------------------------下面为将一级评论保存进excel中---------------------------------------------------

    # id2 = id1[0] #此时，id2是一个字典。  在第32次时报错，因为第32条一级评论没有二级评论，所以取回了0项值。第32条评论的id是6948442261491679264，文本是“奶奶头顶戴着一束花，笑得像个孩子一样！能够看到老人家这样会心的笑容，心都温暖了起来！”
    # 那这里还要加个判断。不加判断的话肯定会报错，因为没有值，所以无法取回，显示“list index out of range”。
    filename = xlwt.Workbook()  # 创建一个excel表格存入变量filename中。
    sheet1 = filename.add_sheet('sheet1')  # 给filename这个表格增加一个名为sheet1的表，并存入sheet1变量中。

    i = 0  # 给i赋予初始变量0。
    for name in name_list:  # 遍历name_list1表格并存入变量name中。
        sheet1.write(i, 0, str(name))  # 将name的值写入表格sheet1的第i行（此时等于初始值0），第0列中。循环第二次的时候即写入表格sheet1的第1列第0行中，依次类推。
        i = i + 1  # 循环一次，i的值加1。

    i = 0
    for text in text_list:
        sheet1.write(i, 1, str(text))
        i = i + 1

    # for i in range(len(count_list1)):
    i = 0
    for count in count_list:
        sheet1.write(i, 2, str(count))
        i = i + 1

    filename.save(str(main_id)+'.一级评论.'+str(len(text_list))+'.xlsx')  # 将所创建和写入数据的表格存为test.xls文档。

    print('一级评论写入成功！')

#-------------------下面为取二级评论的文本、用户、点赞数等数据---------------------------------------------

    text_list1 = []
    name_list1 = []
    count_list1 = []
    for id in id_list: #遍历id_list列表，并将值循环赋予变量id。
        url1 = 'https://www.ixigua.com/tlb/comment/2/comment/v5/reply_list/?'
        for offset in range(0,40):
            offset = offset*10
            param = {
                'count': '10',
                'offset': offset,
                'aid': '1768',
                'id': id
            }
            reponse = requests.get(url=url1, params=param, headers=headers)
            dic_data1 = reponse.json() #将取回的值存入变量dic_data1中，注意，这里存的是字典，不是列表，可以打印出来检查一下。
            guodu1 = dic_data1['data']
            id1 = guodu1['data'] #此时，id1是一个内嵌字典的列表。
            if len(id1) != 0:
                for content in id1: #此时，id2是一个字典。
                    text_list1.append(content['text'])
                    count_list1.append(content['digg_count'])
                    id2 = content['user']
                    name_list1.append(id2['name'])

#----------------------下面为将二级评论的数据保存在excel中-------------------------------------

    filename = xlwt.Workbook() #创建一个excel表格存入变量filename中。
    sheet1 = filename.add_sheet('sheet1')  #给filename这个表格增加一个名为sheet1的表，并存入sheet1变量中。

    i = 0 #给i赋予初始变量0。
    for name in name_list1:  #遍历name_list1表格并存入变量name中。
        sheet1.write(i,0,str(name)) #将name的值写入表格sheet1的第i行（此时等于初始值0），第0列中。循环第二次的时候即写入表格sheet1的第1列第0行中，依次类推。
        i = i+1 #循环一次，i的值加1。

    i = 0
    for text in text_list1:
        sheet1.write(i,1,str(text))
        i = i+1

    #for i in range(len(count_list1)):
    i = 0
    for count in count_list1:
        sheet1.write(i,2,str(count))
        i = i+1

    filename.save(str(main_id)+'.二级评论.'+str(len(text_list1))+'.xlsx') #将所创建和写入数据的表格存为test.xls文档。


    #with open('N_a.txt', 'a',encoding='utf-8') as q:   #这里及下面的循环是把列表id_list1中的数据分行写入txt文件中。
     #   for i in text_list1:
      #      q.write(i.strip(''))
       #     q.write('\n')

    print('二级评论写入成功!!!')


    





