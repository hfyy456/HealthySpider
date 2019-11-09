import urllib
import urllib.request
import os
from bs4 import BeautifulSoup
import time
import random
import threading


# 打开网页，下载器
def open_html(url):
    agent=random.choice(my_headers)
    headers = {'User-Agent': agent}
    require = urllib.request.Request(url=url, headers=headers)
    reponse = urllib.request.urlopen(require)
    html = reponse.read()
    return html

def download(url,path):

    opener = urllib.request.build_opener()
    randdom_header = random.choice(my_headers)
    opener.addheaders = [('User-agent', randdom_header)]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, path)

def read_linklist(html):
    soup = BeautifulSoup(html, 'lxml')
    root = "https://asiansister.com/"
    linklist = []
    for link in soup.findAll(name='img', attrs={'class': 'lazyload showMiniImage'}):
        link = link.get("dataurl")
        link = link[5:]
        link = root + link
        linklist.append(link)
    return linklist
def read_title(html):
    soup = BeautifulSoup(html, 'lxml')
    titles = soup.find_all(name="h1")
    title = titles[0].string
    print(title)
    return title
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
                file_name = "images/"+ title + "/" + str(num) + ".jpg"

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

def run(linklist,title):
    if not os.path.exists("images/"+title):
        os.mkdir("images/"+title)
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(title):
        for file in filenames:
            file_count = file_count + 1
    load_image(linklist,title,file_count)


def href_reader(root):
    html=open_html(root)
    soup = BeautifulSoup(html, 'lxml')
    hrefs=[]
    for i in soup.findAll(name='div',attrs={'class': 'itemBox'}):
        a=i.find("a")
        href=a.get("href")
        hrefs.append(href)
    print(hrefs)
    return hrefs
def page_reader(root):
    html = open_html(root)
    soup = BeautifulSoup(html, 'lxml')
    pages = []
    for i in soup.findAll(name='a', attrs={'class': 'btn page'}):
        b=i.find(name="b")
        total=b.string
        total=int(total)
    for index in range(total):
        s='_page'+str(index+1)
        pages.append(s)
    return pages
if __name__ == '__main__':

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
    root="https://asiansister.com/"
    pages=page_reader(root)
    for page in pages:
        print("正在爬取第"+page[1:]+"页的内容")
        url1=root+page
        hrefs=href_reader(url1)
        for href in hrefs:
            url=root+href
            html = open_html(url)
            linklist = read_linklist(html)
            title = read_title(html)
            run(linklist,title)
            time.sleep(1)
    input("输入任意键结束")

