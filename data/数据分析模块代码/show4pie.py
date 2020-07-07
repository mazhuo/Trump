#饼状图
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] =False

def draw_pie(labels, quants):
    # make a square figure
    plt.figure(1, figsize=(6, 6))
    # For China, make the piece explode a bit
    expl = [0, 0.1, 0]  # 第二块即China离开圆心0.1
    # Colors used. Recycle if not enough.
    colors = ["blue", "red",  "green"]  # 设置颜色（循环显示）
    # Pie Plot
    # autopct: format of "percent" string;百分数格式
    plt.pie(quants, explode=expl, colors=colors, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=True)
    plt.title('情绪分布图', bbox={'facecolor': '0.8', 'pad': 5})
    plt.show()
    plt.savefig("pie.jpg")
    plt.close()


# quants: GDP

# labels: country name

labels = ['Positive', 'Negative', 'Neutral']

quants = [861.0,427.0,415.0]

draw_pie(labels, quants)
