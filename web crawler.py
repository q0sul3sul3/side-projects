#!/usr/bin/env python
# coding: utf-8

# # 下載特定網址資料

# In[7]:


# pip install beautifulsoup4


# In[42]:


# 取得網頁的原始碼(HTML, CSS, JSON)
import urllib.request as rq

src = "https://www.ntu.edu.tw"
with rq.urlopen(src) as responce:
    data = responce.read().decode("utf-8")
print(data)


# In[314]:


# 取得網頁的原始碼
# json
import urllib.request as rq
import json

src = "https://data.taipei/api/v1/dataset/296acfa2-5d93-4706-ad58-e83cc951863c?scope=resourceAquire"
with rq.urlopen(src) as responce:
#     data = responce.read().decode("utf-8")
    data = json.load(responce) # 用json 模組讀取json 資料格式
# print(data)

companylist = data["result"]["results"]
# print(companylist) # "request" 中的 "requests" # list

# 將公司列表列出來
for i in companylist:
#     print(i)
#     print(i["公司名稱"])
    print(i["公司名稱"], i["公司地址"], i["\ufeff統編"])

# 寫入txt檔案
with open("company list", "w") as file:
    for i in companylist:
        file.write(i["公司名稱"] + "\n")

# 寫入txt檔案
with open("company list2", "w") as file:
    for i in companylist:
        file.write(i["公司名稱"] + " " + i["公司地址"] + "\n")


# ## 搜尋 PTT soft_job 所有含有keyword的標題
# https://www.ptt.cc/bbs/Soft_Job/index.html
# 
# 1. https://www.ptt.cc/bbs/Soft_Job/search?q=data+engineer
# 2. https://www.ptt.cc/bbs/Soft_Job/search?q=資料分析
# 3. https://www.ptt.cc/bbs/Soft_Job/search?q=資料科學
# 
# 目標：
# 1. 搜尋keyword=資料分析、資料科學的所有文章
# 2. 推文數>10
# 3. 存成.csv

# In[4]:


'''
爬一頁
'''
import requests
import bs4

keywords = '資料科學'
src = "https://www.ptt.cc/bbs/Soft_Job/search?q=" + keywords

r = requests.get(src) # get 此頁面的 HTML
# print(r.text) # 印出 HTML

soup = bs4.BeautifulSoup(r.text, "html.parser") # 用bs4 解析html 資料格式
# print(soup)
# titles = soup.find_all("div", class_="title") # 所有 div標籤且屬性 class_="title"
# print(titles) # [<div class="title">...</div>, ..., ...]

# for i in soup.find_all('div', class_="title"):
#     print(i.a)
#     print(i.a.string)
#     print(i.a['href'])

# ===== 複雜 =====
# print(soup.find_all('div', class_="r-ent"))
# for i in soup.find_all('div', class_="r-ent"):
#     print(i.find('div', class_='nrec').find('span', class_="hl f3"))
#     if i.find('div', class_='nrec').find('span', class_="hl f3"): # 推文 > 10
#         print(i.find('div', class_='nrec').find('span', class_="hl f3").string) # 印出推文數
#         print(i.a['href'], i.find('div', class_='nrec').find('span', class_="hl f3").string + ' ' + i.a.string)

# ===== 簡化 =====
for i in soup.find_all('div', class_="r-ent"):
#     print(i.span)
    if i.span and i.span['class']==['hl', 'f3']: # 有推文數 and 推文數>10
#         print(i.span['class']==['hl', 'f3'])
        print('ptt.cc' + i.a['href'], i.span.string, i.a.string)

prepage = soup.find("a", string = "‹ 上頁")['href']
src = 'ptt.cc' + prepage
# print(src)


# In[5]:


'''
爬三頁 寫入.csv
'''
keywords = '資料科學' # 搜尋含有'資料科學'的文章
src = "https://www.ptt.cc/bbs/Soft_Job/search?q=" + keywords

file = open('{}.csv'.format(keywords), 'w')
for i in range(3): # 搜尋三頁文章
    r = requests.get(src) # get 此頁面的 HTML
    soup = bs4.BeautifulSoup(r.text, "html.parser") # 用bs4 解析html 資料格式
    for j in soup.find_all('div', class_="r-ent"):
        if j.span and j.span['class']==['hl', 'f3']: # 有推文數 and 推文數 > 10
            print('ptt.cc' + j.a['href'], j.span.string, j.a.string) # 印出
            data = 'ptt.cc' + j.a['href'] + ' ' + j.span.string + ' ' + j.a.string + '\n'
            file.write(data)
    print(soup.find('a', class_="btn wide", string = "‹ 上頁")) # 有些頁面沒有 --> None
    print(soup.find('a', string = "‹ 上頁")) # 有些頁面沒有 --> None
    prepage = soup.find('a', string = "‹ 上頁")
    print(prepage.get('href'))
    if soup.find('a', class_="btn wide", string = "‹ 上頁"):    # 如果有上頁連結
        prepage = soup.find('a', class_="btn wide", string = "‹ 上頁")
        src = 'https://www.ptt.cc' + prepage.get('href') # 沒有頁面 None --> 沒有'href'這個key，會跑不出 prepage['href']

#     try: # 若沒用此方法會 KeyError: 'href' # """tag[key] returns the value of the 'key' attribute for the Tag, and throws an exception if it's not there."""
#         prepage = soup.find("a", string = "‹ 上頁")
#         print(prepage)
#         src = 'https://www.ptt.cc' + prepage['href']
#     except:
#         break
file.close()


# In[14]:


'''
這個
'''


# In[6]:


get_ipython().run_line_magic('time', '')
keyword = '資料科學' # 搜尋含有'資料科學'的文章
src = "https://www.ptt.cc/bbs/Soft_Job/search?q=" + keywords

r = requests.get(src) # get 此頁面的 HTML
soup = bs4.BeautifulSoup(r.text, "html.parser") # 用bs4 解析html 資料格式

file = open('{}.csv'.format(keyword), 'w')

