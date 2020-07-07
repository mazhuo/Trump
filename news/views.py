from django.db import transaction
from django.shortcuts import render
from dateutil.parser import parse

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from news.models import NewsPiece, Tag, ContentTag,Student,news_test,trump1
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
import jieba
import datetime
import copy
import math
import operator
import time
import xlrd
from collections import Counter

from PIL import Image
import numpy as  np
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
#需要对中文进行处理
import matplotlib.font_manager as fm
from os import path

def index(request):
    news_list = trump1.objects.all()
    paginator = Paginator(news_list, 10)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'news/newslist.html', {'news_title_list': news, 'news_sum': len(trump1.objects.all())})

def detail(request,news_id):
    #news = trump1.objects.get(pk = 2)
    news_list = trump1.objects.get(pk = news_id)
    print(news_list.news_id)
    wordcloud(news_list.news_comment)
    return render(request, 'news/detail.html', {'news_list':news_list})


def search(request):
    str = request.GET['tag']
    news_list = trump1.objects.filter(news_title__contains= str)
    paginator = Paginator(news_list, 10)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'news/tag.html', {'news_title_list': news, 'tag': str})


def add(request):

    DataTable = trump1()
    """导入excel表数据"""
    excel_file = 'data.xlsx' # 获取前端上传的文件
    file_type = 'xlsx'  # 拿到文件后缀

    if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
        # 打开工作文件
        filename="E:\TencentFile\data.xlsx"
        data = xlrd.open_workbook(filename)
        tables = data.sheets()  # 得到excel中数据表sheets1，sheets2...
        # 循环获取每个数据表中的数据并写入数据库
        for table in tables:
            rows = table.nrows  # 总行数
            try:
                # 控制数据库事务交易
                with transaction.atomic():
                    # 获取数据表中的每一行数据写入设计好的数据库表
                    for row in range(1, rows):  # 从1开始是为了去掉表头

                        row_values = table.row_values(row)  # 每一行的数据
                        DataTable.news_id=int(row_values[0])
                        DataTable.news_title=row_values[1]
                        DataTable.news_date=str(int(row_values[2]))
                        DataTable.news_content=row_values[3]
                        DataTable.news_emotion=row_values[4]
                        DataTable.news_comment=row_values[5]

                        DataTable.save()
                        print(row)
            except:
                return HttpResponse('解析excel文件或者数据插入错误！')
        return HttpResponse('已添加')
    else:
        return HttpResponse('上传文件类型错误！')




def wordcloud(text):
    # 背景图
    bg = np.array(Image.open("E:\TencentFile\data.png"))

    # 获取当前的项目文件加的路径
    d = path.dirname(__file__)
    # 读取停用词表
    stopwords_path = 'E:\TencentFile\stopwords.txt'
    # 添加需要自定以的分词
    # jieba.add_word("叶文洁")

    # 读取要分析的文本
    text_path = "ciyun.txt"
    # 读取要分析的文本，读取格式


    # 定义个函数式用于分词
    def jiebaclearText(text):
        # 定义一个空的列表，将去除的停用词的分词保存
        mywordList = []
        # 进行分词
        seg_list = jieba.cut(text, cut_all=False)
        # 将一个generator的内容用/连接
        listStr = '/'.join(seg_list)
        # 打开停用词表
        f_stop = open(stopwords_path, encoding="utf8")
        # 读取
        try:
            f_stop_text = f_stop.read()
        finally:
            f_stop.close()  # 关闭资源
        # 将停用词格式化，用\n分开，返回一个列表
        f_stop_seg_list = f_stop_text.split("\n")
        # 对默认模式分词的进行遍历，去除停用词
        for myword in listStr.split('/'):
            # 去除停用词
            if not (myword.split()) in f_stop_seg_list and len(myword.strip()) > 1:
                mywordList.append(myword)
        return ' '.join(mywordList)

    text1 = jiebaclearText(text)
    # 生成
    wc = WordCloud(
        background_color="white",  # 设置背景为白色，默认为黑色
        width=990,  # 设置图片的宽度
        height=440,  # 设置图片的高度
        margin=10,  # 设置图片的边缘

        max_font_size=100,
        random_state=30,
        font_path='C:/Windows/Fonts/simkai.ttf'  # 中文处理，用系统自带的字体
    ).generate(text1)
    # 为图片设置字体
    my_font = fm.FontProperties(fname='C:/Windows/Fonts/simkai.ttf')
    # 产生背景图片，基于彩色图像的颜色生成器
    image_colors = ImageColorGenerator(bg)
    # 开始画图
    plt.imshow(wc)
    # 为云图去掉坐标轴
    plt.axis("off")
    # 画云图，显示
    # 保存云图
    wc.to_file("E:\研究生\研1\课-信息检索与搜索引擎\Trump\static\images\data1.png")


def data(request):
    return render(request,'news/test.html')