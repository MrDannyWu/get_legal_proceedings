'''
名字或者公司名分析
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
        c = Line("Line")
    c.add(label,x,y,is_more_utils=True)
    c.show_config()
    c.render("name_analysis_line.html")
    os.system("start name_analysis_line.html")


def extract_data_save_to_txt():
    with open('name_no_and.txt','r',encoding='UTF-8') as r:
        read = r.readlines()
        print(read)
        result = Counter(read)
        print(result)
        d = sorted(result.items(), key=lambda k: k[1])
        list1 = []
        list2 = []
        for each in d:
            list1.append(each[0])
            list2.append(each[1])
        # get_charts(list1, list2, 'label', 3)
        print(d[-1])
        print(d[-2])
        print(d[-3])
        print(d[-4])
        print(d[-5])
extract_data_save_to_txt()


# 结果：
# ('ANOTHER\n', 13426)
# ('OTHERS\n', 11359)
# ('HKSAR\n', 9624)
# ('香港特別行政區\n', 8058)
# ('THE QUEEN\n', 5685)