
#直方图

import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] =False

# matplotlib模块绘制直方图
# 读入数据
Titanic = pd.read_csv('C:/Users/Administrator/Desktop/数据处理结果/数据爬取/特朗普终止与世界卫生组织合作/two.csv', encoding='gb18030')
# 检查年龄是否有缺失
any(Titanic.trend.isnull())
# 不妨删除含有缺失年龄的观察
Titanic.dropna(subset=['trend'], inplace=True)
# 绘制直方图
plt.hist(x = Titanic.trend, # 指定绘图数据
        bins = 5, # 指定直方图中条块的个数
          color = 'steelblue', # 指定直方图的填充色
          edgecolor = 'black' # 指定直方图的边框色
         )
# 添加x轴和y轴标签
plt.xlabel('情感分值')
plt.ylabel('频数')
# 添加标题
plt.title('情感分布直方图')
# 显示图形
plt.show()
