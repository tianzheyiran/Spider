import jsonpath,os,requests,time,UserAgent
from  lxml import etree

def getModelInfoByPageNum(num):
    ''' num 是想要获取的pageNum'''
    url = 'https://mm.taobao.com/tstar/search/tstar_model.do?'
    formdata = {'currentPage':num}
    headers = {'User-Agent': UserAgent.ua}
    resp = requests.post(url,headers=headers,data=formdata)
    info = resp.json()
    realName = jsonpath.jsonpath(info,'$..realName') #姓名的列表,用于后期创建文件夹以及图片命名用
    userId = jsonpath.jsonpath(info,'$..userId') #userId 用于拼接个人页面的url,获取个人页面的信息用
    return realName,userId

def getModelPage(userId):
    ''' 返回个人页面的Html代码'''
    url = 'https://mm.taobao.com/self/aiShow.htm?userId={}'
    headers = {'User-Agent': UserAgent.ua}
    resp = requests.get(url.format(userId),headers=headers)
    return resp.text

def getImageSrcList(html):
    e = etree.HTML(html)
    emglist = e.xpath('//div[@class="mm-aixiu-content"]//img/@src')
    # 获取到的图片地址是不带协议的,需要对地址进行处理,用于requests访问
    imgsrcList = []
    for src in emglist:
        imgsrc = 'http:' + src
        imgsrcList.append(imgsrc)
    return imgsrcList

def saveImg(url,filepath,imgName):
    ''' 通过请求,获取图片'''
    headers = {'User-Agent': UserAgent.ua}
    resp = requests.get(url, headers=headers)
    with open(filepath + '/'+imgName+'.jpg','wb') as f:
        f.write(resp.content)


def main(pageNum):
    for pn in range(1,pageNum + 1):
        #返回的realname,userId 是model的姓名和id列表
        realname,userId = getModelInfoByPageNum(pn)
        for id,name in zip(userId,realname):
            html = getModelPage(id) #返回的是某一个model的html
            imgsrclist = getImageSrcList(html)
            os.mkdir(name)
            n = 1
            for src in imgsrclist:
                count = n
                imgName = name + str(n)
                saveImg(src,name,imgName)
                n += 1
                time.sleep(0.01)

if __name__ == '__main__':
    main(3)
