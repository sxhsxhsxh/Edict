import re
import pymysql
# from urllib import request
import requests
from multiprocessing import Pool,Manager
import json
import time



def fun(url,heads,q):
    db = pymysql.connect("localhost", "root", "123456", "middle_project")
    cur = db.cursor()

    reqData = requests.get(url,headers=heads)
    reqData.encoding = "utf-8"
    dataList = json.loads(reqData.text)["data"]
    # time.sleep(2)
    # if dataList:
    #     q.put(1)
    # else:
    #     q.put(2)
    # print(dataList)
    for i in dataList:
        # print(i['url'])

        # 抓取电影简介
        videoUrl = i['url']
        movdata = requests.get(videoUrl,headers = heads)
        movdata.encoding = "utf-8"
        htmlStr = movdata.text
        reg = re.compile('<span property="v:summary"[\s\S]*?>([\s\S]*?)</span>')
        items = re.findall(reg,htmlStr)
        introStr1 = ' '.join(items[0].split())
        introStr2 = ' '.join(introStr1.split("<br />"))

        # 获取电影制片地点
        reg2 = re.compile(
            '<span class="pl">[\s\S]*?</span>[\s\S]*?<span property="v:genre">[\s\S]*?</span><br/>[\s\S]*?<span class="pl">[\s\S]*?/[\s\S]*?</span>([\s\S]*?)<br/>')
        items2 = re.findall(reg2, htmlStr)
        area = items2[0]
        # print(i['title'], i['url'], items2[0])


        # 获取图片地址
        img = requests.get(i['cover'])
        # 下载图片
        with open("./static/images/moviePoster/%s.jpg" % (i['title']), 'wb') as f:
            f.write(img.content)
        f.close()
        # try:
        #
        # except Exception as e:
        #     print(e)

        id = int(i['id'])
        director = ",".join(i['directors'])
        rate = i['rate']
        title = i['title']
        casts = ",".join(i['casts'])
        movie_poster = "/static/images/moviePoster/%s.jpg" %(i['title'])
        movie_review = introStr2
        print(director,rate,title)

        # pymysql 把数据存入mysql
        try:
            cur.execute("insert into move values ('%d','%s','%s','%s','%s','%s','%s','%s');" %(id,director,area,casts,movie_poster,movie_review,rate,title))
        except Exception as e:
            print(e)
        else:
            db.commit()
    cur.close()
    db.close()


if __name__ == '__main__':



    url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start="
    heads = {
                "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8",
                "Accept - Encoding": "gzip, deflate",
                "Accept - Language": "zh - CN, zh;q = 0.8",
                "Cache - Control": "no - cache",
                "Connection": "keep - alive",
                "User - Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36"
    }

    start_n =3010
    urlStr = url + str(start_n)
    p = Pool (10)
    q = Manager().Queue()

    while True:
        urlStr = url+str(start_n)
        p.apply_async(func=fun,args=(urlStr,heads,q))
        start_n += 10
        # print(q.get())
        if start_n==5000:
            break


    p.close()
    p.join()

