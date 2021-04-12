def get_picture(page_url):
    response = requests.get(url=page_url,headers = headers) #   请求图集页面的网页
    response.encoding='utf-8'
    response = response.text
    # print(response)
    tree = etree.HTML(response)

    # 以下3行获取图集张数
    ex = '图片数量：(.*?) 张'
    pictures_num = int(re.findall(ex,response,re.S)[0])

    #获取图集名称
    picture_title = tree.xpath('///div[@class="weizhi"]/h1/text()')[0]

    #   以下3行均为拼凑图片源地址
    picture_url = tree.xpath('///div[@class="content"]/center/img/@src')
    picture_section_url = picture_url[0].split('/',6)
    picture_pre_url = picture_section_url[0]+"//"+picture_section_url[2]+'/'+picture_section_url[3]+'/'+picture_section_url[4]+'/'+picture_section_url[5]+'/'
    
    path = "./青年大学习/"+picture_title
    path = path.strip()
    if not os.path.exists(path):
        os.makedirs(path)
    for num in range(pictures_num):
        picture_url = picture_pre_url + str(num+1)+".jpg"
        img_path = path+'/'+str(num+1)+".jpg"
        img_data = requests.get(url=picture_url,headers=headers).content
        with open(img_path,'wb') as fp:
            fp.write(img_data)
            print(img_path,'下载成功')
import requests
import re
import os
from lxml import etree
headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
style_url_list = ['https://www.meitulu.com/t/nvshen/','https://www.meitulu.com/t/wangluohongren/','https://www.meitulu.com/t/youwu/',
                  'https://www.meitulu.com/t/youhuo/','https://www.meitulu.com/t/changtui/','https://www.meitulu.com/t/keai/',
                  'https://www.meitulu.com/t/qingchun/','https://www.meitulu.com/t/jipin/','https://www.meitulu.com/t/fengsuniang/',
                  'https://www.meitulu.com/t/baoru/','https://www.meitulu.com/t/meixiong/','https://www.meitulu.com/t/mengmeizi/',
                  'https://www.meitulu.com/t/huwai/','https://www.meitulu.com/t/weimei/','https://www.meitulu.com/t/nenmo/',
                  'https://www.meitulu.com/t/qizhi/','https://www.meitulu.com/t/xinggan/','https://www.meitulu.com/t/shaofu/',
                  'https://www.meitulu.com/t/loli/','https://www.meitulu.com/t/bijini/','https://www.meitulu.com/t/qingxin/',
                  'https://www.meitulu.com/rihan/','https://www.meitulu.com/guochan/']
print("1.女神\t2.网络红人\t3.尤物\t4.诱惑\t5.长腿\t6.可爱\t7.清纯\t8.极品\t9.风俗娘\t10.爆乳\n\n11.美胸\t12.萌妹子\t13.户外\t14.唯美\t15.嫩模\t16.气质\t17.性感\t18.少妇\t19.萝莉\t20.比基尼\n\n21.清新\t22.日韩\t23.国产")
print('----------------------------------------Powered by Hunger----------------------------------')
choice = input("请输入你要学习的科目")
style_url = style_url_list[int(choice)-1]
flag = "y"
backdoor = input('是否确定（数字1确定，数字0重新选择）')
if int(backdoor)>1:
    n = int(backdoor)
    while flag=="y":
        style_url = style_url + str(n)+".html"
        response = requests.get(url=style_url,headers = headers)
        response.encoding='utf-8'
        response = response.text
        tree = etree.HTML(response)
        pictures_list_url = tree.xpath('////ul[@class="img"]/li/a/@href')#  以列表形式获取图片集地址
        for pictureres_url in pictures_list_url:
            get_picture(pictureres_url)
        flag = input('是否继续\ty.继续\tn.退出')
        n+=1
elif int(backdoor)==0:
    choice = input("请输入你要学习的科目")
    style_url = style_url_list[int(choice)-1]
else:
    pass
n = 2
while flag=="y":
    response = requests.get(url=style_url,headers = headers)
    response.encoding='utf-8'
    response = response.text
    tree = etree.HTML(response)
    pictures_list_url = tree.xpath('////ul[@class="img"]/li/a/@href')#  以列表形式获取图片集地址
    for pictureres_url in pictures_list_url:
        get_picture(pictureres_url)
    flag = input('是否继续\ty.继续\tn.退出')
    style_url = style_url + str(n)+".html"
    n+=1
