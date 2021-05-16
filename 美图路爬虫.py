import requests
import re
import os
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

headers = { 'Referer': 'http://www.meitulu.cn/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
                'Accept': 'image/webp,*/*',
                'DNT': '1',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate'
            }


#解析网页图片地址—————————————————————————————————————————————————————————————————————————————————————————————————————————————————
def get_Picture_Url(page_Url, headers = headers):

    
    # 请求图片网页
    response = requests.get(url=page_Url,headers = headers) 
    response.encoding='utf-8'
    response = response.text
    
    # 结构化超文本
    tree = etree.HTML(response)

    # 获取图片源地址
    picture_url = tree.xpath('///div[@class="content"]/center/a/img/@src')
    return picture_url[0]


#获取图集信息——————————————————————————————————————————————————————————————————————————————————————————————————————————————
def get_Picture_Info(page_Url, headers = headers):

    picture_Info = []

    # 请求图集首张页面的网页
    response = requests.get(url=page_Url,headers = headers) 
    response.encoding='utf-8'
    response = response.text
    
    # 结构化超文本
    tree = etree.HTML(response)

    # 获取图集张数
    ex = '图片数量： (.*?)张'
    pictures_Num = int(re.findall(ex,response,re.S)[0])
    picture_Info.append(pictures_Num)

    #获取图集名称
    picture_Title = tree.xpath('///div[@class="weizhi"]/h1/text()')[0]
    picture_Info.append(picture_Title)

    #获取图片地址
    picture_Info.append(get_Picture_Url(page_Url))
    page_Url_Head = page_Url[:-5] + "_"
    for i in range(pictures_Num - 1):
        n = str(i+2)
        page_Url_Step = page_Url_Head + n + ".html"
        picture_Info.append(get_Picture_Url(page_Url_Step))

    return picture_Info


#下载图集—————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
def download_Picture(*pic):

    path = "./青年大学习/"+ pic[1]
    path = path.strip()
    if not os.path.exists(path):
        os.makedirs(path)
    for num in range(pic[0]):
        picture_url = pic[num + 2]
        img_path = path+'/'+str(num+1)+".jpg"
        img_data = requests.get(url=picture_url,headers=headers).content
        with open(img_path,'wb') as fp:
            fp.write(img_data)
            print(img_path,'下载成功')


#获取各种图集分类列表——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
def get_Pic_Class(home_Page = "http://www.meitulu.cn/"):

     # 请求图片网页
    response = requests.get(url=home_Page,headers = headers) 
    response.encoding='utf-8'
    response = response.text
    
    # 结构化超文本
    tree = etree.HTML(response)

    # 获取图片源地址
    picture_Class = {}
    picture_Class_Url = tree.xpath('//*[@id="tag_ul"]/li/a/@href')
    picture_Class_Name = tree.xpath('//*[@id="tag_ul"]/li/a/text()')
    for num in range(len(picture_Class_Url)):
        picture_Class[picture_Class_Name[num]] = "http://www.meitulu.cn/" + picture_Class_Url[num]
    return picture_Class

#获取该类型页面数量——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
def get_Every_Page(class_Home_Page):

    for i in range (100):
        #遍历请求网页
        next_Page = class_Home_Page + 'index_' + str(i+2) + ".html"
        response = requests.get(url=next_Page,headers = headers) 
        # print(type(response.status_code))
        if response.status_code == 404:
            return i+1

#获取图集url列表———————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
def get_Pictures_Url(class_Home_Page):

    page_Num = get_Every_Page(class_Home_Page)

    pictures_List = []

    # 请求网页
    response = requests.get(url=class_Home_Page,headers = headers) 
    response.encoding='utf-8'
    response = response.text

    # 结构化超文本
    tree = etree.HTML(response)

    #获取图集列表
    pictures_Url = tree.xpath('/html/body/div[2]/div[3]/ul/li/a/@href')


    for i in pictures_Url:
        pictures_List.append(i)
    for num in range (page_Num):
        next_Url = class_Home_Page + 'index_'+ str(num+2) + ".html"

        # 请求网页
        response = requests.get(url=next_Url,headers = headers) 
        response.encoding='utf-8'
        response = response.text
       
        # 结构化超文本
        tree = etree.HTML(response)

        #获取图集列表
        pictures_Url = tree.xpath('/html/body/div[2]/div[3]/ul/li/a/@href')
        for j in pictures_Url:
            pictures_List.append(j)
    
    return pictures_List




if __name__ == '__main__':


    title = "请选择你的英雄"
    picture_Class = get_Pic_Class()
    for key in picture_Class.keys():
        print(key)
    your_Choice = input(title.center(50))

    class_Home_Page = picture_Class[your_Choice]

    pictures_List = get_Pictures_Url(class_Home_Page)

    with ThreadPoolExecutor(100) as t:
        for i in pictures_List:
            t.submit(download_Picture, *(get_Picture_Info("http://www.meitulu.cn/" + i)))
    