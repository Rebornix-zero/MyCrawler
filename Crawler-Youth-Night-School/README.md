# Crawler for youth night school

## 如何使用

1. 在当前目录下运行`crawler_*.py`文件，以爬取相关帖子的最新评论，保存在`./comments`文件夹下
2. 在当前目录下运行`word_cloud.py`文件，以生成相关的词云图，保存为`./comments/word_cloud.png`图片
3. 可以在对应的程序源码中配置部分常量及配置，如索要摘取的话题 id，词云图停用词等等
4. 微博网页版爬虫无查询能力，需要人工搜索，找到对应帖子的 id，再让其爬取；而小红书网页版具备查询能力，可以根据查询结果，选定前 n 个热门帖子，进而获取帖子中的评论

## 注意

1. 不要在 VPN 启动时进行爬取，否则网络包的转发将会报错。注意这并非不可解决的问题，只是因为暂未查看 clash 的代理机制而暂未处理（懒）
2. 本项目需要部分模块依赖，请参考`./requirements.txt`自行安装
3. `./crawler_weibo.py`文件中的 Cookie 字段，`./crawler_xiaohongshu.py`文件中的 cookie 结构体，header 中的 x-s，x-t 字段会失效，data 数据字段，届时需要重新从浏览器中获取最新数据，并放入对应位置更新
