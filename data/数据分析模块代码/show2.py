#核密度图
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] =False

# Pandas模块绘制直方图和核密度图
# 读入数据
Titanic = pd.read_csv('C:/Users/Administrator/Desktop/数据处理结果/数据爬取/特朗普终止与世界卫生组织合作/two.csv', encoding='gb18030')
# 绘制直方图
Titanic.comment.plot(kind = 'hist', bins = 10, color = 'steelblue', edgecolor = 'black', normed = True, label = '直方图')
# 绘制核密度图
Titanic.comment.plot(kind = 'kde', color = 'red', label = '核密度图')
# 添加x轴和y轴标签
plt.xlabel('情感分值')
plt.ylabel('核密度值')
# 添加标题
plt.title('情感分析分值分布')
# 显示图例
plt.legend()
# 显示图形
plt.show()