import requests
import urllib
import urllib.parse
import json
import csv 
import time
import random

#inputData = [['东昌大楼', '121.513375', '31.23252']]
#inputData = [['金桥新城', '121.607994', '31.266537']]
#inputData = [['蕉丽新村', '121.610431', '31.201243']]
#inputData = [['绿梅二村', '121.368963', '31.115158']]
inputData = [['万科城花新园', '121.334995', '31.153221']]
proxies = [
{'http':'http://117.149.12.242:8060','https':'https://117.149.12.242:8060'},
{'http':'http://125.62.27.53:3128','https':'https://125.62.27.53:3128'},
{'http':'http://36.250.156.10:9999','https':'https://36.250.156.10:9999'}]

# 从config.txt读取cookie和userId
cookie_list = []
user_list = []
# 写CSV 文件
fileHeader = ['店铺名','评价','评价数','月售','配送费','地址','品类','电话','营业时间','距离']
fileContent = []
fileHeader2 = ['店铺','商品','标签','价格','月销量','主要原料']
fileContent2 = []

header = {
    'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

allRestuarant = []

# 读取config信息
def get_config():
    global cookie_list, user_list
    cookie_list = []
    user_list = []
    with open("config.txt","r") as f:
        lines = f.readlines()
        flag = ''
        for line in lines:
            if 'cookies' in line:
                flag = 'cookies'
                continue
            if 'users' in line:
                flag = 'users'
                continue
            if flag is 'cookies':
                cookie_list.append(line[:-1])
            if flag is 'users':
                if '\n' in line:
                    line = line[:-1]
                user_list.append(line)

if __name__=="__main__":
    # 读取cookie和user信息
    get_config();

    for region in inputData:
        location = region[0]
        longitude = region[1]
        latitude = region[2]
        offset = 0
        url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude=%s&longitude=%s&offset=%d&limit=8&extras[]=activities&extras[]=tags&extra_filters=home&rank_id=&terminal=h5' % (latitude, longitude, offset)
        print(url)
        header1 = header
        cookie_index = int(random.random()*2)
        header1['cookie'] = cookie_list[cookie_index]
        header1['referer'] = 'https://h5.ele.me/msite/'
        header1['x-shard'] = 'loc=%s,%s' % (longitude, latitude)
        header1['x-uab'] = '118#ZVWZz4EwVT6G1Z4KBZWlZYquZYT4zHWzZgC2Voq4mF860fgTyHRxZZgZZzqhzHRzZgCZXfquZg2zZZFhH0uXzZ2ZZ0NTzeWzzgeuVfq4zH2ZZZChXHR4ZggZZzqhzHRZZXquVfq4zH2z5HK6DHW46NX0sXnVcP+JDZZZRM9B3/sZ4ezeQDu2UtMf25wNvgqWjylaLcACMgCf4CJSugZCmrDtKHZzhXRzzFhLRZZTtW+v+jgn5grodu+nF/A6AGJPjDMwppa/DIoX7Yvi/+I63idV/AtYiuOoatJNQyRMPiTLEo1IClvGr+aqJX6HK2icwk3Ny/D/y3gErD+x5/WA//thJvVChjy0kcT0gM41aJ7EMNnm7QjzKxGQW6U71pPQwb7YXRF0gF3bMMGct05wMiC3OEBtU4a5gb3GYWG0GK1FHyXyuQUGEIJpDkB1P227AK9aP21VnGShlpH96vx72R+AA1tyYxh5tfqymRRxjCIs1FPzB8hMq2eKFWcz8Vi4hltTuY1oJjYJ66SokCc+V54Xxf48uQsDZVyUcnb+Yg=='
        try:
            result = requests.get(url,headers=header1).text
        except:
            print('Request failed....Try again....')
            result = requests.get(url,headers=header1).text
        ret = json.loads(result)
        
        # json保存成文件
        with open("log.json","w") as f:
            json.dump(ret,f)
            print("写入文件完成...")

        allRestuarant.extend(ret['items'])

        while ret['has_next']:
            # 每次请求休眠随机时间，降低请求负载
            time.sleep(random.random()*5)
            offset = offset + 8
            rankId = ret['meta']['rank_id']
            url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude=%s&longitude=%s&offset=%d&limit=8&extras[]=activities&extras[]=tags&extra_filters=home&rank_id=%s&terminal=h5' % (latitude, longitude, offset, rankId)
            print(url)
            cookie_index = int(random.random()*2)
            #proxy_index = int(random.random()*3)
            #print(proxies[proxy_index])
            header1['cookie'] = cookie_list[cookie_index]

            try:
                #result = requests.get(url,headers=header1,proxies = proxies[proxy_index]).text
                result = requests.get(url,headers=header1).text
            except:
                print('Request failed....Try again....')
                result = requests.get(url,headers=header1).text
            ret = json.loads(result)
            with open("log.json","w") as f:
                json.dump(ret,f)
                print("写入文件完成...")

            if 'items' in ret:
                allRestuarant.extend(ret['items'])
            else:
                event = True
                while(event):
                    cin = input('输入c继续')
                    if cin == 'c':
                        event = False
                # 重新读取config并设置cookie
                get_config();
                cookie_index = int(random.random()*2)
                header1['cookie'] = cookie_list[cookie_index]
                result = requests.get(url,headers=header1).text
                ret = json.loads(result)
                with open("log.json","w") as f:
                    json.dump(ret,f)
                    print("写入文件完成...")
                allRestuarant.extend(ret['items'])

        with open(location+"allshops_h5.json","w") as f:
            json.dump(allRestuarant,f)
            print("写入文件完成...")

        print('共搜索到%d家店铺'%len(allRestuarant))
        allCount = len(allRestuarant)
        count = 0

        # 获得店铺详细信息
        for item in allRestuarant:
            count = count + 1
            print('%d/%d'%(count,allCount))
            print(item['restaurant']['name'])
            tag = ''
            for tags in item['restaurant']['flavors']:
                tag = tag + tags['name'] + ' '
            colum = [''] * 10
            colum[0] = item['restaurant']['name']
            colum[1] = item['restaurant']['rating']
            colum[2] = item['restaurant']['rating_count']
            colum[3] = item['restaurant']['recent_order_num']
            colum[4] = item['restaurant']['float_delivery_fee']
            colum[6] = tag
            colum[8] = item['restaurant']['opening_hours']
            colum[9] = item['restaurant']['distance']
            #****************************************
            #请求店铺商品
            #****************************************
            cookie_index = int(random.random()*2)
            shop_id = item['restaurant']['id']
            user_id = user_list[cookie_index]
            shop_lat = item['restaurant']['latitude']
            shop_lon = item['restaurant']['longitude']
            time.sleep(random.random()*5)
            url = 'https://h5.ele.me/pizza/shopping/restaurants/%s/batch_shop?user_id=%s&code=0.898602164780357&extras=[\"activities\",\"albums\",\"license\",\"identification\",\"qualification\"]&terminal=h5&latitude=%s&longitude=%s' % (shop_id, user_id, shop_lat, shop_lon)
            print(url)
            header2 = header
            header2['cookie'] = cookie_list[cookie_index]
            header2['referer'] = 'https://h5.ele.me/shop/'
            header2['x-shard'] = 'shopid=%s;loc=%s,%s' % (shop_id, shop_lon, shop_lat)
            header2['x-uab'] = '118#ZVWZz4EwVT6G1Z4KBZWlZYquZYT4zHWzZgC2Voq4mF860fgTyHRxZZgZZzqhzHRzZgCZXfquZg2zZZFhH0uXzZ2ZZ0NTzeWzzgeuVfq4zH2ZZZChXHR4ZggZZzqhzHRZZXquVfq4zH2z5HK6DHW46NX0sXnVcP+JDZZZRM9B3/sZ4ezeQDu2UtMf25wNvgqWjylaLcACMgCf4CJSugZCmrDtKHZzhXRzzFhLRZZTtW+v+jgn5grodu+nF/A6AGJPjDMwppa/DIoX7Yvi/+I63idV/AtYiuOoatJNQyRMPiTLEo1IClvGr+aqJX6HK2icwk3Ny/D/y3gErD+x5/WA//thJvVChjy0kcT0gM41aJ7EMNnm7QjzKxGQW6U71pPQwb7YXRF0gF3bMMGct05wMiC3OEBtU4a5gb3GYWG0GK1FHyXyuQUGEIJpDkB1P227AK9aP21VnGShlpH96vx72R+AA1tyYxh5tfqymRRxjCIs1FPzB8hMq2eKFWcz8Vi4hltTuY1oJjYJ66SokCc+V54Xxf48uQsDZVyUcnb+Yg=='
            try:
                #proxy_index = int(random.random()*3)
                #print(proxies[proxy_index])
                #result = requests.get(url,headers=header1,proxies = proxies[proxy_index]).text
                result = requests.get(url,headers=header2).text
            except:
                event = True
                while(event):
                    cin = input('输入c继续')
                    if cin == 'c':
                        event = False
                # 重新读取config并设置cookie
                get_config();
                cookie_index = int(random.random()*2)
                header2['cookie'] = cookie_list[cookie_index]
                result = requests.get(url,headers=header2).text

            ret = json.loads(result)
            with open("log.json","w") as f:
                json.dump(ret,f)
                print("写入文件完成...")

            # 补充店铺地址和电话
            if 'rst' in ret:
                colum[5] = ret['rst']['address']
                colum[7] = ret['rst']['phone']
                fileContent.append(colum)
            else:
                event = True
                while(event):
                    cin = input('输入c继续')
                    if cin == 'c':
                        event = False
                # 重新读取config并设置cookie
                get_config();
                cookie_index = int(random.random()*2)
                header2['cookie'] = cookie_list[cookie_index]
                result = requests.get(url,headers=header2).text
                ret = json.loads(result)

                if 'rst' in ret:
                    colum[5] = ret['rst']['address']
                    colum[7] = ret['rst']['phone']
                    fileContent.append(colum)
                else:
                    continue

            for menu in ret['menu']:
                for food in menu['foods']:
                    food_colum = [''] * 6
                    food_colum[0] = item['restaurant']['name']
                    food_colum[1] = food['name']
                    food_colum[2] = menu['name']
                    if 'lowest_price' in food:
                        food_colum[3] = food['lowest_price']
                    food_colum[4] = food['month_sales']
                    if 'materials' in food:
                        food_colum[5] = food['materials']
                    fileContent2.append(food_colum)
        # # 写入CSV
        with open(location+'-店铺.csv','w',newline='',encoding='utf-8')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(fileHeader)
            f_csv.writerows(fileContent)
        with open(location+'-商品.csv','w',newline='',encoding='utf-8')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(fileHeader2)
            f_csv.writerows(fileContent2)