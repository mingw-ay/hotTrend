import jieba.posseg as pseg


# 1.得到停用词列表stopwords,是他人整理的停用词
stopwords = set()

with open(r'dataset\stopwords.txt', encoding='utf-8') as f:
    for line in f:
        stopwords.add(line.strip())


# 2.对应的去除停用词方法
def remove_stopword(words):
    return [word for word in words if word not in stopwords]


# 3.将每条新闻的分词后数组转化为空格分隔的字符串
def join(text_list):
    return " ".join(text_list)


# 4.对应的分词方法（去除每个flag为x,即标点符号）,并且只截取前100个汉字
def cut2words(newsList):
    for i in range(len(newsList)):
        words = pseg.cut(newsList[i])
        newsList[i] = []
        wordsCount = 0
        for w in words:
            if w.flag != 'x' and wordsCount < 100:
                wordsCount += len(w.word)
                newsList[i].append(w.word)
        # 调用去除停用词方法
        newsList[i] = remove_stopword(newsList[i])
        # 调用转为字符串方法
        newsList[i] = join(newsList[i])
    return newsList


# 5.类别标签对应
def map2digits(labelList):
    for i, x in enumerate(labelList):
        if x == 0:
            labelList[i] = '体育'
        elif x == 1:
            labelList[i] = '财经'
        elif x == 2:
            labelList[i] = '房产'
        elif x == 3:
            labelList[i] = '家居'
        elif x == 4:
            labelList[i] = '教育'
        elif x == 5:
            labelList[i] = '科技'
        elif x == 6:
            labelList[i] = '时尚'
        elif x == 7:
            labelList[i] = '时政'
        elif x == 8:
            labelList[i] = '游戏'
        else:
            labelList[i] = '娱乐'
    return labelList
