'''
爬取数据
'''
from bs4 import BeautifulSoup
from selenium import webdriver
import warnings
import csv
import sqlite3


#工具函数：用于请求页面并返回页面数据
def get_web_data(url):
    service_args = []
    service_args.append('--load-images=no')  ##关闭图片加载
    service_args.append('--disk-cache=yes')  ##开启缓存
    service_args.append('--ignore-ssl-errors=true')  ##忽略https错误
    warnings.filterwarnings('ignore')
    browser = webdriver.PhantomJS(service_args=service_args)
    web_data = None
    try:
        browser.get(url)
        web_data = browser.page_source
    except:
        print('请求错误！')
    return web_data


#获取法院名字及url并以列表方式返回
def get_court_data(web_data):
    soup = BeautifulSoup(web_data,'lxml')
    court_list = soup.select('#myMenuID a')
    court_name_list = []
    court_url_list = []
    court_data = []
    for court in court_list:
        if  'href' in str(court):
            print(court.text,court.get('href'))
            court_name_list.append(court.text)
            court_url_list.append(court.get('href'))
            court_data.append([court.text,court.get('href')])
    #print(court_name_list)
    #print(court_url_list)
    #print(court_data)
    return court_data


#获取子类的名称及url并以列表方式返回
def get_court_subclass(court_data):
    web_data = get_web_data(court_data[1])
    soup = BeautifulSoup(web_data,'lxml')
    subclass_list = soup.select('.ThemeXPTreeLevel1 a')
    subclass_name_list = []
    subclass_url_list = []
    subclass_data = []
    for court in subclass_list:
        if 'href' in str(court):
            #print(court.text, court.get('href'))
            subclass_name_list.append(court.text)
            subclass_url_list.append(court.get('href'))
            subclass_data.append([court_data[0], court.text, court.get('href')])
    #print(subclass_name_list)
    #print(subclass_url_list)
    #print(subclass_data)
    return subclass_data


def get_court_subclass_years(subclass_data):
    web_data = get_web_data(subclass_data[2])
    soup = BeautifulSoup(web_data,'lxml')
    years = soup.select('.ThemeXPTreeLevel1 .ThemeXPTreeLevel1 a')
    year_list = []
    year_url_list = []
    year_data = []
    for year in years:
        if 'href' in str(year):
            year_list.append(year.text)
            year_url_list.append(year.get('href'))
            year_data.append([subclass_data[0], subclass_data[1], year.text, year.get('href')])
    #print("@@@@@@@@@@",year_data)
    if 'Pre' in str(year_data[-1][2]):
        web_data1 = get_web_data(year_data[-1][3])
        soup1 = BeautifulSoup(web_data1, 'lxml')
        years1 = soup1.select('.ThemeXPTreeLevel1 .ThemeXPTreeLevel1 #JSCookTreeFolderClosed .ThemeXPFolderText a')
        year_list1 = []
        year_url_list1 = []
        year_data1 = []
        for year1 in years1:
            if 'href' in str(year1):
                year_list1.append(year1.text)
                year_url_list1.append(year1.get('href'))
                year_data1.append([subclass_data[0], subclass_data[1], year1.text, year1.get('href')])
        return year_data1
    else:
        return year_data
    #print(year_list)
    #print(year_url_list)
    #print(year_data)
    #return year_data


