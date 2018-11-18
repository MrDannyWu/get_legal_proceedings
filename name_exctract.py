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

def extract_data_from_txt():
    with open('name1.txt','r',encoding='utf-8') as r:
        result = r.readlines()
        print(result)
        print(type(result))
        print(max(result,key=result.count))
extract_data_from_txt()