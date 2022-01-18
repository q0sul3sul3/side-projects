#!/usr/bin/python3
# coding: utf-8


import requests
import bs4
import argparse
import datetime as dt

parser = argparse.ArgumentParser()
parser.add_argument("keyword", nargs='?', default= '資料科學', type=str, help="get the keyword")
parser.add_argument("--table", nargs='?', default= 'Soft_Job', type=str, help="get the table")
parser.add_argument("-w", "--write", action="store_true", help="write to csv")
args = parser.parse_args()

# keyword = '資料科學' # 搜尋含有'資料科學'的文章
src = "https://www.ptt.cc/bbs/{}/search?q=".format(args.table) + args.keyword
r = requests.get(src) # get 此頁面的 HTML
soup = bs4.BeautifulSoup(r.text, "html.parser") # 用bs4 解析html 資料格式
print(dt.date.today())

if args.write:

    file = open('/tmp/{}.csv'.format(args.keyword), 'w')

    for j in soup.find_all('div', class_="r-ent"):
#         if j.span and int(j.span.string) >= 10: # 有推文數 and 推文數 > 10
        if j.span and (j.span['class']==['hl', 'f3'] or j.span['class']==['hl', 'f1']):
            print('ptt.cc' + j.a['href'], j.span.string, j.a.string)
            data = 'ptt.cc' + j.a['href'] + ' ' + j.span.string + ' ' + j.a.string + '\n'
            file.write(data)
    prepage = soup.find('a', class_="btn wide", string = "‹ 上頁") # 如果沒有上頁 --> None

    while prepage:
        src = 'https://www.ptt.cc' + prepage['href'] # None --> 沒有'href'這個key，會跑不出 prepage['href'] --> KeyError
        r = requests.get(src) # get 此頁面的 HTML
        soup = bs4.BeautifulSoup(r.text, "html.parser") # 用bs4 解析html 資料格式
        for j in soup.find_all('div', class_="r-ent"):
#             if j.span and int(j.span.string) >= 10: # 有推文數 and 推文數 > 10
            if j.span and (j.span['class']==['hl', 'f3'] or j.span['class']==['hl', 'f1']):
                print('ptt.cc' + j.a['href'], j.span.string, j.a.string)
                data = 'ptt.cc' + j.a['href'] + ' ' + j.span.string + ' ' + j.a.string + '\n'
                file.write(data)
        prepage = soup.find('a', class_="btn wide", string = "‹ 上頁")

    file.close()