#写入csv文件头部
def save_to_csv():
    with open('legal_proceedings_data.csv', 'a', newline='') as csvfile:
        fieldnames = ['court', 'subclass', 'year', 'id', 'time', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        csvfile.close()


#获取诉讼结果的编号，时间，内容，并将分类加入存储到csv
def get_details(year_data):
    data_list = year_data[3].split('?')
    base_url = data_list[0] + '?page={}&'+data_list[1]
    url = base_url.format(1)
    web_data = get_web_data(url)
    soup = BeautifulSoup(web_data,'lxml')
    pages = soup.select('a.pagefont')
    if len(pages) > 0:
        for each in range(len(pages)+1):
            web_data1 = get_web_data(base_url.format(each+1))
            print(base_url.format(each+1))
            soup_1 = BeautifulSoup(web_data1,'lxml')
            # type_list = soup.select('.ThemeXPTreeLevel1 .ThemeXPTreeLevel1 .ThemeXPTreeLevel1 #JSCookTreeItem .ThemeXPItemText img')
            tr_list1 = soup_1.select('.ThemeXPTreeLevel1 .ThemeXPTreeLevel1 .ThemeXPTreeLevel1 #JSCookTreeItem .ThemeXPItemText table tbody tr td table tbody tr')
            id_list_1 = []
            time_list_1 = []
            content_list_1 = []
            for tr in tr_list1:
                soup1_1 = BeautifulSoup(str(tr), 'lxml')
                # td0 = soup1.select('td')[0]
                td_1 = soup1_1.select('td')[1]
                td_2 = soup1_1.select('td')[2]
                soup_td_1 = BeautifulSoup(str(td_1), 'lxml')
                try:
                    id = soup_td_1.select('a')[0].text
                except:
                    id = '无'
                try:
                    time = soup_td_1.select('font')[0].text
                except:
                    time = '无'
                content = td_2.text
                legal_data = {
                    'court': year_data[0],
                    'subclass': year_data[1],
                    'year': year_data[2],
                    'id': id,
                    'time': time,
                    'content': content
                }
                print('多页：',legal_data)
                with open('legal_proceedings_data.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
                    fieldnames = ['court', 'subclass', 'year', 'id', 'time', 'content']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    # writer.writeheader()
                    writer.writerow(legal_data)
                    csvfile.close()
        # print(len(pages))
        # print(url)
        # page_total = int(pages[-1].text)
        # print(page_total)
        # for num in range(page_total):
        #     print(base_url.format(num+1))
    else:
        #type_list = soup.select('.ThemeXPTreeLevel1 .ThemeXPTreeLevel1 .ThemeXPTreeLevel1 #JSCookTreeItem .ThemeXPItemText img')
        print(base_url.format(1))
        tr_list = soup.select('.ThemeXPTreeLevel1 .ThemeXPTreeLevel1 .ThemeXPTreeLevel1 #JSCookTreeItem .ThemeXPItemText table tbody tr td table tbody tr')
        id_list = []
        time_list = []
        content_list = []
        for tr in tr_list:
            soup1 = BeautifulSoup(str(tr),'lxml')
            #td0 = soup1.select('td')[0]
            td1 = soup1.select('td')[1]
            td2 = soup1.select('td')[2]
            soup_td1 = BeautifulSoup(str(td1),'lxml')
            try:
                id = soup_td1.select('a')[0].text
            except:
                id = '无'
            try:
                time = soup_td1.select('font')[0].text
            except:
                time = '无'
            content = td2.text
            legal_data = {
                'court':year_data[0],
                'subclass':year_data[1],
                'year':year_data[2],
                'id':id,
                'time':time,
                'content':content
            }
            print('单页：',legal_data)
            with open('legal_proceedings_data.csv', 'a', newline='',encoding='utf-8-sig') as csvfile:
                fieldnames = ['court', 'subclass','year','id','time','content']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                #writer.writeheader()
                writer.writerow(legal_data)
                csvfile.close()
            # print(id)
            # print(time)
            # print(content)
        # print(time_list)
        #print(content_list)
    # for i in pages:
    #     print(i.text)

def main():
    url = 'https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp'
    web_data = get_web_data(url)
    court_data = get_court_data(web_data)
    save_to_csv()
    for data in court_data:
        subclass_data = get_court_subclass(data)
        for data1 in subclass_data:
            data2 = get_court_subclass_years(data1)
            # pool.map(get_details,data2)
            # pool.close()
            # pool.join()
            #print(data2)
            for each in data2:
                get_details(each)
    # data = [1,2,3,'https://legalref.judiciary.hk/lrs/common/ju/judgment.jsp?EX=&L1=FA&L2=CC&L3=2013&AR=1_6#A1_6']
    # get_details(data)


if __name__ == '__main__':
    main()