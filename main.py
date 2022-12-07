# 至少一个反反爬技术并阐述说明
# 自主选择感兴趣的电视剧（集数不少于10集），爬取每集弹幕信息，爬取信息量不少于500条，信息包含但不限于集数、播放时间点、弹幕信息内容
# 爬取的数据保存在csv文件或数据库中（二选一），供数据可视化分析，需根据弹幕数量分析剧情受欢迎程度，弹幕关键词云分析，弹幕词频（赞、演技很好、颜值很高等积极信息和演技差、剧情不合理、吐槽等消极信息）统计分析。
import os
import requests
from fake_useragent import UserAgent
from lxml import etree
import time
import csv


# 820680426     820680738
headers = {
        'User-agent': UserAgent().random
}
# 创建树解析对象

def getTree(url):
    res = requests.get(url, headers=headers)
    res.encoding='utf-8'
    tree = etree.HTML(res.text.encode('utf-8'))
    return tree

def parse_data(tree):

    element_list = tree.xpath('//d')

    rows = []
    for attrs_ele in element_list:
        # 2695.34400,1,25,16707842,1670310086,0,355b8c5,1201407094729993216,11
        attr_ele = attrs_ele.xpath('./@p')[0]

        # 弹幕出现的时间
        emerge_time = attr_ele.split('.')[0]
        m_emerge_time = time.strftime("%H:%M:%S", time.gmtime(int(emerge_time)))
        # 时间戳
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(attr_ele.split(',')[4])))
        # 内容
        texts = attrs_ele.xpath('./text()')[0]
        rows.append([m_emerge_time, timestamp, texts])



    return rows



def fetch(cid, episode_name, index):

    # with open("家有仙妻前十集.csv", "w", newline='', encoding='utf-8')as f:
    #     csv_writer = csv.writer(f)
    #     header = ['弹幕信息出现分钟', '弹幕出现日期', '弹幕内容']
    #     csv_writer.writerow(header)


        url = f'http://comment.bilibili.com/{cid}.xml'
        print(f'{url}准备被抓取')
        # time.sleep(3)
        # 获取树解析对象
        tree = getTree(url)
        # 解析方法返回一组数据列表
        rows = parse_data(tree)
        # 创建csv文件夹来对每一集的弹幕进行存储
        if not os.path.exists(episode_name):
            os.mkdir(episode_name)
        csv_name = f'家有仙妻第{index}集'
        path = os.path.join(episode_name, csv_name+'.csv')
        with open(path, 'a', encoding='utf-8', newline='')as f:
            csv_writer = csv.writer(f)
            header = ['弹幕信息出现分钟', '弹幕出现日期', '弹幕内容']
            csv_writer.writerow(header)
        # 接下来循环遍历这个数组列表
            for row in rows:
                csv_writer.writerow(row)

        print(csv_name,'已存储完成')





if __name__ == '__main__':
    start = time.time()
    # 家有仙妻 前十集的cid值
    cids = [820680426, 820680738, 820681510, 820682146, 820682647, 820682989, 820683722, 820684233, 820684795, 820685315]
    files_name = '家有仙妻弹幕汇总'
    i = 1
    for cid in cids:
        fetch(cid, files_name, i)
        i = i + 1
    print('Progrem Finished')
    print(f'累计用时{time.time()-start}')