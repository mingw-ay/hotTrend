import os
import numpy as np
import jieba.analyse
from util.newsdb import get_news, update_news
from data_process import cut2words, map2digits
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_selection import SelectKBest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import f_classif


# 采用朴素贝叶斯进行分类的方法如下
def cat_by_bys(newsList):
    # 一、读取得到训练集，测试集，验证机文本，并得到其分类标签列表
    base_dir = 'dataset'
    X_train_dir = os.path.join(base_dir, 'train_contents.txt')
    y_train_dir = os.path.join(base_dir, 'train_labels.txt')

    X_train = open(X_train_dir, encoding='utf-8').read().split('\n')
    y_train = np.array(open(y_train_dir).read().split('\n')).astype(np.int32)
    X_test = newsList

    # 二、使用TfidVectorizer()进行向量化
    # 1.ngram_range=(1,2)先将新闻切分为一维/二维元组再进行向量化
    # 减少语句本来不同但切分出的单词相同带来的误差
    vec = TfidfVectorizer(ngram_range=(1, 2))
    X_train_tran = vec.fit_transform(X_train)
    print('X_train向量化结束!')
    X_test_tran = vec.transform(X_test)
    print('X_test向量化结束!')

    # 2. 将数组转化为float32的numpy数组
    X_train_tran = X_train_tran.astype(np.float32)
    X_test_tran = X_test_tran.astype(np.float32)

    # 3.词袋模型向量化后会产生过多特征，用方差分析进行特征选择
    # 选择出与目标相对变量最相关的20000个特征
    # print(f_classif(X_train_tran, y_train))
    selector = SelectKBest(f_classif, k=min(30000, X_train_tran.shape[1]))
    selector.fit(X_train_tran, y_train)
    X_train_tran = selector.transform(X_train_tran)
    X_test_tran = selector.transform(X_test_tran)

    # 三、训练模型进行预测分析
    # 1.朴素贝叶斯
    clf = MultinomialNB(alpha=0.01)
    clf.fit(X_train_tran, y_train)
    # 2.对输入的新闻主题列表进行预测
    return clf.predict(X_test_tran).tolist()


# 对文本进行清洗以及分词
def getLabels(textList):
    # 调用数据处理进行分词操作
    textList = cut2words(textList)
    print('分词结束!')

    # 进行模型训练以及预测
    print('开始预测!')
    labelList = cat_by_bys(textList)
    labelList = map2digits(labelList)
    return labelList


# 得到文本的关键词并返回关键词列表
def cut2keywords(textList):
    # 得到方法
    extract = jieba.analyse.extract_tags
    keywordsList = []
    for text in textList:
        keywords = extract(text, topK=5, allowPOS=(['n', 'nr']))
        keywordsList.append(' '.join(keywords))
    return keywordsList


# 从数据库取出未分类的新闻，进行清洗
newsList = get_news()
textList = []
for news in newsList:
    textList.append(news.title+news.abstract+news.keywordStr)


# 调用提取关键词方法
keywordsList = cut2keywords(textList)
print('提取关键词结束！')

# 调用分类方法
labelList = getLabels(textList)
print('分类结束！')


# 更新新闻列表
for i, news in enumerate(newsList):
    newsList[i].tag = labelList[i]
    newsList[i].keywordStr = keywordsList[i]

update_news(newsList)
