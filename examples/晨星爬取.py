# -*- coding: utf-8 -*-

import sys
from lxml import etree
import time
import random
import requests
import json
import csv
from selenium import webdriver   # 导入webdriver模块
from bs4 import BeautifulSoup
from time import sleep


class ChengxingspiderItem:
    def __init__(self):
        self.fund_code = ""
        self.fund_name = ""
        self.fund_price = ""
        self.category = ""
        self.inception = ""
        self.subscribe = ""
        self.redeem = ""
        self.sbdesc = ""
        self.sharprate = ""
        self.date = ""
        self._i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._i == 0:
            self._i += 1
            return self.fund_code
        elif self._i == 1:
            self._i += 1
            return self.fund_name
        elif self._i == 2:
            self._i += 1
            return self.fund_price
        elif self._i == 3:
            self._i += 1
            return self.category
        elif self._i == 4:
            self._i += 1
            return self.sharprate
        elif self._i == 5:
            self._i += 1
            return self.date
        else:
            raise StopIteration()


class FundSpider():
    name = 'fund'
    allowed_domains = ['cn.morningstar.com/quicktake/']
    # fund_list = ['0P0000Z821', 'F0000003VJ', '0P00016WFU', 'F000000416', 'F0000004AI',
    #             '0P00015HFT', 'F0000003ZX', '0P000147K8', '0P0000P5UD', '0P0001606X']
    fund_list = ['0P0000RU7I', '0P0000S0NU', '0P0000XBF0', '0P0000YXTA', '0P0000Z5JW', '0P0000ZEAH', '0P00015WGK', '0P0001606X', '0P000160TK', '0P00016A08', '0P00016DKC',
                 '0P00016FT6', '0P000178CP', '0P00018J2K', '0P00018KU4', '0P0001ABM2', '0P0001D6IU', '0P0001F1K9', '0P0001FDKQ', 'F0000003VJ', 'F0000004AI', 'F0000004JE']

    start_urls = [
        f'http://cn.morningstar.com/quicktake/{page}' for page in fund_list]

    # json_url = 'http://cn.morningstar.com/handler/quicktake.ashx'
    url = 'http://cn.morningstar.com/handler/quicktake.ashx'
    webUrl = 'http://cn.morningstar.com/quicktake/'

    def parse(self, response):

        # 把网页变成xpath结构
        fund_xpath = etree.HTML(response)
        item = ChengxingspiderItem()

        fund_name = fund_xpath.xpath('//*[@id="qt_fund"]/span[1]/text()')
        fund_price = fund_xpath.xpath(
            '//*[@id="qt_base"]/ul[1]/li[2]/span/text()')
        date = fund_xpath.xpath('//*[@id="qt_base"]/ul[1]/li[3]/text()')

        category = fund_xpath.xpath(
            '//*[@id="qt_base"]/ul[3]/li[7]/span/text()')
        sharprate = fund_xpath.xpath('//*[@id="qt_risk"]/li[30]/text()')

        item.fund_code = fund_name[0][:6]
        item.fund_name = fund_name[0][7:]
        item.fund_price = fund_price[0]
        if len(category) != 0:
            item.category = category[0]
        if len(sharprate) != 0:
            item.sharprate = sharprate[0]

        item.date = date[0][5:]

        print(item.fund_code)
        print(item.fund_name)
        print(item.fund_price)
        print(item.category)
        print(item.sharprate)

        # print(len(date[0]))
        # print(type(item['date']))
        # print(type(fund_price))
        # print(dir(fund_price))
        # print(len(str(date)))
        # print(str(date)[-12:-1])
        return list(item)


if __name__ == '__main__':

    # headers = {'User-Agent':
    #           'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    #           'Host': 'cn.morningstar.com'
    #          }
    fs = FundSpider()

    # 指定chrom的驱动
    # 执行到这里的时候Selenium会到指定的路径将chrome driver程序运行起来
    # driver = webdriver.Chrome('./chromedriver/chromedriver.exe')
    # driver = webdriver.Firefox()#这里是火狐的浏览器运行方法

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        './chromedriver/chromedriver.exe', chrome_options=options)

    cookies = ''
    headers = ['fund_code', 'fund_name',
               'fund_price', 'category', 'sharprate', 'date']
    rows = [

    ]

    for urlitem in fs.start_urls:
        # soup = BeautifulSoup(html_doc, 'html.parser')
        if(cookies == ''):
            # 可以通过 id 获取 form 表单
            driver.get(urlitem)
            username = driver.find_element_by_id('emailTxt')
            password = driver.find_element_by_id('pwdValue')
            username.send_keys('***********@qq.com')
            password.send_keys('w*************')
            submit = driver.find_element_by_id('loginGo')
            submit.click()
            sleep(1)
            # 获取网站cookie
            # 获取网站cookie
            cookies = driver.get_cookies()
        else:
            # driver.add_cookie(cookies)
            driver.get(urlitem)
        singlerow = fs.parse(driver.page_source)
        rows.append(singlerow)
        # reobj = requests.get(urlitem, headers=headers)  # 对HTTP响应的数据
        # fs.parse(reobj)

    with open('test.csv', 'w', newline='')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)