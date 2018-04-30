# -*- coding: UTF-8 -*-
'''
@author: 'FenG_Vnc'
@date: 2018/4/30 21:04
@file: $NAME.py
'''
from __future__ import unicode_literals

import json
import re

import requests
from lxml import etree


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"
}

def single_html():

    response = requests.get("https://www.ithome.com/blog",headers=headers)
    # print(response.content)
    contents = etree.HTML(response.content)
    pages = contents.xpath("//ul[@class='ulcl']//li[4]/a[1]//@href")[0]
    return pages


def news_html(url):
    response = requests.get(url,headers=headers)

    contents = etree.HTML(response.content)
    title = contents.xpath("//div[@class='post_title']//h1//text()")[0]
    descrptioin = contents.xpath("//meta[@name='description']//@content")[0]
    pub_time = contents.xpath("//span[@id='pubtime_baidu']//text()")[0]
    source = contents.xpath("//span[@id='source_baidu']//a//text()")[0]
    author = contents.xpath("//span[@id='author_baidu']//strong//text()")[0]
    editor = contents.xpath("//span[@id='editor_baidu']//strong//text()")[0]
    commentcount = get_news_id(url)
    # soce = get_news_grade(url)
    result = {
        'url':url,
        "descrptioin":descrptioin,
        'title':title,
        'pub_time':pub_time,
        'source':source,
        'author':author,
        'editor':editor,
        'commentcount':commentcount
    }
    return result


def get_news_id(url):
    id = re.findall('\d+',url)[0]
    id_url = 'https://dyn.ithome.com/api/comment/count'
    request = requests.get(id_url,params={"newsid":id},headers=headers)
    id = re.findall("\d+",request.content)[0]
    return id


# def get_news_grade(url): #TODO 评分需要研究JS请求获取
#     response = requests.get(url,headers=headers).content
#     content = etree.HTML(response)
#     soce = content.xpath("//span[@class='ss']//text()")
#     print(soce)


if __name__ == '__main__':
    news_url = single_html()
    data = news_html(news_url)
    for k,v in data.items():
        print k,v



