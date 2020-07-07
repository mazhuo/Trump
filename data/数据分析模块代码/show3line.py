#散点图
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
df = pd.read_csv('C:/Users/Administrator/Desktop/数据处理结果/time.csv',  parse_dates=['time'])
plt.plot_date(df.time, df.score, fmt='b.')

ax = plt.gca()
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))  #设置时间显示格式
ax.xaxis.set_major_locator(AutoDateLocator(maxticks=120
                                           ))  # 设置时间间隔

plt.xticks(rotation=90, ha='center')
label = ['score']
plt.legend(label, loc='upper right')

plt.grid()

ax.set_title(u'情感分值散点图', fontproperties='SimHei', fontsize=14)
ax.set_xlabel('time')
ax.set_ylabel('score')

plt.show()
