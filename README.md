### gitter-flow

#### 描述

实现 `gitter.im` 中历史聊天记录的信息流


#### Todo

* [x] spider-通过Pyppeteer请求gitter首页并获取页面中的最新id
* [x] spider-测试通过api接口请求历史消息集合
* [ ] spider-优化实现分页请求api接口历史消息
* [ ] spider-对历史消息数据的解析及入库操作
* [ ] spider-spider功能封装
* [ ] web-通过Flask实现gitter历史消息显示
* [ ] web-实现浏览记忆功能，标记上次看到哪里
* [ ] web-实现Docker容器化部署
