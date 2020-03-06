import requests
from lxml import etree
import os
import time

page_url = 'https://www.mzitu.com/'

# 反爬虫措施，加请求头部信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/81.0.4044.9 Safari/537.36",
    "Referer": page_url
}

# pictures_path = os.path.join(os.getcwd(), 'pictures/')
pictures_path = os.path.dirname(os.path.abspath(__file__)) + "/pictures"


class Spider(object):
    def __init__(self, page_num):
        self.page_num = page_num
        self.page_urls = dict() # {}

    def get_page_urls(self):
        """
        获取所有导航页面url
            :return:
        """
        selector = self.get_request_content(page_url)
        page_footer_names = selector.xpath('//div[@class="footer"]/a/text()')
        page_footer_urls = selector.xpath('//div[@class="footer"]/a/@href')
        for footer_name, footer_url in zip(page_footer_names, page_footer_urls):
            self.page_urls[footer_name] = footer_url

    def get_request_content(self, url):
        response = requests.get(url, headers=headers)
        time.sleep(3)
        return etree.HTML(response.content.decode())

    def get_pic_url(self):
        """
        下载所有导航页面分页数据
            :return:
        """
        for key, value in self.page_urls.items():
            pictures_category_path = pictures_path + "/" + key
            is_exists = os.path.exists(pictures_category_path)
            if not is_exists:
                os.makedirs(pictures_category_path)

            for i in self.page_num:
                selector = self.get_request_content(value + "page/" + str(i) + "/");
                self.xpath_data(selector, pictures_category_path)

    def xpath_data(self, html, path):
        # 1. 抽取想要的数据 标题、图片 xpath
        src_list = html.xpath('//ul[@id="pins"]/li/a/img/@data-original')
        alt_list = html.xpath('//ul[@id="pins"]/li/a/img/@alt')
        for src, alt in zip(src_list, alt_list):
            file_name = path + "/" + alt + ".jpg"
            response = requests.get(src, headers=headers)
            time.sleep(3)
            print("正在抓取图片：" + file_name)
            # 2. 存储数据 jpg with open
            try:
                with open(file_name, "wb") as f:
                    f.write(response.content)
            except Exception as ex:
                print("==========文件名有误！==========" + ex)


if __name__ == '__main__':
    page_num = input("请输入页码:")
    spider = Spider(page_num)
    spider.get_page_urls()
    spider.get_pic_url()
