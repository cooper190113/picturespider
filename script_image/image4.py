import requests
from lxml import etree
import os
import time


# 设计模式 --》面向对象编程 https://www.cnblogs.com/girliswater/p/11152942.html
class Spider(object):
    def __init__(self):
        # 反反爬虫措施，加请求头部信息
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36",
            "Referer": "https://www.mzitu.com/"
        }
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.path = self.dir_path + "/image"
        is_exists = os.path.exists(self.dir_path + "/image")
        if not is_exists:
            os.makedirs(self.path)

    def start_request(self):
        # 1. 获取整体网页的数据 requests
        for i in range(1, 204):
            print("==========正在抓取%s页==========" % i)
            response = requests.get("https://www.mzitu.com/page/" + str(i) + "/", headers=self.headers)
            time.sleep(3)
            html = etree.HTML(response.content.decode())
            self.xpath_data(html)

    def xpath_data(self, html):
        # 2. 抽取想要的数据 标题 图片 xpath
        src_list = html.xpath('//ul[@id="pins"]/li/a/img/@data-original')
        alt_list = html.xpath('//ul[@id="pins"]/li/a/img/@alt')
        for src, alt in zip(src_list, alt_list):
            file_name = self.path + "/" + alt + ".jpg"
            response = requests.get(src, headers=self.headers)
            time.sleep(3)
            print("正在抓取图片：" + file_name)
            # 3. 存储数据 jpg with open
            try:
                with open(file_name, "wb") as f:
                    f.write(response.content)
            except:
                print("==========文件名有误！==========")


spider = Spider()
spider.start_request()