import requests
import json
import random
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import settings


def get_proxy():
    proxy_pool_addr = '{}:{}'.format(settings.PROXY_POOL_HOST, settings.PROXY_POOL_PORT)
    return json.loads(requests.get('http://{}/get/'.format(proxy_pool_addr)).text)['proxy']

def delete_proxy(proxy):
    requests.get("http://{}:{}/delete/?proxy={}".format(settings.PROXY_POOL_HOST, settings.PROXY_POOL_PORT, proxy))
    print('Deleting proxy:', proxy)

def refresh_mirror_list():
    mirror_list = []
    proxy = get_proxy()
    response = requests.get(
        'https://www.library.ac.cn/',
        headers={'User-Agent': UserAgent(verify_ssl=False).random,},
        proxies={"http": "http://{}".format(proxy)}
    )

    soup = BeautifulSoup(response.text, 'html.parser')
    public_mirror_tr_list = [i for i in soup.find_all('tr', class_='text-center')][1:3]
    for public_mirror_tr in public_mirror_tr_list:
        mirror_list.extend([i['href'] for i in public_mirror_tr.find_all('a', title='Google Scholar')])
    
    with open('mirrors.json', 'w') as f:
        json.dump(mirror_list, f, indent=4)

    print('Get {} mirrors'.format(len(mirror_list)))


def get_google_scholar_citation(keyword, base_url, max_retries=3):
    # TODO: 拉取谷歌学术US、HK镜像站节点列表并测试连通性，根据连接速度排序，定时优选
    base_url = 'https://scholar.google.tsinbei.cn/'
    keyword = 'machine'
    proxy = get_proxy()

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
