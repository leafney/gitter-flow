### spider



#### 分析

1. 通过Pyppeteer获取第一页的数据，从第一页中得到最新的一个id值
2. 将该id值作为接口请求中的beforeid值，传入
3. 测试发现接口请求中，请求头中必须带有参数`x-access-token`，而该token值可以从第一页页面中通过正则匹配得到
4. 测试发现接口请求中，cookie不是必需的
5. token值有一定期限，但具体多长时间待测试


#### 问题

> [W:pyppeteer.chromium_downloader] start chromium download.
Download may take a few minutes.

默认 `await pyppeteer.launch()` 会下载chromium浏览器，需要指定本地已安装的浏览器地址。

```
# EXECPATH = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome' # 这样在js中可以，但在py中不行
EXECPATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # 这样可以，中间的空格不用转义

pyppeteer.launch({
        'executablePath':EXECPATH,
        })

```


> pyppeteer.errors.NetworkError: Protocol error Page.navigate: Target closed.

当网页请求超时时，容易出现该问题。暂未找到解决方法。


