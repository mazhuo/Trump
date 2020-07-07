import pandas as pd

# 读取原始数据
data = pd.read_csv('C:/Users/Administrator/Desktop/数据处理结果/数据爬取/特朗普称将很快接受病毒检测/0101.csv', encoding='gb18030')

print('原始数据信息：')
print(len(data))
print('--------------------')

# 清除缺失数据
data = data.dropna()

print('清除缺失数据后：')
print(len(data))
print('--------------------')


# 文本去重处理
data = pd.DataFrame(data['评论'].unique())
print('文本去重处理后：')
print(len(data))
print('--------------------')

# 机械压缩去词函数定义
def cutword(strs,reverse=False):
        s1=[]
        s2=[]
        s=[]
        if reverse :
            strs=strs[::-1]

        s1.append(strs[0])
        for i in strs[1:]:
            if i==s1[0] :
                if len(s2)==0:
                    s2.append(i)
                else :
                    if s1==s2:
                        s2=[]
                        s2.append(i)
                    else:
                        s=s+s1+s2
                        s1=[]
                        s2=[]
                        s1.append(i)
            else :
                if s1==s2 and len(s1)>=2 and len(s2)>=2 :
                    s=s+s1
                    s1=[]
                    s2=[]
                    s1.append(i)
                else:
                    if len(s2)==0:
                        s1.append(i)
                    else :
                        s2.append(i)
        if s1==s2:
            s=s+s1
        else:
            s=s+s1+s2
        if reverse :
            return''.join(s[::-1])
        else:
            return''.join(s)

# 机械压缩去词
data2 = data.iloc[:,0].apply(cutword)
data2 = data2.apply(cutword,reverse=True)
print('机械压缩去词后：')
print(len(data2))
print('--------------------')

# 短句过滤
data3 = data2[data2.apply(len)>=4]
print('短句过滤后：')
print(len(data3))
print('--------------------')

# 情感分析
from snownlp import SnowNLP
coms = []
coms = data3.apply(lambda x: SnowNLP(x).sentiments)


data3.to_csv('C:/Users/Administrator/Desktop/数据处理结果/数据爬取/特朗普称将很快接受病毒检测/Result1.csv',encoding='utf_8_sig')
coms.to_csv('C:/Users/Administrator/Desktop/数据处理结果/数据爬取/特朗普称将很快接受病毒检测/Result2-scores.csv',encoding='utf_8_sig')
print('情感分析后：')
print(data3)
print(coms)
print('--------------------')

# 情感分析后的正负分类
data1 = data3 [coms>=0.7]
data2 = data3 [coms<0.3]

print('情感分类后数据：')
print('大于等于0.7——积极情绪：')
print(data1)
print('小于等于0.3——消极情绪：')
print(data2)
print('--------------------')

data1.to_csv('C:/Users/Administrator/Desktop/数据处理结果/数据爬取/特朗普称将很快接受病毒检测/Result3-split-pos.csv',encoding='utf_8_sig')
data2.to_csv('C:/Users/Administrator/Desktop/数据处理结果/数据爬取/特朗普称将很快接受病毒检测/Result4-split-neg.csv',encoding='utf_8_sig')

# 分词
import jieba
mycut = lambda s: ' '.join(jieba.cut(s))
data1 = data1.apply(mycut)
data2 = data2.apply(mycut)


print('大于等于0.7——积极情绪——分词')
print(data1)
print('小于等于0.3——消极情绪——分词')
print(data2)
print('--------------------')


















