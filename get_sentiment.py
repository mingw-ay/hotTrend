import json
import requests

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
    print(results)
    return results


# 根据感情倾向数值进行可视化呈现
def process_bar(percent):
    repeat_times = int(percent * 10)
    bar = '感情正向->' + '微笑' * repeat_times + \
        '伤心' * (10 - repeat_times) + '<-感情负向'
    print(bar)


myStr = '味道不错，确实不算太辣，适合不能吃辣的人。就在长江边上，抬头就能看到长江的风景。鸭肠、黄鳝都比较新鲜。'
process_bar(txt_mask(myStr, mytoken)['positive_prob'])