for j in soup.find_all('div', class_="r-ent"):
    if j.span and int(j.span.string) >= 10: # 有推文數 and 推文數 > 10
#     if j.span and j.span['class']==['hl', 'f3']:
        print('ptt.cc' + j.a['href'], j.span.string, j.a.string)
        data = 'ptt.cc' + j.a['href'] + ' ' + j.span.string + ' ' + j.a.string + '\n'
        file.write(data)
prepage = soup.find('a', class_="btn wide", string = "‹ 上頁") # 如果沒有上頁 --> None

while prepage:
    src = 'https://www.ptt.cc' + prepage['href'] # None --> 沒有'href'這個key，會跑不出 prepage['href'] --> KeyError
    r = requests.get(src) # get 此頁面的 HTML
    soup = bs4.BeautifulSoup(r.text, "html.parser") # 用bs4 解析html 資料格式
    for j in soup.find_all('div', class_="r-ent"):
        if j.span and int(j.span.string) >= 10: # 有推文數 and 推文數 > 10
#         if j.span and j.span['class']==['hl', 'f3']:
            print('ptt.cc' + j.a['href'], j.span.string, j.a.string)
            data = 'ptt.cc' + j.a['href'] + ' ' + j.span.string + ' ' + j.a.string + '\n'
            file.write(data)
    prepage = soup.find('a', class_="btn wide", string = "‹ 上頁")

file.close()


# In[17]:


get_ipython().run_line_magic('time', '')
def getPTTtitle(url):
    r = requests.get(url) # get 此頁面的 HTML
    soup = bs4.BeautifulSoup(r.text, "html.parser") # 用bs4 解析html 資料格式

    with open('{}.csv'.format(url.split('q=')[1]), 'a') as file:
        for j in soup.find_all('div', class_="r-ent"):
            if j.span and int(j.span.string) >= 10: # 有推文數 and 推文數 > 10
                print('ptt.cc' + j.a['href'], j.span.string, j.a.string)
                file.write('ptt.cc' + j.a['href'] + ' ' + j.span.string + ' ' + j.a.string + '\n')

    return soup.find('a', class_="btn wide", string = "‹ 上頁") # 如果沒有上頁 --> None


# In[18]:


keyword = '資料科學'
url = "https://www.ptt.cc/bbs/Soft_Job/search?q=" + keyword

while True:
    try:
        url = 'https://www.ptt.cc' + getPTTtitle(url)['href']
    except:
        break


# In[14]:


