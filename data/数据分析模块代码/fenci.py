import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib


df = pd.read_table('C:/Users/Administrator/Desktop/数据处理结果/数据爬取/特朗普终止与世界卫生组织合作/0505.txt', names=['name', 'content'], encoding='utf-8')
df = df.dropna()

content = df.content.values.tolist()
#for i in content:
#   print(i)
content = df.content.values.tolist()
print(content[200])

content_S = []
for i in range(df.shape[0]):
    content_S.append(jieba.lcut(content[i]))

df_content = pd.DataFrame({'content': content_S})

stopwords = pd.read_csv('tingyongcibiao.txt',
                        index_col=False,sep='\t',
                        quoting=3,
                        names=['stopwords'],
                        encoding='gbk')
stopwords = stopwords.stopwords.values.tolist()
print('清洗前的数据第200条数据的分词情况：',len(df_content.content[200]))

all_word = []  # 存储除停用词外的所有词（可重复）
content_word = []  # 按新闻条数一次存入清洗后的新闻列表

su = len(df_content.content)

for line in df_content.content:
    line_clean = []
    # print(line)
    for i in line:
        if i in stopwords:
            continue
        line_clean.append(i)
        all_word.append(i)

    content_word.append(line_clean)

print('清洗后的数据第1000条数据的分词情况：', len(content_word[200]))
# 清理完的数据
df_content = pd.DataFrame({'contents_clean': content_word})
df_all_words = pd.DataFrame({'all_words': all_word})

# 得到词频数据
words_count = df_all_words['all_words'].value_counts()
words_count = pd.DataFrame({'val': words_count})
words_count.sort_values(by='val', inplace=True, ascending=False)

print(words_count.head(50))

# 生成词云
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)

cloud = WordCloud(font_path='PingFang.ttc',
                  background_color='white',
                  max_font_size=80)

word_frequence = {words_count.index[x]: words_count['val'][x] for x in range(100)}
print(word_frequence)
cloud = cloud.fit_words(word_frequence)

plt.imshow(cloud)
plt.show()

