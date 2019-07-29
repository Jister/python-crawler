import requests
import urllib
import urllib.parse
import json
import csv 
import time
import random
# 用于生成随机userAgent
# from fake_useragent import UserAgent
# ua = UserAgent()
cookies[4]=[
'',
'',
'',
'']

fileHeader = ['店铺名','评价','评价数','月售','配送费','地址','品类','电话','营业时间','距离']
fileContent = []
fileHeader2 = ['店铺','商品','标签','价格','月销量','主要原料']
fileContent2 = []
# 商品商品请求链接
menuUrl = 'https://www.ele.me/restapi/shopping/v2/menu'
#店铺请求链接
#webUrl = 'https://www.ele.me/restapi/shopping/restaurants'
webUrl = 'https://mainsite-restapi.ele.me/shopping/restaurants'
#extras = 'extras%5B%5D=activities&geohash=wtw1r8ew6tuw&latitude=31.161078&limit=24&longitude=121.27201&offset=0&terminal=web'
#url = 'https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=wtw1r8ew6tuw&latitude=31.161078&limit=24&longitude=121.27201&offset=48&terminal=web'
#需要更换cookie
header = {
    'cookie':'ubt_ssid=m52pe06yyaejcqxlz9x1686t8ie4fkxc_2019-06-08; _utrace=35cf4168f81f765256ee36d9743aba08_2019-06-08; cna=7vnuD2ai7BMCAd4sVr33SmO2; track_id=1559983155|fba4ca2b09e5344835ebb518119f4675cae8716caeaadd2338|d1f257cf884b25dcbf53e731852262a9; tzyy=7640beceed673e2b65f9b64a60332073; ut_ubt_ssid=vkf0vjkxqugi1en8s3mfqfz1qajjxdnj_2019-07-16; USERID=213622608; UTUSER=213622608; SID=OQQodQZhhvWP8D6abiq2r5s7ja4GspVYWTDg; ZDS=1.0|1563366966|XsZPqPM9Er9L3xZrcH5UB7Mk0tC8EYCpeNTHz5XtcaPhVc0rdn30rE7WtaD36apgE/H3iN6Yoo9L+O0Pcfah4A==; pizza73686f7070696e67=CPuz42fVoxnRVcVQ1x33fSMNnyWTsQFk40S1tg0vkhcG-AOSptNfAGKoWLJCi3gy; isg=BCoqgSFcA8rISI5ylhd7qaU-e5AMM4UVTjWNQ7Tj3X0I58qhnCl1BVFWc1PeFyaN; l=cBjri9wuqriXPhUYBOCwVuIRX7bTjIRAguPRwkO6i_5pK6T10oQOkD0u_F96cjWdtd8B4tb6Mew9-etlwQiEkl5xD205.',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

allRestuarant = []

# 从CSV导入所有需要查询的地区经纬度坐标
inputData = []
with open('input.csv') as csvfile:
    lines = csvfile.readlines()
    for line in lines:
        inputData.append(line.split(','))

for region in inputData:
    if region[0] == 'location':
        continue;
    #搜索区域中心的经纬度
    location = region[0]
    longitude = region[1]
    latitude = region[2]
    geohash = region[3]
    offset = 0
    params={
        'extras[]':'activities',
        'geohash': geohash,
        'limit': 24,
        'latitude': latitude,
        'longitude': longitude,
        'terminal': 'web',
        'offset': offset
    }
    extras = urllib.parse.urlencode(params)
    url = webUrl + '?' + extras
    print(url)
    header1 = header
    header1['referer'] ='https://www.ele.me/place/wtw1r8ew6tuw?latitude=%s&longitude=%s' % (latitude, longitude)
    result = requests.get(url,headers=header1).text
    ret = json.loads(result)
    allRestuarant.extend(ret)

    while len(ret) is not 0:
        # 每次请求休眠随机时间，降低请求负载
        time.sleep(random.random()*3)
        offset = offset + 24
        params={
            'extras[]':'activities',
            'geohash': geohash,
            'limit': 24,
            'latitude': latitude,
            'longitude': longitude,
            'terminal': 'web',
            'offset': offset
        }
        extras = urllib.parse.urlencode(params)
        url = webUrl + '?' + extras
        print(url)
        header1['referer'] ='https://www.ele.me/place/wtw1r8ew6tuw?latitude=%s&longitude=%s' % (latitude, longitude)
        header1['user-agent'] = ua.random
        result = requests.get(url,headers=header1).text
        ret = json.loads(result)
        # with open("./test.json","w") as f:
        #     json.dump(ret,f)
        #     print("写入文件完成...")
        allRestuarant.extend(ret)

    # json保存成文件
    with open("./shops.json","w") as f:
        json.dump(allRestuarant,f)
        print("写入文件完成...")

    # 获得需要的店铺信息
    for item in allRestuarant:
        # print(item['name'])
        tag = ''
        for tags in item['flavors']:
            tag = tag + tags['name'] + ' '
        colum = [''] * 10
        colum[0] = item['name']
        colum[1] = item['rating']
        colum[2] = item['rating_count']
        colum[3] = item['recent_order_num']
        colum[4] = item['float_delivery_fee']
        if 'address' in item:
            colum[5] = item['address']
        colum[6] = tag
        if 'phone' in item:
            colum[7] = item['phone']
        colum[8] = item['opening_hours']
        colum[9] = item['distance']

        # 获得店铺地址与电话****电话拿不到****
        # params={
        #     'latitude': '%s' % item['latitude'],
        #     'longitude': '%s' % item['longitude'],
        #     'terminal': 'web',
        # }
        # extras = urllib.parse.urlencode(params)
        # #url = 'https://www.ele.me/restapi/shopping/restaurant/E12898842484495203641?extras%5B%5D=flavors&extras%5B%5D=qualification&latitude=31.198751&longitude=121.436576&terminal=web'
        # url = 'https://www.ele.me/restapi/shopping/restaurant/' + item['id'] + '?' + 'extras%5B%5D=flavors&extras%5B%5D=qualification&' + extras
        # print(url)
        # header2  = header
        # header2['referer'] = 'https://www.ele.me/shop/' + item['id']
        # header2['x-shard'] = 'shopid=%s;loc=%s,%s'%(item['id'], item['longitude'], item['latitude'])
        # result = requests.get(url,headers=header2).text
        # if result:
        # ret = json.loads(result)
        # # with open("./test111.json","w") as f:
        # #     json.dump(ret,f)
        # # print("写入文件完成...")
        # if 'address' in ret:
        #     colum[5] = ret['address']
        # if 'phone' in ret:    
        #     colum[7] = ret['phone']

        fileContent.append(colum)

    print('共搜索到%d家店铺'%len(allRestuarant))
    # 写入CSV
    with open(location+'-店铺.csv','w',newline='',encoding='utf-8')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(fileHeader)
        f_csv.writerows(fileContent)

    for shop in allRestuarant:
        # 每次请求休眠随机时间，降低请求负载
        time.sleep(random.random()*3)
        print(shop['name'])
        params={
            'restaurant_id':shop['id'],
            'terminal': 'web',
        }
        url = menuUrl + '?' + urllib.parse.urlencode(params)
        print(url)
        header3 = header
        header3['referer'] = 'https://www.ele.me/shop/' + shop['id']
        header3['x-shard'] = 'shopid=%s;loc=%s,%s'%(shop['id'], shop['longitude'], shop['latitude'])
        # 发起请求
        result = requests.get(url,headers=header3).text
        try:
            ret = json.loads(result)
        except:
            with open(shop['name']+"_error.json","w") as f:
                f.write(result)
        else:
            # 获取商品
            for item in ret:
                if 'foods' in item:
                    for goods in item['foods']:
                        colum = [''] * 6
                        colum[0] = shop['name']
                        colum[1] = goods['name']
                        colum[2] = item['name']
                        colum[3] = goods['lowest_price']
                        colum[4] = goods['month_sales']
                        colum[5] = goods['materials']
                        fileContent2.append(colum)
                else:
                    print('request failed')

        # with open("./detail.json","w") as f:
        #     json.dump(ret,f)
        #     print("写入文件完成...")

    with open(location+'-商品.csv','w',newline='',encoding='utf-8')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(fileHeader2)
        f_csv.writerows(fileContent2)

# 从文件读取商铺信息
# with open('./shops.json','r') as f:
#     allRestuarant = json.load(f)
# # 请求每家商铺商品信息
# for shop in allRestuarant:
#     print(shop['name'])
#     params={
#         'restaurant_id':shop['id'],
#         'terminal': 'web',
#     }
#     url = menuUrl + '?' + urllib.parse.urlencode(params)
#     print(url)
#     header['referer'] = 'https://www.ele.me/shop/' + shop['id']
#     header['x-shard'] = 'shopid=%s;loc=%s,%s'%(shop['id'], shop['longitude'], shop['latitude'])
#     # print(header)
#     # 发起请求
#     result = requests.get(url,headers=header).text
#     ret = json.loads(result)
#     with open("./detail.json","w") as f:
#         json.dump(ret,f)
#         print("写入文件完成...")
#     #获取商品
#     for item in ret:
#         for goods in item['foods']:
#             colum = [''] * 6
#             colum[0] = shop['name']
#             colum[1] = goods['name']
#             colum[2] = item['name']
#             colum[3] = goods['lowest_price']
#             colum[4] = goods['month_sales']
#             colum[5] = goods['materials']
#             fileContent2.append(colum)
#     break

# with open('detail.csv','w',newline='',encoding='utf-8')as f:
#     f_csv = csv.writer(f)
#     f_csv.writerow(fileHeader2)
#     f_csv.writerows(fileContent2)
