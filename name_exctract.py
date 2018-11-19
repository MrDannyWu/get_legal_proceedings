'''
人名或公司名提取
'''
import csv
def extract_data_save_to_txt():
    with open('legal_datas2.csv','r',encoding='UTF-8') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [row['content'] for row in reader]
    name_list = []
    name_list1 = []
    for i in column:
        if  'Reported in' in i:
            content = i.split('Reported in')[0]
            if  'v.' in content:
                content_ist = content.split('v.')
                print(content_ist[0].strip(),'==>',content_ist[1].strip())
                name_list.append(content_ist[0].strip())
                name_list.append(content_ist[1].strip())
            elif  '訴' in content:
                content_ist = content.split('訴')
                print(content_ist[0].strip(), '==>', content_ist[1].strip())
                name_list.append(content_ist[0].strip())
                name_list.append(content_ist[1].strip())
            elif '對' in content:
                content_ist = content.split('對')
                print(content_ist[0].strip(), '==>', content_ist[1].strip())
                name_list.append(content_ist[0].strip())
                name_list.append(content_ist[1].strip())
            else:
                print('有关： ',content.strip())
                name_list.append(content.strip())
        else:
            content = i
            if  'v.' in content:
                content_ist = content.split('v.')
                print(content_ist[0].strip(),'==>',content_ist[1].strip())
                name_list.append(content_ist[0].strip())
                name_list.append(content_ist[1].strip())
            elif  '訴' in content:
                content_ist = content.split('訴')
                print(content_ist[0].strip(), '==>', content_ist[1].strip())
                name_list.append(content_ist[0].strip())
                name_list.append(content_ist[1].strip())
            elif '對' in content:
                content_ist = content.split('對')
                print(content_ist[0].strip(), '==>', content_ist[1].strip())
                name_list.append(content_ist[0].strip())
                name_list.append(content_ist[1].strip())
            else:
                print('有关： ',content.strip())
                name_list.append(content.strip())
    csvfile.close()
    for j in name_list:
        print(j)
        with open('name1.txt','a',encoding='utf-8') as txtfile:
            txtfile.write(str(j)+'\n')
        txtfile.close()


def extract_name_max_num_from_txt():
    with open('name1.txt','r',encoding='utf-8') as r:
        result = r.readlines()
        print(result)
        print(type(result))
        print(max(result,key=result.count))

def extract_data_save_to_txt1(args,filename):
    with open('name1.txt','r',encoding='utf-8') as r:
        result = r.readlines()
        for name in result:
            if args in name:
                name_list = name.split(args)
                for i in name_list:
                    print(i)
                    with open(filename, 'a', encoding='utf-8')as w:
                        if name_list.index(i) == len(name_list)-1:
                            w.write(str(i))
                        else:
                            w.write(str(i) + '\n')

                        w.close()
            else:
                with open(filename, 'a', encoding='utf-8')as w:
                    print(name)
                    w.write(str(name))
                    w.close()

extract_data_save_to_txt1(' AND ','name_no_and.txt')

# extract_name_max_num_from_txt()