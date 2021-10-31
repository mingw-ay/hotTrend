import time
import json
import requests
from util.newsdb import get_comments_without, update_comments

# client_id 为官网获取的AK， client_secret 为官网获取的SK
# 获取access_token
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=4VdHqzXuclTj2G7M9d9GG7mC&client_secret=xLrOO6HH2h9t94CWzfrtT75aiz2TC47S'
response = requests.get(host).json()
mytoken = response['access_token']


def txt_mask(mystr, mytoken):
    data = json.dumps({
        "text": mystr
    })

    header = {
        'Content-Type': 'application/json'
    }

    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=' + mytoken
    results = requests.post(url=url, headers=header, data=data).json()
    results = results['items'][0]
    return results


# 根据感情倾向数值进行可视化呈现
def process_bar(percent):
    repeat_times = int(percent * 10)
    bar = '感情正向->' + '微笑' * repeat_times + \
        '伤心' * (10 - repeat_times) + '<-感情负向'
    print(bar)


# 从数据库中取出未曾进行情感分析的评论对象列表
commentList = get_comments_without()


# 循环commentList对象列表
# 然后对每个对象进行情感分析，并且将结果放入对象
for i, comment in enumerate(commentList):
    result = txt_mask(comment.comment_str, mytoken)
    commentList[i].sentiment = result['sentiment']
    commentList[i].positive = result['positive_prob']
    commentList[i].confidence = result['confidence']
    print(f'分析了第{i}个评论')
    time.sleep(0.3)


# 更新数据库comment表
update_comments(commentList)
