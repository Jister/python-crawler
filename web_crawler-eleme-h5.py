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

#cookie_list = [
#'ubt_ssid=m52pe06yyaejcqxlz9x1686t8ie4fkxc_2019-06-08; _utrace=35cf4168f81f765256ee36d9743aba08_2019-06-08; perf_ssid=1h2wp75l1yfh4qk2l76rafn7ut5qk2d4_2019-06-08; cna=7vnuD2ai7BMCAd4sVr33SmO2; track_id=1559983155|fba4ca2b09e5344835ebb518119f4675cae8716caeaadd2338|d1f257cf884b25dcbf53e731852262a9; tzyy=7640beceed673e2b65f9b64a60332073; _bl_uid=sejv2xz3h90hF6yjzv3R21y3vw5j; ut_ubt_ssid=vkf0vjkxqugi1en8s3mfqfz1qajjxdnj_2019-07-16; l=cBjri9wuqriXPtQTBOCNCuI8Us7tIIRYouPRwd0Xi_5CP6T1K4QOkqcfoF96cjWdOc8p4tb6Mew9-etk9w5pBKCxD205.; USERID=159589; UTUSER=159589; SID=KEm8yV0CTBl3sL7DUcxkvvFPLpKlsRJlebDw; ZDS=1.0|1563636325|jNJfGb5I/WzphbYPCJMvmU1o30xRiL3AEQAgiVwJ1QMkrkcn6XXPRJqKctzVbA9O; pizza73686f7070696e67=_HHDoSEnvf2x_BZ4BJF9V3Q7q-45CmYggiJ9Ib-kSwzP2geRNRCtDzTRq0riFwCa; isg=BL6-x1x3b1p2XLq26nMntbESD9TAV4ARozwAVWjHK4H8C1_l0I-8jOTqh5FiNXqR',
#'ubt_ssid=x16s67tlrrd4dhpqak1xncmdogmtb1iy_2019-07-21; _utrace=a22b3c83552c17e6e844b597ea50424b_2019-07-21; cna=0pO6EwacoRICAbSul5USoXE/; l=cBjqYpHnq_I_DSkJBOCwCuI8Ly7TSIRxGuPRwCcMi_5QZ6T6S6QOk4FQnF96DbBdt0Yp4082vew9-etkvvIr813kml3C.; perf_ssid=ff82cd599uhtz7txbq9b2m0ra02m6gad_2019-07-21; ut_ubt_ssid=qcpjfigc79xt8bnc3emvhk383vqfukag_2019-07-21; _bl_uid=ebj7ky01dzv2n6ln3wn0sqIbnge2; track_id=1563720206|63e9aba5865f1c2f8e2ddfefc6aa58746c341e9a5aff67b354|97778ccf71f05e67dc791843b6df9844; USERID=109018827; UTUSER=109018827; SID=r8C7qMcjy2sdx7rb7a6zbLr5pBBjchUR1FMw; ZDS=1.0|1563720206|KBKL+MCYwizxq5wQgAQ3JG8NkBpd1fPYOtI33vsfKYZO+Y3VEK/a4ioX+P+Ax2K2; isg=BIaGaYugJ6W2lvPB2c3l8i8v13zIT8uknMwcrnCvdqmEcyKNyXfIsD0CTukaLMK5'
#]
#user_list = ['159589','109018827']
# 从config.txt读取
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
            header1['cookie'] = cookie_list[cookie_index]
            #print(proxies[proxy_index])
            #result = requests.get(url,headers=header1,proxies = proxies[proxy_index]).text
            try:
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
                #proxy_index = int(random.random()*3)
                #result = requests.get(url,headers=header1,proxies = proxies[proxy_index]).text
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