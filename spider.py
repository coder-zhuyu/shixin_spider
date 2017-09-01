# -*- coding: utf-8 -*-
# Created by coder-zhuyu on 2017/9/1
"""
全国失信被执行人爬取
"""
import requests
from random import choice
import time
import pymongo
from pymongo import MongoClient

from agents import AGENTS_ALL


shixin_api_url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'

params = {
    'resource_id': 6899,
    'query': '失信被执行人',
    'pn': 0,
    'rn': 10,
    'ie': 'utf-8',
    'oe': 'utf-8',
    'format': 'json',
}

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'sp0.baidu.com',
    'User-Agent': choice(AGENTS_ALL)
}

mongo_host = '10.0.32.34'
mongo_port = 27017


def get_data(i):
    params['pn'] = i * 10
    try:
        response = requests.get(shixin_api_url, headers=headers, params=params)
        data_list = response.json()['data']
    except Exception as e:
        print(e)
        return []
    else:
        return data_list


def save_data_to_mongo(collection, data_list):
    for data in data_list:
        for result in data['result']:
            # print(result['iname'], result['cardNum'])
            try:
                collection.insert_one(result)
            except Exception as e:
                pass


def main():
    try:
        client = MongoClient(mongo_host, mongo_port)
        db = client['credit']
        collection = db['shixin']
        collection.ensure_index([('iname', pymongo.ASCENDING), ('cardNum', pymongo.ASCENDING)],
                                name='uk_name_card', unique=True)
    except Exception as e:
        print(e)
        return

    for i in range(3):
        print('第' + str(i) + '页')
        data_list = get_data(i)
        if data_list:
            save_data_to_mongo(collection, data_list)
        time.sleep(3)


if __name__ == '__main__':
    main()
