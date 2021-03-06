import urllib
import urllib.request
import json
import re
import time
from pyquery import PyQuery as pq
import random
import  requests
import os
import threading
def download(url,path):

    opener = urllib.request.build_opener()
    randdom_header = random.choice(my_headers)
    opener.addheaders = [('User-agent', randdom_header)]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, path)

def open_html(url):
    agent = random.choice(my_headers)
    headers = {'User-Agent': agent}
    require = urllib.request.Request(url=url, headers=headers)
    reponse = urllib.request.urlopen(require)
    html = reponse.read()
    return html
def get_json(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'cookie': 'qz99r5VmLrNvURxZrk1zBjl4RygJ2aN5'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print('请求网页json错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        time.sleep(60 + float(random.randint(1, 4000))/100)
        return get_json(url)
def get_urls(html):
    urls = []
    html_decode = html.decode('utf-8')
    user_id = re.findall('"profilePage_([0-9]+)"', html_decode, re.S)[0]
    print('user_id：' + user_id)
    doc = pq(html)
    items = doc('script[type="text/javascript"]').items()
    for item in items:
        if item.text().strip().startswith('window._sharedData'):
            js_data = json.loads(item.text()[21:-1], encoding='utf-8')
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
            cursor = page_info['end_cursor']
            flag = page_info['has_next_page']
            for edge in edges:
                if edge['node']['display_url']:
                    display_url = edge['node']['display_url']
                   # print(display_url)
                    urls.append(display_url)
            #print(cursor, flag)
    while flag:
        url = uri.format(user_id=user_id, cursor=cursor)
        #print(url)
        js_data = get_json(url)
        #print(js_data)
        infos = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        #print(infos)
        cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        for info in infos:
            if info['node']['display_url']:
                display_url = info['node']['display_url']
                #print(display_url)
                urls.append(display_url)
        #print(cursor, flag)
        # time.sleep(4 + float(random.randint(1, 800))/200)    # if count > 2000, turn on
    return urls
def run(linklist,title):
    if not os.path.exists("ins/"+title):
        os.mkdir("ins/"+title)
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(title):
        for file in filenames:
            file_count = file_count + 1
    load_image(linklist,title,file_count)
def load_image(linklist,title,file_count):
    num=1
    thread_pool = []
    max_thread = 30
    while True:
        try:
            # 多线程
            for t in thread_pool:
                if not t.is_alive():
                    thread_pool.remove(t)
            if len(thread_pool) == max_thread:
                continue
            if linklist != None:
                link=linklist[0]
                linklist.remove(link)
                file_name = "ins/"+ title + "/" + str(num) + ".jpg"

                num = num + 1
                if not os.path.exists(file_name):
                    thread = threading.Thread(target=download, name=None, args=(link, file_name))
                    thread_pool.append(thread)
                    thread.setDaemon(True)
                    thread.start()
                    print(str(thread.ident)+"下载了"+file_name)
                    file_count = file_count + 1;
                    sleepTime = random.uniform(1, 2)
                    time.sleep(sleepTime)
                else:
                    pass
            else: break

        except Exception as Arg:
            print(Arg)
            break
    if file_count >= len(linklist):
        print("下载成功！！！")
    else:
        print("下载失败，正在重试！")
if __name__ == '__main__':
    web= 'https://www.instagram.com/'
    user='kimuko__0'
    url = web+user
    my_headers = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36']
    html = open_html(url)
   #print(html)
    urls=get_urls(html)
    title = user
    if not os.path.exists("ins/"):
        os.mkdir("ins/")
    run(urls,title)

