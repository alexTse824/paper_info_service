# coding=utf-8
import os
import json
import requests
import setting

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class BaiduPaperInfoCrawler:
    
    PAPER_LIST_PAGE_HEADER = {
        'User-Agent': UserAgent().random,
        'Referer': 'https://xueshu.baidu.com/',
        'Host': 'xueshu.baidu.com'
    }
    
    PAPER_CIT_PAGE_HEADER = {
        'User-Agent': UserAgent().random,
        'Host': 'xueshu.baidu.com'
    }

    def __init__(self, keyword):
        self.keyword = keyword
        self.proxy = self.get_proxy()

    def get_proxy(self):
        return json.loads(requests.get('{}/get/'.format(setting.PROXY_POOL_ADDR)).text)['proxy']

    def delete_proxy(self, proxy):
        '''删除并更新代理'''
        requests.get("{}/delete/?proxy={}".format(setting.PROXY_POOL_ADDR, proxy))
        self.proxy = self.get_proxy()

    def get_paper_cit(self):    
        ret = []
        # sc_hit参数指定跳转列表页面
        response = requests.get('http://xueshu.baidu.com/s', params={'sc_hit': 1, 'wd': self.keyword}, headers=self.PAPER_LIST_PAGE_HEADER, proxies={"http": "http://{}".format(self.proxy)})

        # 反爬页面筛选（验证码、错误页面）
        if 'https://wappass.baidu.com/static/captcha/tuxing.html' in response.url:
            print('Baidu captcha, delete proxy {}'.format(self.proxy))
            self.delete_proxy(self.proxy)
        elif response.url == 'https://www.baidu.com/search/error.html':
            print('Baidu error page, delete proxy {}'.format(self.proxy))
            self.delete_proxy(self.proxy)
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


class GooglePaperInfoCrawler:
    def __init__(self, keyword):
        self.keyword = keyword
        self.options = Options()
        self.options.headless = True
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference('network.proxy.type', 2)
        self.profile.set_preference('network.proxy.autoconfig_url', setting.PAC_URL)
        self.profile.set_preference('intl.accept_languages', 'en-US, en')
        self.profile.set_preference("general.useragent.override", UserAgent().random)
    
    def get_paper_cit(self):
        ret = []
        url = 'https://scholar.google.com/scholar?lookup=0&q={}'.format(self.keyword)
        try:
            browser = webdriver.Firefox(
                executable_path = setting.WEBDRIVER_PATH,
                options=self.options,
                service_log_path=os.path.join('log', 'geckodriver.log'),
                firefox_profile=self.profile
            )
            browser.get(url)
            paper_list = []
            item_list = browser.find_elements_by_class_name('gs_scl')
            for item in item_list:
                paper_id = item.get_attribute('data-cid')
                if paper_id:
                    paper_list.append(paper_id)

            for paper_id in paper_list:
                cit_url = 'https://scholar.google.com/scholar?q=info:{}:scholar.google.com/&output=cite'.format(paper_id)
                browser.get(cit_url)
                cit_ele = browser.find_element_by_class_name('gs_citr')
                info = cit_ele.text
                ret.append(info)
        except Exception as e:
            print(e)
        finally:
            browser.quit()
        return ret
