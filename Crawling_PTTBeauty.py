'''
思考路線:
1.找到PTT表特版網址，get表特版原始碼
2.由表特版的原始碼，匹配get各個文章網址列表
3.由各個文章原始碼，匹配單一文章中各個圖片網址列表
4.由各個圖片網址列表，下載儲存圖片(由二進位碼寫入檔案中儲存.jpg格式)
'''

from selenium import webdriver
from selenium.webdriver.common.by import By

import requests
import re

import os
from urllib.request import urlretrieve
from urllib import request, error
    
browser = webdriver.PhantomJS()
url = "https://www.ptt.cc/bbs/beauty/index.html"
browser.get(url)
browser.implicitly_wait(3)
#page source盡量用selenium爬取，不要用requests可能被擋
content_beauty = browser.page_source 

'''
#刪文章不要讀
#topic 用selenium爬，回傳是element的list
topic = browser.find_elements_by_class_name('title')
'''

#文章連結們topic_url用Regex爬，回傳字串的list，
topic_url = re.findall('mark.*?title.*?href="(.*?)">.*?</a>', content_beauty, re.S)

#驗證是否有抓到文章列表
''' 
#被刪除的文章不要讀
print(len(topic)) #這是element的list
'''
print("PTT_Beauty文章列表\n")
print(topic_url) #這是list
print("\n")

#爬topic_url-4篇文章，因為要扣除【版規文章】
for i in range(0, len(topic_url)-4):
    
    #topic是element的list，所以要.text才可以看內容
    browser.get("https://www.ptt.cc"+topic_url[i])
    topic = browser.find_elements_by_class_name('article-meta-value') 
    #會有作者[0]、看板[1]、標題[2]、時間[3]
    print("標題: "+topic[2].text+" 作者: "+topic[0].text+" 時間: "+topic[3].text+"\n")

    #獲取文章的source code，用selenium比較保險
    content_topic = browser.page_source

    #抓取文章內的pic_url，使用list儲存
    pic_url = re.findall('<a href=".*?" target="_blank.*?nofollow.*?">(.*?)</a>', content_topic, re.S)

    #爬1到pic_url-1篇文章，因為要扣除【置底連結】
    for i in range(0, len(pic_url)-1):
        print(pic_url[i]+"\n") #印出每張圖片連結，確認網址都對
        
		pic = requests.get(pic_url[i])
		
		#文章名當標題，for迴圈順序當附加，記得用.jpg當結尾不然不能簡單看
        pic_title = topic[2].text+"_"+str(i)+".jpg"
        
		#由連結下載寫入圖片二進位碼
        with open(pic_title,'wb') as f:
            f.write(pic.content)
            f.close()
		#存取位置就是執行python程式的位置(不是python程式的位置)
            
browser.close()