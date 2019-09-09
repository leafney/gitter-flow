#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------
  File Name  : run.py
  Description: 
  Author     : xue
  Date       : 2019/9/9
-------------------------------
"""


import asyncio
import re
import time
import requests
import pyppeteer

# EXECPATH = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome' # 这样在js中可以，但在py中不行
EXECPATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # 这样可以，中间的空格不用转义


async def main():

    url='https://gitter.im/drone/drone'
    # url='http://gitter.im/vuejs/vue'
    # url='https://www.baidu.com/'
    # url='https://ip.cn/'

    browser=await pyppeteer.launch({
        'executablePath':EXECPATH,
        'headless':False,
        'args':['--no-sandbox',
            '--disable-dev-shm-usage',
            '--proxy-server=socks5://127.0.0.1:1080', # 设置代理
        ],
        'slowMo': 10,
    })

    page=await browser.newPage()

    # 设置页面视图大小
    await page.setViewport(viewport={'width':1280, 'height':800})

    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')


    # 是否启用JS，enabled设为False，则无渲染效果
    # await page.setJavaScriptEnabled(enabled=True)

    # await page.goto(url)
    await page.goto(url, {
        'timeout': 30000,
        # 'waitUntil': 'networkidle0',
        'waitUntil': 'domcontentloaded',
    })

    # 等待
    await page.waitFor(5000)

    # 屏幕截图
    # await page.screenshot({'path':'test.png'})

    # 打印当前页标题
    print(await page.title())

    # 打印页面文本
    # print(await page.content())
    html=await page.content()

    # 打印页面cookies
    cookis=await page.cookies()
    print(cookis)

    cook_dict={}
    for ck in cookis:
        cook_dict[ck['name']]=ck['value']
    print(cook_dict)

    # 通过xpath找到每一项
    xpath_str = '//div[@id="chat-container"]//div[starts-with(@class,"chat-item model-id-")]//a[contains(@class,"js-chat-time")]'

    chat_items=await page.xpath(xpath_str)

    res_list=[]
    for item in chat_items:
        link_str=await (await item.getProperty('href')).jsonValue()
        # print(link_str)
        # 截取得到
        link= link_str.split('=')[-1]
        res_list.append(link)

    # 获取到结果
    print('result: \n',res_list)


    # 通过正则找到accesstoken
    sres=re.search(r'\{\"accessToken\"\:\"(.*?)\",',html)
    print(sres.group())
    token=''
    tokenGroup=sres.group()
    if len(tokenGroup)>0:
        token= sres.group(1)

    print(token)



    await browser.close()

    print('done')



    # 请求api载入更多页数据
    time.sleep(5)
    searchId=res_list[-1]

    loadMorePage(searchId,38,cook_dict,token)



# 5d750852460a6f5a16e94241
# 5d72c94db3e2fc579366c017

def loadMorePage(searchId,count,cookies,token):

    url='https://gitter.im/api/v1/rooms/5bdc942fd73408ce4fadad37/chatMessages'
    params={
        'lookups[]':'user',
        'beforeId': searchId,
        'limit': count,
    }

    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/70.0.3538.67 Safari/537.36',
        'Host': 'gitter.im',
        'Referer': 'https://gitter.im/drone/drone',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'x-access-token': token,   #'$FozXdHdID/j7v++Mj9wHAt8BEro/Qbmq4Lbax0SFM0U=',
    }

    # 经验证，cookie不是必需的
    r=requests.get(url=url,params=params,headers=headers,verify=False)

    jsonData=r.json()
    print(jsonData)



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

    # loadMorePage('5d72d1cf6e889c4bbdaf4b6c',38)