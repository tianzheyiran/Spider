from lxml import etree
from selenium import webdriver
import time
import pymysql

def writeIntoDb(companys, locations, jobpositions, treatments):
    conn = pymysql.connect(host="localhost", user="root", password="123456", db="lagou", charset="utf8")
    cursor = conn.cursor()
    for cp, lc, jp, tt in zip(companys, locations, jobpositions, treatments):
        sql = "INSERT INTO lagou (company, location, jobposition, treatment) VALUES('%s', '%s', '%s', '%s')"%(cp, lc, jp, tt)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()

def getInfo(key,nums=100):
    driver = webdriver.Chrome()
    driver.get('https://www.lagou.com/jobs/list_?city=%E5%8C%97%E4%BA%AC')
    driver.find_element_by_id('keyword').send_keys(key)
    driver.find_element_by_id('submit').click()
    n = 1
    while True:
        print('正在获取第%s页的信息'% n)
        # if n == 100:
        #     break
        time.sleep(2)
        e = etree.HTML(driver.page_source)
        companys = e.xpath('//div[@class="company_name"]/a/text()')
        locations = e.xpath('//span[@class = "add"]/em/text()')
        jobpositions = e.xpath('//div[@class = "list_item_top"]//h3/text()')
        treatments = e.xpath('//span[@class="money"]/text()')
        # with open("拉钩搜索.txt",'a',encoding='utf-8') as f:
        #     for cp, lc, jp, tt in zip(companys, locations, jobpositions, treatments):
        #         f.write(cp + "\t" + lc + "\t" + jp + "\t" + tt + "\n")
        print("正在保存第%s页的信息到数据库"% n)
        writeIntoDb(companys, locations, jobpositions, treatments)
        if driver.page_source.find('pager_next_disabled') == -1:
            driver.find_element_by_class_name('pager_next').click()
        else:
            break
        n+=1
    driver.close()

if __name__ == '__main__':
    getInfo("python")