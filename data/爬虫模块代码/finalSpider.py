import datetime
import json
import random
import re
import time

import requests
from retrying import retry


class weiboSpider():
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        self.cookie = "Cookie: SINAGLOBAL=3758414542611.39.1590823246637; un=15233161074; wvr=6; SCF=Apt0VTIzlj2iyFXgoldfvIBWJX_3-OLu-l7juL0_yrNMMXoqfx_owF3xicdIxkTMHFGxy65UN4P8K_3UB75YPC8.; SUHB=08J72jVhU3X2-l; ALF=1593747762; SUB=_2A25z02xiDeRhGeBI7FEU9y7Pzj6IHXVRPHQqrDV8PUJbkNANLWjukW1NRmIHxzVs5SiUyAXDhqxzOioAF6qGl73d; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhaV0QwpA..78YljNqxHT6R5JpX5oz75NHD95QcSoM0SKM7e0-EWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSoqNe0-Nehefentt; UOR=,,www.baidu.com; Ugrow-G0=6fd5dedc9d0f894fec342d051b79679e; YF-V5-G0=f5a079faba115a1547149ae0d48383dc; _s_tentry=www.baidu.com; Apache=3166665788267.38.1591687013125; ULV=1591687013136:9:8:4:3166665788267.38.1591687013125:1591583430221; wb_view_log_6673570352=1536*8641.375; YF-Page-G0=761bd8cde5c9cef594414e10263abf81|1591687210|1591687010; webim_unReadCount=%7B%22time%22%3A1591687213047%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A38%2C%22msgbox%22%3A0%7D"
        self.cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in self.cookie.split(";")}

    def get_url_list(self):
        """获取url列表"""
        with open("news_href.txt", "r", encoding="utf-8")as f:
            url_list = f.readlines()
        return url_list

    @retry(stop_max_attempt_number=5)
    def __parse_url(self, url):
        """解析url，获取html字符串"""
        response = requests.get(url, headers=self.headers, cookies=self.cookie_dict, timeout=3)
        html_str = response.content.decode()
        return (html_str)

    def parse_url(self, url):
        """解析url时的异常处理"""
        try:
            html_str = self.__parse_url(url)
        except:
            html_str = None
        return html_str

    def get_content_list(self, html_str, url):
        """获取发布者，标题，发表时间，内容以及评论"""
        if html_str != None:
            content_list = []
            id = url[-17:].replace("\n", "")
            item = {}
            # 获取新闻平台
            item["screen_name"] = re.compile(r'"screen_name": "(.*?)"').findall(html_str)
            item["screen_name"] = item["screen_name"][0] if len(item["screen_name"]) > 0 else None
            # 获取新闻标题
            item["title"] = re.compile(r'"title": "(.*?)"').findall(html_str)
            item["title"] = item["title"][0] if len(item["title"]) > 0 else None
            # 获取新闻事件
            date = re.compile(r'"created_at": "(.*?)"').findall(html_str)
            date = date[0].split(" +")[0][0:-9] if len(date) > 0 else None
            date_format = datetime.datetime.strptime(date, '%a %b %d')
            time = datetime.datetime.strftime(date_format, '%m-%d')
            item["time"] = "2020-" + time
            # 获取新闻文章
            mix_text = re.compile(r'"text": "(.*)"').findall(html_str)  # 获取script中的text标签的所有内容
            mix_text = mix_text[0] if len(mix_text) > 0 else None  # 获取到混合文本，里面有a标签和文本数据
            stop_text_list = re.compile(r'<a .*?</a>').findall(mix_text)
            for stop_text in stop_text_list:
                mix_text = mix_text.replace(stop_text, "")
            item["text"] = mix_text if len(mix_text) > 0 else None
            item["comment"] = self.get_comment_list(id)
            content_list.append(item)
            # print(content_list)
            return content_list
        else:
            return None

    def get_comment_list(self, id):
        """获取评论列表和下一页评论的max_id"""
        temp = 0
        max_id = ""
        while temp <= 5:
            if max_id == "":
                url = "https://m.weibo.cn/comments/hotflow?id=" + str(id) + "&mid=" + str(id) + "&max_id_type=0"
            elif max_id == 0:
                break
            else:
                url = "https://m.weibo.cn/comments/hotflow?id=" + str(id) + "&mid=" + str(id) + "&max_id=" + str(
                    max_id) + "&max_id_type=0"
            # print(url)
            # 发送请求，获取响应
            html_str = self.parse_url(url)
            # print(html_str)
            dict_data = json.loads(html_str)
            if dict_data['ok'] == 0:
                return None
            max_id = dict_data["data"]["max_id"]
            comment_list = []
            for comment_data in dict_data["data"]["data"]:
                data = comment_data["text"]
                p = re.compile(r'(<span.*>.*</span>)*(<a.*>.*</ a>)?')
                data = p.sub(r'', data)
                if len(data) != 0:
                    comment_list.append(data)
            time.sleep(10)
            temp += 1
        return comment_list

    def sava_content_list(self, content_list):
        """保存数据"""
        with open("content.txt", "a", encoding="utf-8")as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")
        print("保存成功！", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def run(self):
        # 1.获取URL
        url_list = self.get_url_list()
        for url in url_list:
            print(url)
            # 2.发送请求，获取响应
            html_str = self.parse_url(url)
            # print(html_str)
            # 3.获取数据
            content_list = self.get_content_list(html_str, url)
            if content_list != None:
                # 4.保存数据
                self.sava_content_list(content_list)
            else:
                continue
            time.sleep(random.random() * 10)


if __name__ == '__main__':
    spider = weiboSpider()
    spider.run()
