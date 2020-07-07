import json
import random
import time

import requests
from retrying import retry


class getNewsHref:
    def __init__(self):
        self.temp_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D%E7%89%B9%E6%9C%97%E6%99%AE%E7%96%AB%E6%83%85%26t%3D0&page_type=searchall&page={}"
        self.data = "append=list-home&paged=20&action=ajax_load_posts&query=&page=home"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "Referer": "https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E7%89%B9%E6%9C%97%E6%99%AE%E7%96%AB%E6%83%85"}

    def get_url_list(self):
        """获取url列表"""
        url_list = [self.temp_url.format(i) for i in range(1, 200)] 
        return url_list

    @retry(stop_max_attempt_number=5)
    def __parse_url(self, url):
        """解析url，输出json字符串"""
        response = requests.get(url, headers=self.headers, data=self.data, timeout=3)
        json_str = response.content.decode()
        return json_str

    def parse_url(self, url):
        """字符串解析时的异常处理"""
        try:
            json_str = self.__parse_url(url)
        except:
            json_str = None
        return json_str

    def get_href_list(self, json_str):
        """解析json字符串，获取微博的id，构建带有评论的微博的url"""
        dict_data = json.loads(json_str)
        content_list = dict_data["data"]["cards"]
        href_list = []
        for content in content_list:
            content = content["mblog"]["id"]
            content = "https://m.weibo.cn/status/" + content
            href_list.append(content)
        return href_list

    def sava_href_list(self, href_list):
        """保存满足条件的微博url"""
        with open("news_href.txt", "a", encoding="utf-8")as f:
            for href in href_list:
                f.write(href+"\n")
                print("保存成功！")

    def run(self):
        # 1.获取URL
        url_list = self.get_url_list()
        for url in url_list:
            # 2.发送请求，获取响应
            html_str = self.parse_url(url)
            # 3.获取数据
            href_list = self.get_href_list(html_str)
            #  4.保存
            self.sava_href_list(href_list)
            time.sleep(random.random() * 10)


if __name__ == '__main__':
    getHref = getNewsHref()
    getHref.run()