'''
'''
'''


# ## 取得PTT Gossiping版的原始碼
# https://www.ptt.cc/bbs/Gossiping/index.html

# In[316]:


# 取得PTT Gossiping版的原始碼
# 取得標題資訊
# HTTP Error 403: Forbidden 連線被拒絕 --> 要讓連線像使用者
import urllib.request as rq
import requests

url = "https://www.ptt.cc/bbs/Gossiping/index.html"

# r = requests.get(url, headers={'cookie': 'over18=1'})
# data = r.text

# 建立request物件，附加request headers的資訊
# user-agent 使用者上網的模式
request = rq.Request(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36", 
                                   "cookie": "over18=1"}) # cookie

with rq.urlopen(request) as responce:
    data = responce.read().decode("utf-8")
# print(data)

# ====================
import bs4

soup = bs4.BeautifulSoup(data, "html.parser") # 用bs4 解析html 資料格式
# print(soup)
print(soup.title) # title標籤的內容
print(soup.title.string) # title標籤的文字內容

print("==========")

title = soup.find("div", class_="title") # 第一個 div標籤且屬性 class_="title"
print(title)
print(title.a.string) # div標籤的 a標籤文字內容

print("==========")

titles = soup.find_all("div", class_="title") # 所有 div標籤且屬性 class_="title"
print(titles) # [<div class="title">...</div>, ..., ...]

print("==========")

for i in titles:
    if i.a != None:
        print(i.a.string)

##### 取得「‹ 上頁」的連結 #####
previouspage = soup.find("a", string = "‹ 上頁") # a標籤且文字是「‹ 上頁」的內容
print(previouspage)
print(previouspage["href"]) # a標籤的 href屬性的屬性值 # 上頁網址 /bbs/Gossiping/index38942.html
print(previouspage["class"]) # a標籤的 class屬性的屬性值 ['btn', 'wide']


# In[327]:


# 取得PTT Gossiping版的原始碼
# 取得標題資訊
# HTTP Error 403: Forbidden 連線被拒絕 --> 要讓連線像使用者
import urllib.request as rq
import bs4

##### 讀取網頁標題資訊的 function #####
def getpagetitle(url):
    # 建立request物件，附加request headers的資訊
    # user-agent 使用者上網的模式
    request = rq.Request(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36", 
                                       "cookie": "over18=1"}) # cookie
    with rq.urlopen(request) as responce:
        data = responce.read().decode("utf-8")

    soup = bs4.BeautifulSoup(data, "html.parser") # 用bs4 解析html 資料格式
    titles = soup.find_all("div", class_="title") # 所有 div標籤且屬性 class_="title"

    for i in titles:
        if i.a != None:
            print(i.a.string)

    ########## 取得「‹ 上頁」的連結 ##########
    previouspage = soup.find("a", string = "‹ 上頁") # a標籤且文字是「‹ 上頁」的內容
    return previouspage["href"] # a標籤的 href屬性的屬性值 # 上頁網址

# ====================
# url = "https://www.ptt.cc/bbs/Gossiping/index.html"
# url = "https://www.ptt.cc" + getpagedata(url)
# print(url)

# ====================
# 取得三頁文章標題
url = "https://www.ptt.cc/bbs/Gossiping/index.html"
for i in range(3):
    url = "https://www.ptt.cc" + getpagetitle(url) # 完整上頁的網址


# ## 爬 Medium 文章標題

# In[277]:


import urllib.request as rq
import json


url = "https://medium.com/_/graphql"

# 建立request物件，附加request headers和request data的資訊
# user-agent 使用者上網的模式
# request payload # 額外的請求資訊
requestdata = {"operationName":"ExtendedFeedQuery","variables":{"items":[]},"query":"query ExtendedFeedQuery($items: [ExtendedFeedItemOptions!]!) {\n  extendedFeedItems(items: $items) {\n    post {\n      ...PostListModulePostPreviewData\n      __typename\n    }\n    metadata {\n      topic {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PostListModulePostPreviewData on Post {\n  id\n  firstPublishedAt\n  readingTime\n  createdAt\n  mediumUrl\n  previewImage {\n    id\n    __typename\n  }\n  title\n  collection {\n    id\n    domain\n    slug\n    name\n    navItems {\n      url\n      __typename\n    }\n    logo {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    __typename\n  }\n  creator {\n    id\n    name\n    username\n    imageId\n    mediumMemberAt\n    ...userUrl_user\n    __typename\n  }\n  visibility\n  isProxyPost\n  isLocked\n  ...HomeFeedItem_post\n  ...HomeTrendingModule_post\n  __typename\n}\n\nfragment HomeFeedItem_post on Post {\n  __typename\n  id\n  title\n  firstPublishedAt\n  mediumUrl\n  collection {\n    id\n    name\n    domain\n    logo {\n      id\n      __typename\n    }\n    __typename\n  }\n  creator {\n    id\n    name\n    username\n    imageId\n    mediumMemberAt\n    __typename\n  }\n  previewImage {\n    id\n    __typename\n  }\n  previewContent {\n    subtitle\n    __typename\n  }\n  readingTime\n  tags {\n    ...TopicPill_tag\n    __typename\n  }\n  ...BookmarkButton_post\n  ...CreatorActionOverflowPopover_post\n  ...PostPresentationTracker_post\n  ...PostPreviewAvatar_post\n}\n\nfragment TopicPill_tag on Tag {\n  __typename\n  id\n  displayTitle\n}\n\nfragment BookmarkButton_post on Post {\n  visibility\n  ...SusiClickable_post\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment SusiContainer_post on Post {\n  id\n  __typename\n}\n\nfragment AddToCatalogBookmarkButton_post on Post {\n  ...AddToCatalogBase_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBase_post on Post {\n  id\n  viewerEdge {\n    catalogsConnection {\n      catalogsContainingThis(type: LISTS) {\n        catalogId\n        catalogItemIds\n        __typename\n      }\n      predefinedContainingThis {\n        catalogId\n        predefined\n        catalogItemIds\n        __typename\n      }\n      __typename\n    }\n    ...editCatalogItemsMutation_postViewerEdge\n    ...useAddItemToPredefinedCatalog_postViewerEdge\n    __typename\n    id\n  }\n  ...WithToggleInsideCatalog_post\n  __typename\n}\n\nfragment useAddItemToPredefinedCatalog_postViewerEdge on PostViewerEdge {\n  id\n  catalogsConnection {\n    predefinedContainingThis {\n      catalogId\n      version\n      predefined\n      catalogItemIds\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment editCatalogItemsMutation_postViewerEdge on PostViewerEdge {\n  id\n  catalogsConnection {\n    catalogsContainingThis(type: LISTS) {\n      catalogId\n      version\n      catalogItemIds\n      __typename\n    }\n    predefinedContainingThis {\n      catalogId\n      predefined\n      version\n      catalogItemIds\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment WithToggleInsideCatalog_post on Post {\n  id\n  viewerEdge {\n    catalogsConnection {\n      catalogsContainingThis(type: LISTS) {\n        catalogId\n        __typename\n      }\n      predefinedContainingThis {\n        predefined\n        __typename\n      }\n      __typename\n    }\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment CreatorActionOverflowPopover_post on Post {\n  allowResponses\n  id\n  statusForCollection\n  isLocked\n  isPublished\n  clapCount\n  mediumUrl\n  pinnedAt\n  pinnedByCreatorAt\n  curationEligibleAt\n  mediumUrl\n  responseDistribution\n  visibility\n  ...useIsPinnedInContext_post\n  pendingCollection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    __typename\n  }\n  creator {\n    id\n    ...MutePopoverOptions_creator\n    ...auroraHooks_publisher\n    __typename\n  }\n  collection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    ...MutePopoverOptions_collection\n    ...auroraHooks_publisher\n    __typename\n  }\n  ...ClapMutation_post\n  ...NewsletterV3EmailToSubscribersMenuItem_post\n  __typename\n}\n\nfragment MutePopoverOptions_creator on User {\n  id\n  __typename\n}\n\nfragment MutePopoverOptions_collection on Collection {\n  id\n  __typename\n}\n\nfragment ClapMutation_post on Post {\n  __typename\n  id\n  clapCount\n  ...MultiVoteCount_post\n}\n\nfragment MultiVoteCount_post on Post {\n  id\n  ...PostVotersNetwork_post\n  __typename\n}\n\nfragment PostVotersNetwork_post on Post {\n  id\n  voterCount\n  recommenders {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment useIsPinnedInContext_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  pendingCollection {\n    id\n    __typename\n  }\n  pinnedAt\n  pinnedByCreatorAt\n  __typename\n}\n\nfragment auroraHooks_publisher on Publisher {\n  __typename\n  ... on Collection {\n    isAuroraEligible\n    isAuroraVisible\n    viewerEdge {\n      id\n      isEditor\n      __typename\n    }\n    __typename\n    id\n  }\n  ... on User {\n    isAuroraVisible\n    __typename\n    id\n  }\n}\n\nfragment NewsletterV3EmailToSubscribersMenuItem_post on Post {\n  id\n  creator {\n    id\n    newsletterV3 {\n      id\n      subscribersCount\n      __typename\n    }\n    __typename\n  }\n  isPublishToEmail\n  isNewsletter\n  __typename\n}\n\nfragment PostPresentationTracker_post on Post {\n  id\n  visibility\n  previewContent {\n    isFullContent\n    __typename\n  }\n  collection {\n    id\n    slug\n    __typename\n  }\n  __typename\n}\n\nfragment PostPreviewAvatar_post on Post {\n  __typename\n  id\n  collection {\n    id\n    name\n    ...CollectionAvatar_collection\n    __typename\n  }\n  creator {\n    id\n    username\n    name\n    ...UserAvatar_user\n    ...userUrl_user\n    __typename\n  }\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  mediumMemberAt\n  name\n  username\n  ...userUrl_user\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment HomeTrendingModule_post on Post {\n  id\n  ...HomeTrendingPostPreview_post\n  __typename\n}\n\nfragment HomeTrendingPostPreview_post on Post {\n  id\n  title\n  mediumUrl\n  readingTime\n  firstPublishedAt\n  ...PostPreviewAvatar_post\n  ...PostPresentationTracker_post\n  __typename\n}\n"},{"operationName":"ExtendedFeedQuery","variables":{"items":[{"postId":"9828331e55f2","topicId":""},{"postId":"d20f8a7136bf","topicId":""},{"postId":"b79a7a24016b","topicId":""},{"postId":"7f61c13afdd1","topicId":""},{"postId":"22e09fa01e04","topicId":""},{"postId":"f078272e9573","topicId":""},{"postId":"7dade155a942","topicId":""},{"postId":"646313a9220","topicId":""},{"postId":"9f6a47b2a677","topicId":""},{"postId":"47f3051ec352","topicId":""},{"postId":"9cb67d3752df","topicId":""},{"postId":"5f16873e53c3","topicId":""},{"postId":"751b2158e8e1","topicId":""},{"postId":"b3587c4a3eaa","topicId":""},{"postId":"d16f6bbaa9d7","topicId":""},{"postId":"a556c1571df4","topicId":""},{"postId":"2612369e0cc5","topicId":""},{"postId":"68961bb8c11e","topicId":""},{"postId":"96f24a8dc59b","topicId":""},{"postId":"8f3bb22371ba","topicId":""}]},"query":"query ExtendedFeedQuery($items: [ExtendedFeedItemOptions!]!) {\n  extendedFeedItems(items: $items) {\n    post {\n      ...PostListModulePostPreviewData\n      __typename\n    }\n    metadata {\n      topic {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PostListModulePostPreviewData on Post {\n  id\n  firstPublishedAt\n  readingTime\n  createdAt\n  mediumUrl\n  previewImage {\n    id\n    __typename\n  }\n  title\n  collection {\n    id\n    domain\n    slug\n    name\n    navItems {\n      url\n      __typename\n    }\n    logo {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    __typename\n  }\n  creator {\n    id\n    name\n    username\n    imageId\n    mediumMemberAt\n    ...userUrl_user\n    __typename\n  }\n  visibility\n  isProxyPost\n  isLocked\n  ...HomeFeedItem_post\n  ...HomeTrendingModule_post\n  __typename\n}\n\nfragment HomeFeedItem_post on Post {\n  __typename\n  id\n  title\n  firstPublishedAt\n  mediumUrl\n  collection {\n    id\n    name\n    domain\n    logo {\n      id\n      __typename\n    }\n    __typename\n  }\n  creator {\n    id\n    name\n    username\n    imageId\n    mediumMemberAt\n    __typename\n  }\n  previewImage {\n    id\n    __typename\n  }\n  previewContent {\n    subtitle\n    __typename\n  }\n  readingTime\n  tags {\n    ...TopicPill_tag\n    __typename\n  }\n  ...BookmarkButton_post\n  ...CreatorActionOverflowPopover_post\n  ...PostPresentationTracker_post\n  ...PostPreviewAvatar_post\n}\n\nfragment TopicPill_tag on Tag {\n  __typename\n  id\n  displayTitle\n}\n\nfragment BookmarkButton_post on Post {\n  visibility\n  ...SusiClickable_post\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment SusiContainer_post on Post {\n  id\n  __typename\n}\n\nfragment AddToCatalogBookmarkButton_post on Post {\n  ...AddToCatalogBase_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBase_post on Post {\n  id\n  viewerEdge {\n    catalogsConnection {\n      catalogsContainingThis(type: LISTS) {\n        catalogId\n        catalogItemIds\n        __typename\n      }\n      predefinedContainingThis {\n        catalogId\n        predefined\n        catalogItemIds\n        __typename\n      }\n      __typename\n    }\n    ...editCatalogItemsMutation_postViewerEdge\n    ...useAddItemToPredefinedCatalog_postViewerEdge\n    __typename\n    id\n  }\n  ...WithToggleInsideCatalog_post\n  __typename\n}\n\nfragment useAddItemToPredefinedCatalog_postViewerEdge on PostViewerEdge {\n  id\n  catalogsConnection {\n    predefinedContainingThis {\n      catalogId\n      version\n      predefined\n      catalogItemIds\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment editCatalogItemsMutation_postViewerEdge on PostViewerEdge {\n  id\n  catalogsConnection {\n    catalogsContainingThis(type: LISTS) {\n      catalogId\n      version\n      catalogItemIds\n      __typename\n    }\n    predefinedContainingThis {\n      catalogId\n      predefined\n      version\n      catalogItemIds\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment WithToggleInsideCatalog_post on Post {\n  id\n  viewerEdge {\n    catalogsConnection {\n      catalogsContainingThis(type: LISTS) {\n        catalogId\n        __typename\n      }\n      predefinedContainingThis {\n        predefined\n        __typename\n      }\n      __typename\n    }\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment CreatorActionOverflowPopover_post on Post {\n  allowResponses\n  id\n  statusForCollection\n  isLocked\n  isPublished\n  clapCount\n  mediumUrl\n  pinnedAt\n  pinnedByCreatorAt\n  curationEligibleAt\n  mediumUrl\n  responseDistribution\n  visibility\n  ...useIsPinnedInContext_post\n  pendingCollection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    __typename\n  }\n  creator {\n    id\n    ...MutePopoverOptions_creator\n    ...auroraHooks_publisher\n    __typename\n  }\n  collection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    ...MutePopoverOptions_collection\n    ...auroraHooks_publisher\n    __typename\n  }\n  ...ClapMutation_post\n  ...NewsletterV3EmailToSubscribersMenuItem_post\n  __typename\n}\n\nfragment MutePopoverOptions_creator on User {\n  id\n  __typename\n}\n\nfragment MutePopoverOptions_collection on Collection {\n  id\n  __typename\n}\n\nfragment ClapMutation_post on Post {\n  __typename\n  id\n  clapCount\n  ...MultiVoteCount_post\n}\n\nfragment MultiVoteCount_post on Post {\n  id\n  ...PostVotersNetwork_post\n  __typename\n}\n\nfragment PostVotersNetwork_post on Post {\n  id\n  voterCount\n  recommenders {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment useIsPinnedInContext_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  pendingCollection {\n    id\n    __typename\n  }\n  pinnedAt\n  pinnedByCreatorAt\n  __typename\n}\n\nfragment auroraHooks_publisher on Publisher {\n  __typename\n  ... on Collection {\n    isAuroraEligible\n    isAuroraVisible\n    viewerEdge {\n      id\n      isEditor\n      __typename\n    }\n    __typename\n    id\n  }\n  ... on User {\n    isAuroraVisible\n    __typename\n    id\n  }\n}\n\nfragment NewsletterV3EmailToSubscribersMenuItem_post on Post {\n  id\n  creator {\n    id\n    newsletterV3 {\n      id\n      subscribersCount\n      __typename\n    }\n    __typename\n  }\n  isPublishToEmail\n  isNewsletter\n  __typename\n}\n\nfragment PostPresentationTracker_post on Post {\n  id\n  visibility\n  previewContent {\n    isFullContent\n    __typename\n  }\n  collection {\n    id\n    slug\n    __typename\n  }\n  __typename\n}\n\nfragment PostPreviewAvatar_post on Post {\n  __typename\n  id\n  collection {\n    id\n    name\n    ...CollectionAvatar_collection\n    __typename\n  }\n  creator {\n    id\n    username\n    name\n    ...UserAvatar_user\n    ...userUrl_user\n    __typename\n  }\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  mediumMemberAt\n  name\n  username\n  ...userUrl_user\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment HomeTrendingModule_post on Post {\n  id\n  ...HomeTrendingPostPreview_post\n  __typename\n}\n\nfragment HomeTrendingPostPreview_post on Post {\n  id\n  title\n  mediumUrl\n  readingTime\n  firstPublishedAt\n  ...PostPreviewAvatar_post\n  ...PostPresentationTracker_post\n  __typename\n}\n"}
request = rq.Request(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36", 
                                   "content-type": "application/json"}, 
                     data=json.dumps(requestdata).encode("utf-8")) # 用json.dumps 轉換成字串string 的 utf-8編碼

# encode 通常是指把文字 (chars) 轉換成更原始的位元組 (bytes)，decode 則是反過來
# 通常是送出連線的時候要把文字轉成更原始的位元組，取得資料的時候要把原始的位元組轉回文字
# encode 是把字典轉換成字串(編碼)
# decode 是把字串轉換成字典(解碼)

with rq.urlopen(request) as responce:
    result = responce.read().decode("utf-8") # 字串格式
# print(result)
# print("\n====================\n")

# json.loads(字串) 或者是 json.load(可讀取的物件) 所以是不同的
# json.loads 和 json.dumps 是相對的
result = json.loads(result) # 用json 轉成字典格式
# print(result) # list # [{'data': {'extendedFeedItems': []}}, {'data': {'extendedFeedItems': [{......}]

for i in range(11):
    print(result[1]["data"]["extendedFeedItems"][i]["post"]["title"])


# In[282]:


import urllib.request as rq
import json

url = "https://medium.com/_/graphql"
requestdata = {"operationName":"WebRankedModulesScreen","variables":{},"query":"query WebRankedModulesScreen {\n  webRankedModules(\n    options: {recommendationSurface: MODULAR_WEB_HP, icelandVersion: ICELAND_GENERAL_RELEASE}\n  ) {\n    ... on Modules {\n      modules {\n        ...BasePostModuleData\n        ...RecentlyUpdatedModuleData\n        ...FollowedStoriesRankedModuleData\n        ...HomeFeedModuleData\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BasePostModuleData on BaseRankedModule {\n  metadata {\n    ...RankedModuleMetadataData\n    __typename\n  }\n  entities: items {\n    ... on ModuleItemPost {\n      __typename\n      post {\n        ...PostListModulePostPreviewData\n        __typename\n        id\n      }\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment RankedModuleMetadataData on RankedModuleMetadata {\n  type\n  feedId\n  sourceEncoding\n  __typename\n}\n\nfragment PostListModulePostPreviewData on Post {\n  id\n  firstPublishedAt\n  readingTime\n  createdAt\n  mediumUrl\n  previewImage {\n    id\n    __typename\n  }\n  title\n  collection {\n    id\n    domain\n    slug\n    name\n    navItems {\n      url\n      __typename\n    }\n    logo {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    __typename\n  }\n  creator {\n    id\n    name\n    username\n    imageId\n    mediumMemberAt\n    ...userUrl_user\n    __typename\n  }\n  visibility\n  isProxyPost\n  isLocked\n  ...HomeFeedItem_post\n  ...HomeTrendingModule_post\n  __typename\n}\n\nfragment HomeFeedItem_post on Post {\n  __typename\n  id\n  title\n  firstPublishedAt\n  mediumUrl\n  collection {\n    id\n    name\n    domain\n    logo {\n      id\n      __typename\n    }\n    __typename\n  }\n  creator {\n    id\n    name\n    username\n    imageId\n    mediumMemberAt\n    __typename\n  }\n  previewImage {\n    id\n    __typename\n  }\n  previewContent {\n    subtitle\n    __typename\n  }\n  readingTime\n  tags {\n    ...TopicPill_tag\n    __typename\n  }\n  ...BookmarkButton_post\n  ...CreatorActionOverflowPopover_post\n  ...PostPresentationTracker_post\n  ...PostPreviewAvatar_post\n}\n\nfragment TopicPill_tag on Tag {\n  __typename\n  id\n  displayTitle\n}\n\nfragment BookmarkButton_post on Post {\n  visibility\n  ...SusiClickable_post\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment SusiContainer_post on Post {\n  id\n  __typename\n}\n\nfragment AddToCatalogBookmarkButton_post on Post {\n  ...AddToCatalogBase_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBase_post on Post {\n  id\n  viewerEdge {\n    catalogsConnection {\n      catalogsContainingThis(type: LISTS) {\n        catalogId\n        catalogItemIds\n        __typename\n      }\n      predefinedContainingThis {\n        catalogId\n        predefined\n        catalogItemIds\n        __typename\n      }\n      __typename\n    }\n    ...editCatalogItemsMutation_postViewerEdge\n    ...useAddItemToPredefinedCatalog_postViewerEdge\n    __typename\n    id\n  }\n  ...WithToggleInsideCatalog_post\n  __typename\n}\n\nfragment useAddItemToPredefinedCatalog_postViewerEdge on PostViewerEdge {\n  id\n  catalogsConnection {\n    predefinedContainingThis {\n      catalogId\n      version\n      predefined\n      catalogItemIds\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment editCatalogItemsMutation_postViewerEdge on PostViewerEdge {\n  id\n  catalogsConnection {\n    catalogsContainingThis(type: LISTS) {\n      catalogId\n      version\n      catalogItemIds\n      __typename\n    }\n    predefinedContainingThis {\n      catalogId\n      predefined\n      version\n      catalogItemIds\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment WithToggleInsideCatalog_post on Post {\n  id\n  viewerEdge {\n    catalogsConnection {\n      catalogsContainingThis(type: LISTS) {\n        catalogId\n        __typename\n      }\n      predefinedContainingThis {\n        predefined\n        __typename\n      }\n      __typename\n    }\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment CreatorActionOverflowPopover_post on Post {\n  allowResponses\n  id\n  statusForCollection\n  isLocked\n  isPublished\n  clapCount\n  mediumUrl\n  pinnedAt\n  pinnedByCreatorAt\n  curationEligibleAt\n  mediumUrl\n  responseDistribution\n  visibility\n  ...useIsPinnedInContext_post\n  pendingCollection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    __typename\n  }\n  creator {\n    id\n    ...MutePopoverOptions_creator\n    ...auroraHooks_publisher\n    __typename\n  }\n  collection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    ...MutePopoverOptions_collection\n    ...auroraHooks_publisher\n    __typename\n  }\n  ...ClapMutation_post\n  ...NewsletterV3EmailToSubscribersMenuItem_post\n  __typename\n}\n\nfragment MutePopoverOptions_creator on User {\n  id\n  __typename\n}\n\nfragment MutePopoverOptions_collection on Collection {\n  id\n  __typename\n}\n\nfragment ClapMutation_post on Post {\n  __typename\n  id\n  clapCount\n  ...MultiVoteCount_post\n}\n\nfragment MultiVoteCount_post on Post {\n  id\n  ...PostVotersNetwork_post\n  __typename\n}\n\nfragment PostVotersNetwork_post on Post {\n  id\n  voterCount\n  recommenders {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment useIsPinnedInContext_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  pendingCollection {\n    id\n    __typename\n  }\n  pinnedAt\n  pinnedByCreatorAt\n  __typename\n}\n\nfragment auroraHooks_publisher on Publisher {\n  __typename\n  ... on Collection {\n    isAuroraEligible\n    isAuroraVisible\n    viewerEdge {\n      id\n      isEditor\n      __typename\n    }\n    __typename\n    id\n  }\n  ... on User {\n    isAuroraVisible\n    __typename\n    id\n  }\n}\n\nfragment NewsletterV3EmailToSubscribersMenuItem_post on Post {\n  id\n  creator {\n    id\n    newsletterV3 {\n      id\n      subscribersCount\n      __typename\n    }\n    __typename\n  }\n  isPublishToEmail\n  isNewsletter\n  __typename\n}\n\nfragment PostPresentationTracker_post on Post {\n  id\n  visibility\n  previewContent {\n    isFullContent\n    __typename\n  }\n  collection {\n    id\n    slug\n    __typename\n  }\n  __typename\n}\n\nfragment PostPreviewAvatar_post on Post {\n  __typename\n  id\n  collection {\n    id\n    name\n    ...CollectionAvatar_collection\n    __typename\n  }\n  creator {\n    id\n    username\n    name\n    ...UserAvatar_user\n    ...userUrl_user\n    __typename\n  }\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  mediumMemberAt\n  name\n  username\n  ...userUrl_user\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment HomeTrendingModule_post on Post {\n  id\n  ...HomeTrendingPostPreview_post\n  __typename\n}\n\nfragment HomeTrendingPostPreview_post on Post {\n  id\n  title\n  mediumUrl\n  readingTime\n  firstPublishedAt\n  ...PostPreviewAvatar_post\n  ...PostPresentationTracker_post\n  __typename\n}\n\nfragment RecentlyUpdatedModuleData on RecentlyUpdatedEntitiesRankedModule {\n  metadata {\n    ...RankedModuleMetadataData\n    __typename\n  }\n  items {\n    ...RecentlyUpdatedEntityData\n    __typename\n  }\n  __typename\n}\n\nfragment RecentlyUpdatedEntityData on RankedModuleUpdatedFollowedEntity {\n  entity {\n    __typename\n    ... on Collection {\n      id\n      name\n      avatar {\n        id\n        __typename\n      }\n      domain\n      slug\n      __typename\n    }\n    ... on User {\n      id\n      name\n      username\n      imageId\n      mediumMemberAt\n      ...userUrl_user\n      __typename\n    }\n  }\n  updatesCount\n  updatesCountText\n  __typename\n}\n\nfragment FollowedStoriesRankedModuleData on FollowedStoriesRankedModule {\n  metadata {\n    ...RankedModuleMetadataData\n    __typename\n  }\n  items {\n    ...FollowedStoryPreviewData\n    __typename\n  }\n  __typename\n}\n\nfragment FollowedStoryPreviewData on RankedModuleFollowedStoriesItem {\n  post {\n    __typename\n    id\n    title\n    readingTime\n    mediumUrl\n    firstPublishedAt\n    previewImage {\n      id\n      __typename\n    }\n    previewContent {\n      isFullContent\n      subtitle\n      __typename\n    }\n    creator {\n      id\n      name\n      imageId\n      mediumMemberAt\n      username\n      ...userUrl_user\n      __typename\n    }\n    collection {\n      id\n      name\n      avatar {\n        id\n        __typename\n      }\n      domain\n      slug\n      __typename\n    }\n    isProxyPost\n    visibility\n    isLocked\n    ...BookmarkButton_post\n    ...CreatorActionOverflowPopover_post\n  }\n  __typename\n}\n\nfragment HomeFeedModuleData on ExtendedFeedRankedModule {\n  metadata {\n    ...RankedModuleMetadataData\n    __typename\n  }\n  feedItems {\n    post {\n      ...PostListModulePostPreviewData\n      __typename\n    }\n    postId\n    metadata {\n      reason\n      postFeedReason\n      topicId\n      topic {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  extendedFeedItems {\n    postId\n    metadata {\n      reason\n      postFeedReason\n      topicId\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
request = rq.Request(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36", 
                                   "content-type": "application/json"}, 
                     data=json.dumps(requestdata).encode("utf-8"))

with rq.urlopen(request) as responce:
    result = responce.read().decode("utf-8")
# print(result)

result = json.loads(result)
# print(result)

for i in range(6):
    print(result["data"]["webRankedModules"]["modules"][1]["entities"][i]["post"]["title"])


# In[299]:


import urllib.request as rq
import json

url = "https://medium.com/_/graphql"
requestdata = {"operationName":"WebRankedModulesScreen","variables":{},"query":"query WebRankedModulesScreen {\n  webRankedModules(\n    options: {recommendationSurface: MODULAR_WEB_HP, icelandVersion: ICELAND_GENERAL_RELEASE}\n  ) {\n    ... on Modules {\n      modules {\n        ...BasePostModuleData\n        ...RecentlyUpdatedModuleData\n        ...FollowedStoriesRankedModuleData\n        ...HomeFeedModuleData\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BasePostModuleData on BaseRankedModule {\n  metadata {\n    ...RankedModuleMetadataData\n    __typename\n  }\n  entities: items {\n    ... on ModuleItemPost {\n      __typename\n      post {\n        ...PostListModulePostPreviewData\n        __typename\n        id\n      }\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment RankedModuleMetadataData on RankedModuleMetadata {\n  type\n  feedId\n  sourceEncoding\n  __typename\n}\n\nfragment PostListModulePostPreviewData on Post {\n  id\n  firstPublishedAt\n  readingTime\n  createdAt\n  mediumUrl\n  previewImage {\n    id\n    __typename\n  }\n  title\n  collection {\n    id\n    domain\n    slug\n    name\n    navItems {\n      url\n      __typename\n    }\n    logo {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    __typename\n  }\n  creator {\n    id\n    name\n    username\n    imageId\n    mediumMemberAt\n    ...userUrl_user\n    __typename\n  }\n  visibility\n  isProxyPost\n  isLocked\n  ...HomeFeedItem_post\n  ...HomeTrendingModule_post\n  __typename\n}\n\nfragment HomeFeedItem_post on Post {\n  __typename\n  id\n  title\n  firstPublishedAt\n  mediumUrl\n  collection {\n    id\n    name\n    domain\n    logo {\n      id\n      __typename\n    }\n    __typename\n  }\n  creator {\n    id\n    name\n    username\n    imageId\n    mediumMemberAt\n    __typename\n  }\n  previewImage {\n    id\n    __typename\n  }\n  previewContent {\n    subtitle\n    __typename\n  }\n  readingTime\n  tags {\n    ...TopicPill_tag\n    __typename\n  }\n  ...BookmarkButton_post\n  ...CreatorActionOverflowPopover_post\n  ...PostPresentationTracker_post\n  ...PostPreviewAvatar_post\n}\n\nfragment TopicPill_tag on Tag {\n  __typename\n  id\n  displayTitle\n}\n\nfragment BookmarkButton_post on Post {\n  visibility\n  ...SusiClickable_post\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment SusiContainer_post on Post {\n  id\n  __typename\n}\n\nfragment AddToCatalogBookmarkButton_post on Post {\n  ...AddToCatalogBase_post\n  __typename\n  id\n}\n\nfragment AddToCatalogBase_post on Post {\n  id\n  viewerEdge {\n    catalogsConnection {\n      catalogsContainingThis(type: LISTS) {\n        catalogId\n        catalogItemIds\n        __typename\n      }\n      predefinedContainingThis {\n        catalogId\n        predefined\n        catalogItemIds\n        __typename\n      }\n      __typename\n    }\n    ...editCatalogItemsMutation_postViewerEdge\n    ...useAddItemToPredefinedCatalog_postViewerEdge\n    __typename\n    id\n  }\n  ...WithToggleInsideCatalog_post\n  __typename\n}\n\nfragment useAddItemToPredefinedCatalog_postViewerEdge on PostViewerEdge {\n  id\n  catalogsConnection {\n    predefinedContainingThis {\n      catalogId\n      version\n      predefined\n      catalogItemIds\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment editCatalogItemsMutation_postViewerEdge on PostViewerEdge {\n  id\n  catalogsConnection {\n    catalogsContainingThis(type: LISTS) {\n      catalogId\n      version\n      catalogItemIds\n      __typename\n    }\n    predefinedContainingThis {\n      catalogId\n      predefined\n      version\n      catalogItemIds\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment WithToggleInsideCatalog_post on Post {\n  id\n  viewerEdge {\n    catalogsConnection {\n      catalogsContainingThis(type: LISTS) {\n        catalogId\n        __typename\n      }\n      predefinedContainingThis {\n        predefined\n        __typename\n      }\n      __typename\n    }\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment CreatorActionOverflowPopover_post on Post {\n  allowResponses\n  id\n  statusForCollection\n  isLocked\n  isPublished\n  clapCount\n  mediumUrl\n  pinnedAt\n  pinnedByCreatorAt\n  curationEligibleAt\n  mediumUrl\n  responseDistribution\n  visibility\n  ...useIsPinnedInContext_post\n  pendingCollection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    __typename\n  }\n  creator {\n    id\n    ...MutePopoverOptions_creator\n    ...auroraHooks_publisher\n    __typename\n  }\n  collection {\n    id\n    name\n    creator {\n      id\n      __typename\n    }\n    avatar {\n      id\n      __typename\n    }\n    domain\n    slug\n    ...MutePopoverOptions_collection\n    ...auroraHooks_publisher\n    __typename\n  }\n  ...ClapMutation_post\n  ...NewsletterV3EmailToSubscribersMenuItem_post\n  __typename\n}\n\nfragment MutePopoverOptions_creator on User {\n  id\n  __typename\n}\n\nfragment MutePopoverOptions_collection on Collection {\n  id\n  __typename\n}\n\nfragment ClapMutation_post on Post {\n  __typename\n  id\n  clapCount\n  ...MultiVoteCount_post\n}\n\nfragment MultiVoteCount_post on Post {\n  id\n  ...PostVotersNetwork_post\n  __typename\n}\n\nfragment PostVotersNetwork_post on Post {\n  id\n  voterCount\n  recommenders {\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment useIsPinnedInContext_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  pendingCollection {\n    id\n    __typename\n  }\n  pinnedAt\n  pinnedByCreatorAt\n  __typename\n}\n\nfragment auroraHooks_publisher on Publisher {\n  __typename\n  ... on Collection {\n    isAuroraEligible\n    isAuroraVisible\n    viewerEdge {\n      id\n      isEditor\n      __typename\n    }\n    __typename\n    id\n  }\n  ... on User {\n    isAuroraVisible\n    __typename\n    id\n  }\n}\n\nfragment NewsletterV3EmailToSubscribersMenuItem_post on Post {\n  id\n  creator {\n    id\n    newsletterV3 {\n      id\n      subscribersCount\n      __typename\n    }\n    __typename\n  }\n  isPublishToEmail\n  isNewsletter\n  __typename\n}\n\nfragment PostPresentationTracker_post on Post {\n  id\n  visibility\n  previewContent {\n    isFullContent\n    __typename\n  }\n  collection {\n    id\n    slug\n    __typename\n  }\n  __typename\n}\n\nfragment PostPreviewAvatar_post on Post {\n  __typename\n  id\n  collection {\n    id\n    name\n    ...CollectionAvatar_collection\n    __typename\n  }\n  creator {\n    id\n    username\n    name\n    ...UserAvatar_user\n    ...userUrl_user\n    __typename\n  }\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  mediumMemberAt\n  name\n  username\n  ...userUrl_user\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment HomeTrendingModule_post on Post {\n  id\n  ...HomeTrendingPostPreview_post\n  __typename\n}\n\nfragment HomeTrendingPostPreview_post on Post {\n  id\n  title\n  mediumUrl\n  readingTime\n  firstPublishedAt\n  ...PostPreviewAvatar_post\n  ...PostPresentationTracker_post\n  __typename\n}\n\nfragment RecentlyUpdatedModuleData on RecentlyUpdatedEntitiesRankedModule {\n  metadata {\n    ...RankedModuleMetadataData\n    __typename\n  }\n  items {\n    ...RecentlyUpdatedEntityData\n    __typename\n  }\n  __typename\n}\n\nfragment RecentlyUpdatedEntityData on RankedModuleUpdatedFollowedEntity {\n  entity {\n    __typename\n    ... on Collection {\n      id\n      name\n      avatar {\n        id\n        __typename\n      }\n      domain\n      slug\n      __typename\n    }\n    ... on User {\n      id\n      name\n      username\n      imageId\n      mediumMemberAt\n      ...userUrl_user\n      __typename\n    }\n  }\n  updatesCount\n  updatesCountText\n  __typename\n}\n\nfragment FollowedStoriesRankedModuleData on FollowedStoriesRankedModule {\n  metadata {\n    ...RankedModuleMetadataData\n    __typename\n  }\n  items {\n    ...FollowedStoryPreviewData\n    __typename\n  }\n  __typename\n}\n\nfragment FollowedStoryPreviewData on RankedModuleFollowedStoriesItem {\n  post {\n    __typename\n    id\n    title\n    readingTime\n    mediumUrl\n    firstPublishedAt\n    previewImage {\n      id\n      __typename\n    }\n    previewContent {\n      isFullContent\n      subtitle\n      __typename\n    }\n    creator {\n      id\n      name\n      imageId\n      mediumMemberAt\n      username\n      ...userUrl_user\n      __typename\n    }\n    collection {\n      id\n      name\n      avatar {\n        id\n        __typename\n      }\n      domain\n      slug\n      __typename\n    }\n    isProxyPost\n    visibility\n    isLocked\n    ...BookmarkButton_post\n    ...CreatorActionOverflowPopover_post\n  }\n  __typename\n}\n\nfragment HomeFeedModuleData on ExtendedFeedRankedModule {\n  metadata {\n    ...RankedModuleMetadataData\n    __typename\n  }\n  feedItems {\n    post {\n      ...PostListModulePostPreviewData\n      __typename\n    }\n    postId\n    metadata {\n      reason\n      postFeedReason\n      topicId\n      topic {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  extendedFeedItems {\n    postId\n    metadata {\n      reason\n      postFeedReason\n      topicId\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
request = rq.Request(url, headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36", 
                                   "content-type": "application/json"}, 
                      data=json.dumps(requestdata).encode("utf-8"))

with rq.urlopen(request) as responce:
    result = responce.read().decode("utf-8")
# print(result)

result = json.loads(result)
# print(result)

for i in range(5):
    print(result["data"]["webRankedModules"]["modules"][2]["feedItems"][i]["post"]["title"])

