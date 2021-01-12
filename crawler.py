import requests
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import settings


class ProxyHandler:
    def __init__(self):
        self.proxy_pool_addr = '{}:{}'.format(settings.PROXY_POOL_HOST, settings.PROXY_POOL_PORT)

    def get_proxy(self):
        return json.loads(requests.get('http://{}/get/'.format(self.proxy_pool_addr)).text)['proxy']

    def delete_proxy(self, proxy):
        '''删除并更新代理'''
        requests.get("http://{}/delete/?proxy={}".format(self.proxy_pool_addr, proxy))


class BaiduPaperInfoCrawler:
    PAPER_LIST_PAGE_HEADER = {
        'User-Agent': UserAgent(verify_ssl=False).random,
        'Referer': 'https://xueshu.baidu.com/',
        'Host': 'xueshu.baidu.com'
    }
    
    PAPER_CIT_PAGE_HEADER = {
        'User-Agent': UserAgent(verify_ssl=False).random,
        'Host': 'xueshu.baidu.com'
    }

    def __init__(self, keyword):
        self.keyword = keyword
        self.proxy_handler = ProxyHandler()
        self.proxy = self.proxy_handler.get_proxy()

    def get_paper_cit(self):    
        ret = []

        # sc_hit参数指定跳转列表页面
        response = requests.get(
            'http://xueshu.baidu.com/s',
            params={'sc_hit': 1, 'wd': self.keyword}, headers=self.PAPER_LIST_PAGE_HEADER, proxies={"http": "http://{}".format(self.proxy)}
        )

        # 反爬页面筛选（验证码、错误页面）
        if 'https://wappass.baidu.com/static/captcha/tuxing.html' in response.url or response.url == 'https://www.baidu.com/search/error.html':
            print('proxy busted, deleting {}'.format(self.proxy))
            self.proxy_handler.delete_proxy(self.proxy)
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            cit_btn_list = soup.find_all('a', class_='sc_q c-icon-shape-hover')
            if cit_btn_list:
                for cit_btn in cit_btn_list:
                    cit_info = self.get_cit_info(cit_btn['data-sign'], cit_btn['data-link'])
                    if cit_info:
                        ret.append(cit_info)
        return ret

    def get_cit_info(self, sign, url):
        '''引文详情页面获取GB/T7714格式引文'''
        params = {'sign': sign, 'url': url, 't': 'cite'}
        response = requests.get('https://xueshu.baidu.com/u/citation', params=params, headers=self.PAPER_CIT_PAGE_HEADER, proxies={"http": "http://{}".format(self.proxy)})
        return json.loads(response.text).get('sc_GBT7714', '')
