import datetime
import os
import random
import time
import urllib
from bs4 import BeautifulSoup
import http.cookiejar
import gzip
import re
from pyquery import PyQuery as pq

class pixiv_praser:
    def __init__(self):
        self.root="http://www.pixiv.net/member_illust.php?mode=medium&illust_id="
        self.url="https://www.pixiv.net/ranking.php?mode=monthly&content=illust&date=20190909"
        self.my_headers = [
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
        self.login_url = "https://accounts.pixiv.net/login"
        self.login_post = 'https://accounts.pixiv.net/api/login'
        self.base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'accounts.pixiv.net',
            'Referer': 'http://www.pixiv.net/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'
        }

    def open_html(self,url):
        agent = random.choice(self.my_headers)
        headers = {'User-Agent': agent}
        require = urllib.request.Request(url=url, headers=headers)
        reponse = urllib.request.urlopen(require)
        html = reponse.read()
        return html
    def get_post_key(self):
        base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        key_headers = {
              'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        require = urllib.request.Request(url=base_url, headers=key_headers)
        reponse = urllib.request.urlopen(require)
        html = reponse.read()
        post_key_soup = BeautifulSoup(html, 'lxml')
        post_key = post_key_soup.find('input')['value']
        return post_key

    def getopener(self):
        cj = http.cookiejar.CookieJar()
        cp = urllib.request.HTTPCookieProcessor(cj)
        op = urllib.request.build_opener(cp)
        h = []
        for key, value in self.base_headers.items():
            elem = (key, value)
            h.append(elem)
        op.addheaders = h
        return op
    def login(self):
        op = self.getopener()
        post_key=self.get_post_key()
        pixiv_id="siriushfyy@gmail.com"
        pixiv_password="Fyw2DDuHEiUdXRn"
        pixiv_source = 'accounts'
        post_data = {
            'pixiv_id': pixiv_id,
            'password': pixiv_password,
            'post_key': post_key,
            'source': pixiv_source
        }
        post_data = urllib.parse.urlencode(post_data).encode('utf-8')
        op_login = op.open(self.login_post, post_data)
        op_login.close()
        return op
    def read_id(self,html):
        soup = BeautifulSoup(html, 'lxml')
        ids=[]
        #print(soup)
        sections=soup.findAll(name='section', attrs={'class': 'ranking-item'})
        for s in sections:
            print(s)
            id=s.attrs['data-id']
            ids.append(id)
        return ids
    def read_title(self,html):
        soup = BeautifulSoup(html, 'lxml')
        titles = []
        # print(soup)
        sections = soup.findAll(name='section', attrs={'class': 'ranking-item'})
        for s in sections:
            print(s)
            title = s.attrs['data-title']
            titles.append(title)
        return titles

    def get_images(self):
        opener = self.login()
        html = opener.open(self.url).read()
        res = gzip.decompress(html).decode("utf-8")
        ids=self.read_id(res)
        titles=self.read_title(res)
        urls=[]
        i=0
        path_root="pixiv"
       # print(ids)
        #pixiv_url_login_test = 'https://i.pximg.net/img-master/img/2019/11/09/18/41/47/77723343_p0_master1200.jpg'
        #path="ins"
        #with opener.open(pixiv_url_login_test) as i:
          #if i.status == 200:
                #print("登陆成功！")
                #print("开始下载测试图片！")

                #with open(os.path.join(path, pixiv_url_login_test.split('/')[-1]), 'wb') as o:
                    #o.write(i.read())
                    #print("下载完成！")
        for id in ids:
            url=self.root+str(id)
            urls.append(url)
        for url in urls:
            print(url)
            html = opener.open(url).read()
            res = gzip.decompress(html).decode("utf-8")
            print(titles[i])
            urls=re.search(r'(?<=regular)((?:(?!regular).)*?)(?=original)',res)
            image_url=urls[0]
            image_url=re.findall("https.*jpg|https.*png",image_url)
            image_url=image_url[0]
            print(image_url)
            filename=os.path.join(path_root, titles[i]+".jpg")
            if not os.path.exists(filename):
                with opener.open(image_url) as img:
                    if img.status == 200:
                        print("开始下载图片！")
                        with open(filename, 'wb') as o:
                            o.write(img.read())
                            print("下载完成！")
            else:
                    print("该图片已下载，略过")
            i=i+1
            time.sleep(1)




