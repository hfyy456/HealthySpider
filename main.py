import os

from asiansister_praser import asiansister_praser
from downloader import downloader
from instagram_praser import instagram_praser
if __name__ == '__main__':

    print("选择你要爬取的网站：")
    print("1.Asiansister")
    print("2.Instagram")
    selected=False
    selections=["1","2"]
    dl = downloader()
    if not os.path.exists("images/"):
        os.mkdir("images/")
    while(selected==False):
        selection = input("请输入序号:")
        if(selection in selections):
            print("你选择了" + selection)
            selected=True
        else:
            print("请输入正确的序号")
            selected=False
    if(selection=='1'):
        url="https://asiansister.com/"
        ap=asiansister_praser()
        pages = ap.page_reader()
        linklist = []
        for page in pages:
            print("正在爬取第" + page[1:] + "页的内容")
            url1 = ap.root + page
            hrefs = ap.href_reader(url1)
            for href in hrefs:
                url = ap.root + href
                html = ap.open_html(url)
                title=ap.read_title(html)
                linklist=ap.read_linklist(html)
                dl.run(linklist,title)
                #print(linklist)

    elif(selection=="2"):
        user = input("请输入你要爬取博主的用户名:\n")
        inp=instagram_praser(user)
        urls=inp.get_urls()
        title = user
        if not os.path.exists("ins/"):
            os.mkdir("ins/")
        dl.run(urls,title)



