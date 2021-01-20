import random
import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
import time

path = r'./item_comment_list2'
if not os.path.exists(path):
    os.mkdir(path)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

cookie = {
    'session-id': '140-7979274-1963044',
    'session-id-time': '2082787201l', 'i18n-prefs': 'USD', 'lc-main': 'zh_TW', 'sp-cdn': '"L5Z9:TW"',
    'ubid-main': '131-6233273-5566760',
    'session-token': 'PpeJ3AG6o7SoHIiRDuWiXkntbJmxl9kUBT+vNi1DLsh8NR6NEBFNaUxRevE7xihr2B/ARbgUhpIC+Xtnw4+jZ2VCvH/OeoOdBeRVffWw8gDmSbHMnvxS55xJKrblQGn4lJ9/+bnlQwT/teyhAyWKKIly57vepE3UnVvTgvHnZnhibwkRH9aBO9WMvHvdudSU'
}

df = pd.read_csv('amzon_ETL_20201218.csv')['Description']  # 讀取要爬取的品項名稱
item = []
commentList = []
for i in df:
    item.append(i)  # 商品頁面連結放入list中
for k in item:  # 將品項整理成可放在url的格式
    commentStr = ''
    keywords = k.strip(' ').replace("(", '')  \
                           .replace("/", ' ') \
                           .replace("&", ' ') \
                           .replace(")", '')  \
                           .replace("'", '')  \
                           .replace('*', '')  \
                           .replace('"', ' ') \
                           .replace(':', '')  \
                           .replace('.', ' ') \
                           .replace(' ', '+') \
                           .replace('-', '+')
    k_name = k.strip(' ').replace(' ', '_').replace('-', '_').replace(':', '_').replace('(','_').replace(")", '_')
    url = 'https://www.amazon.com/s?k=' + keywords + '&ref=nb_sb_noss'
    # print(url)  # 搜尋關鍵字之後的頁面連結
    time.sleep(random.uniform(1, 6))  # 睡1~5秒
    res = requests.get(url, headers=headers, cookies=cookie)
    # print(res)
    soup = BeautifulSoup(res.text, 'html.parser')
    itemN1 = soup.select('a.a-link-normal.s-no-outline')
    # print(itemN1)
    if len(itemN1) == 1:
        itemN1 = soup.select('a.a-link-normal.s-no-outline')[0]['href']
    elif len(itemN1) > 1:
        itemN1 = soup.select('a.a-link-normal.s-no-outline')[1]['href']

    item_link = 'https://www.amazon.com' + itemN1
    print(item_link)  # 單一商品頁面連結，有該商品評論
    # print('-' * 50)
    res2 = requests.get(item_link, headers=headers, cookies=cookie)
    soup2 = BeautifulSoup(res2.text, 'html.parser')
    commentFrame = soup2.select('div#cm-cr-dp-review-list')
    com = soup2.select('div.a-expander-content.reviewText.review-text-content.a-expander-partial-collapse-content span')
    # print(com) #一筆商品評論一個list

    try:
        for j in com:
            oneItem_Comment = j.text.strip('\n')  # 去掉前後空白
            commentStr += oneItem_Comment
            # commentStr += '\n-----------------------------------------------\n'
            print(commentStr)  # 一個評論放一行

            with open(path + '/%s.txt' % (k_name), 'w', encoding='utf-8') as f:
                f.write(commentStr)  # 將每項商品的評論各別存檔並依商品名稱為檔名存成txt檔
    except FileNotFoundError as e1:
        print('%s is %s' % (keywords, e1))
    except IndexError as e2:
        print('%s is %s' % (keywords, e2))
        # pass
    except TypeError as e3:
        print('%s is %s' % (keywords, e3))
    except:
        print('another problem')
