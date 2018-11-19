'''
对各个法院的诉讼结果文档数目分析
'''
import csv
from collections import Counter
import os
from pyecharts import Bar,Pie,Line

def get_charts(x,y,label,type1):
    if type1 == 1:
        c = Pie("Pie")
    elif type1 == 2:
        c = Bar("Bar")
    elif type1 == 3:
        c = Line("各个法院的诉讼结果文档数目分析")
    c.add(label,x,y,is_more_utils=True)
    c.show_config()
    c.render("court_analysis_line.html")
    os.system("start firefox court_analysis_line.html")


def extract_data_save_to_txt():
    with open('legal_datas2.csv','r',encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader)
        column = [row['\ufeffcourt'] for row in reader]

        print(type(column))

        print(column)
        result = Counter(column)
        print(result)
        d = sorted(result.items(), key=lambda k: k[0])
        list1 = []
        list2 = []
        for each in d:
            list1.append(each[0])
            list2.append(each[1])
        get_charts(list1, list2, '诉讼结果文档', 3)
        print(d)
extract_data_save_to_txt()