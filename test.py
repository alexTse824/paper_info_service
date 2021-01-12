import requests
import json
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import settings


start_time = time.time()
# 获取代理
proxy_pool_addr = '{}:{}'.format(settings.PROXY_POOL_HOST, settings.PROXY_POOL_PORT)
proxy = json.loads(requests.get('http://{}/get/'.format(proxy_pool_addr)).text)['proxy']
print('Using Proxy: {}'.format(proxy))

# TODO: 拉取谷歌学术US、HK镜像站节点列表并测试连通性，根据连接速度排序，定时优选
base_url = 'https://us3111.scholar.eu.org/'
keyword = 'machine'

with requests.Session() as s:
    # 拉取关键字第一页所有item的datacid
    s.proxies = {'http': "http://{}".format(proxy)}
    s.headers.update({
        'User-Agent': UserAgent(verify_ssl=False).random,
        'Referer': base_url,
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    })

    search_url = '{}/scholar?q={}'.format(base_url, keyword)
    response = s.get(search_url, timeout=5)
    print(response)

    soup = BeautifulSoup(response.text, 'html.parser')
    paper_id_list = [paper_item['data-cid'] for paper_item in soup.find_all('div', class_='gs_r gs_or gs_scl')]

    # 分别获取所有item的引文信息
    s.headers.update({
        'User-Agent': UserAgent(verify_ssl=False).random,
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    })

    cit_list = []

    for paper_id in paper_id_list:
        cit_url = '{}/scholar?q=info:{}:scholar.google.com/&output=cite&script=0'.format(base_url, paper_id)

        cit_response = s.get(
            cit_url,
        )
        cit_soup = BeautifulSoup(cit_response.text, 'html.parser')
        cit_list.append(cit_soup.find('div', class_='gs_citr').text)

    print(cit_list)
    print('-' * 50)
    print(s.headers)
    print(s.proxies)
