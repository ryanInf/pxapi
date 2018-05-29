#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# #      Created Date: Tue May 29 2018
# #      Author: Ryan
# #      mail: ryaninf@outlook.com
# #      Last Modified:
# #      Modified By:
# #------------------------------------------
# #      Copyright (c) 2018
# #------------------------------------------
# #
###
import requests
import json
from threading import Thread
from queue import Queue
from lxml import etree
from time import sleep
import re

unchkiplist = []
pxiplist = []
MAX_THREAD = 2000


class ThreadPool(object):
    def __init__(self, max_num=20):
        self.queue = Queue()
        for i in range(max_num):
            self.queue.put(Thread)

    def get_thread(self):
        return self.queue.get()

    def add_thread(self):
        self.queue.put(Thread)


def updatePX():
    api = 'http://jisuproxy.market.alicloudapi.com/proxy/get'
    appcode = 'abcdefg'
    query = 'protocol=2&type=1&num=2000'
    headers = {
        'Authorization': 'APPCODE ' + appcode
    }
    url = api + '?' + query
    r = requests.get(url, headers=headers)
    # print(r.text)
    # print(r.json())
    with open('proxy.json', 'w', encoding='utf-8') as f:
        json.dump(r.json(), f, ensure_ascii=False)
    return r.json()


def getHTML(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        r = requests.get(url, headers=headers)
        # with open('1.html', 'w', encoding='utf-8') as f:
        #     f.write(r.text)
        return r.text
    except:
        return None


def getIPFromXD(page=10):
    url = 'http://www.xicidaili.com/wt/{}'
    for i in range(1, page + 1):
        html = getHTML(url.format(i))
        if html:
            selector = etree.HTML(html)
            ip = selector.xpath('//*[@id="ip_list"]/tr[*]/td[2]/text()')
            port = selector.xpath('//*[@id="ip_list"]/tr[*]/td[3]/text()')
            if len(ip) == len(port):
                for i in range(len(ip)):
                    unchkiplist.append(ip[i] + ':' + port[i])
    # print(unchkiplist)


def getIPFromKD(page=10):
    url = 'https://www.kuaidaili.com/free/inha/{}/'
    for i in range(1, page + 1):
        html = getHTML(url.format(i))
        if html:
            selector = etree.HTML(html)
            ip = selector.xpath(
                '//*[@id="list"]/table/tbody/tr[*]/td[1]/text()')
            port = selector.xpath(
                '//*[@id="list"]/table/tbody/tr[*]/td[2]/text()')
            if len(ip) == len(port):
                for i in range(len(ip)):
                    unchkiplist.append(ip[i] + ':' + port[i])
        sleep(1)
    # print(unchkiplist)


def getIPFrom66():
    url = 'http://www.66ip.cn/nmtq.php?getnum=300&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip'
    html = getHTML(url)
    if html:
        addrlist = re.findall('(\d+.+\d+:\d+?)<br', html)
        unchkiplist.extend(addrlist)
    # print(unchkiplist)


def saveuncheckip():
    proxydic = dict()
    proxydic['result'] = {}
    proxydic['result']['list'] = []
    for addr in unchkiplist:
        proxydic['result']['list'].append({'ip': addr})
    with open('proxy.json', 'w', encoding='utf-8') as f:
        json.dump(proxydic, f, ensure_ascii=False)
    # print(len(proxydic['result']['list']))


def checkPXIP(addr, tpool):
    url = 'http://httpbin.org/ip'
    proxies = {'http': addr, 'https': addr}
    try:
        r = requests.get(url, proxies=proxies, timeout=3)
        ip = addr.split(':')[0]
        if r.json()['origin'] == ip:
            # print(addr)
            pxiplist.append(addr)
    except:
        pass
    finally:
        tpool.add_thread()


def getVIVDPX(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        pxlist = json.load(f)
    tpool = ThreadPool(MAX_THREAD)
    tp = []
    for item in pxlist["result"]["list"]:
        ip = item["ip"]
        thread = tpool.get_thread()
        t = thread(target=checkPXIP, args=(ip, tpool))
        tp.append(t)
        t.start()
        # checkPXIP(ip)
    for th in tp:
        th.join()
    return pxiplist


if __name__ == '__main__':
    # 从各个网站更新IP地址，可选操作
    getIPFrom66()
    getIPFromKD()
    getIPFromXD()
    saveuncheckip()
    # print(len(unchkiplist))
    # 检测IP地址可用性，输出可用IP
    # pxiplist = getVIVDPX('proxy.json')
    # print(len(pxiplist), pxiplist)
