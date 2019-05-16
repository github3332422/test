'''
练习使用pandas对数据进行处理。
'''
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
from lxml import etree
'''
df获取 all.xls 的数据
df1获取 全国城市经纬度表.xls 的数据
'''
df = pd.DataFrame(pd.read_excel('../../data/all.xls'))

'''
获取每个大的行政区的所有城市列表
'''
def get_allKV():
    f = open('../../data/all.txt', encoding='UTF-8').read()
    response = etree.HTML(f)
    provience = response.xpath("//div[@class='mw-parser-output']/h3//span[@class='mw-headline']//text()")
    citys = response.xpath("//div[@class='mw-parser-output']/ul")[2:-1]
    dict = []
    for p, c in zip(provience, citys):
        item = {
            'provience': p,
            'citys': c.xpath("./li//a//text()")
        }
        dict.append(item)
    item = {
        'provience': "北京市",
        'citys': "北京"
    }
    dict.append(item)
    item = {
        'provience': "天津市",
        'citys': "天津"
    }
    dict.append(item)
    item = {
        'provience': "上海市",
        'citys': "上海"
    }
    dict.append(item)
    item = {
        'provience': "重庆市",
        'citys': "重庆"
    }
    dict.append(item)
    return dict

'''
通过省份，获取每一个省份的所有城市
'''


'''
获取原始的省的数据
'''
# def get_provience():
#     provience = []
#     for x in df1['provience']:
#         provience.append(x.strip())
#     return provience

'''
对城市数据进行处理
'''
def get_city():
    city = []
    for x in df['city']:
        city.append(x.split('-')[0])
    return city
    # se = set(city)
    # #设置城市和职位数目
    # items = []
    # for s in se:
    #     item = {
    #         'name': s,
    #         'value': city.count(s)
    #     }
    #     items.append(item)
    #     # print(s,city.count(s))
    # for item in items:
    #     print(item,',')

'''
对薪水进行分析处理
对工资面议的数据进行处理:对工资面议的数据设置为其他数值的平均值
'''
def get_salary():
    salary = []
    for x in df['salary']:
        x = re.sub('[k|K]', '', x).split('-')
        salary.append(x)
    return salary

'''
对经验进行分析处理
对经验不限和无的情况设置为0
'''
def get_experience():
    experience = []
    for x in df['jinyan']:
        x = re.sub('[年]', '', x).split('-')
        experience.append(x)
    return experience

'''
对经验福利进行分析
对一些符号进行处理
'''
def deal_fuli_wordclod():
    text = ""
    for x in df['fuli']:
        x = re.sub('[,]', '', x)
        x = re.sub('"','',x)
        x = re.sub(' ','',x)
        # print(x[1:-1])
        text += x[1:-1]
    print(text)
    cut_text = jieba.cut(text)
    # 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云
    result = " ".join(cut_text)
    # 3.生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
    # 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'
    wc = WordCloud(
        font_path=r'.\simhei.ttf',
        background_color='white',
        width=500,
        height=350,
        max_font_size=50,
        min_font_size=10,
    )
    # 产生词云
    wc.generate(result)
    # 保存图片
    wc.to_file(r"../../tmp/fuliwordcloud.png")


def main():
    #第一步获取各个城市所对应的省份
    dict = get_allKV()
    #第二步，统计每个城市有多少个职位
    city = get_city()
    scity = list(set(city))

    for s in scity:
        for d in dict:
            for x in d['citys']:
                if s in x:
                    print(s,d['provience'],city.count(s))


if __name__ == '__main__':
    main()