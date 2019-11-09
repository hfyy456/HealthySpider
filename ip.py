import time
from random import random

import requests
from scrapy.selector import Selector

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER"
}



def rand_sleep_time():
    sleep_time = random() * 100
    return time.sleep(sleep_time)

# 用于更新ip池
def update_ip_pond():
    # 这个网站目前一共有3637页，这里获取前面的10个页面
    for i in range(1, 11):
        resp = requests.get('https://www.xicidaili.com/wn/%s' % i, headers=headers)
        if resp.status_code != 200:
            print('第%s页获取失败' % i)
        else:
            print('已获取第%s页内容' % i)
        selector = Selector(text=resp.text)
        # 使用xpath找到ip_list这个id
        all_items = selector.xpath('//*[@id="ip_list"]//tr')
        ip_list = []
        #第一行不是我们需要的，过滤掉，从第1列开始
        for item in all_items[1:]:
            # 这里使用xpath从网页提取
            speed_str = item.xpath('td[7]/div/@title').get()
            ip = item.xpath('td[2]/text()').get()
            ip_list.append(ip)

    print(ip_list)
    with open("ip.txt", "w") as f:
        for i in ip_list:
            print(i, file=f)
update_ip_pond()