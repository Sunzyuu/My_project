import scrapy
import re
import os
import urllib
import sys
import urllib.request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request
from words.items import WordsItem

class WebWordSpider(scrapy.Spider):
    name = 'web_word'
    allowed_domains = ['word.iciba.com/']

    # class 是四级必备单词，这里可以根据需要选择不同的单词表
    first_url = "http://word.iciba.com/?action=words&class=11&course={}"
    start_urls = []

    # 生成爬取需要的url地址池
    # 可以根据需要修改nums，控制爬取的单词数
    nums = 11
    for page in range(1,nums):
        start_urls.append(first_url.format(page))
    print(start_urls)

    def parse(self, response):
        se = Selector(response)
        # 先判断页面中是否存在单词
        src = se.xpath("//div[@class='word_main']/ul/li")
        # 提取出url中的页数
        page = re.findall(r"course=\d+", response.url)[0]
        print("===" * 10 + "正在爬取第"+page[7:]+"页"+"===" * 10)
        if len(src) > 0:
            # 将单词的信息提取出来，word是一个数组，存放的是页面中的所有单词
            word = se.xpath("//li/div[@class='word_main_list_w']/span/@title" ).extract()  # 提取节点信息
            soundmark = se.xpath("//li/div[@class='word_main_list_y']/strong/text()" ).extract()
            url = se.xpath("//li/div[@class='word_main_list_y']/a/@id" ).extract()
            translation = se.xpath("//li/div[@class='word_main_list_s']/span/@title" ).extract()

            # 因为上一步提出的音标存在制表符，这里就用正则提取出正确的音标
            for i in range(0,len(word)):
                sm = re.findall(r"\[.*?\]",soundmark[i])
                soundmark[i] = sm[0]

            for i in range(0,len(word)):
                file_name = u"%s.mp3" % word[i]         # 用单词给mp3文件命名
                path = os.path.join("D:\Sunzh\word\cet4", file_name)  # mp3保存的路径
                urllib.request.urlretrieve(url[i], path)    # 下载该mp3文件
                item = WordsItem()
                item['word'] = word[i]
                item['soundmark'] = soundmark[i]
                item['url'] = url[i]
                item['translation'] = translation[i]
                # print(item)
                # 将item发给管道处理，在管道中写入数据库和josn文件
                yield item
