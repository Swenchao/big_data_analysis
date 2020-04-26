# big_data_analysis

## 链家二手房交易信息爬虫（lianjia_spider）

使用scrapy框架爬取链家二手房交易信息，存储到mysql数据库中（注意需要首先创建数据库：lianjia）

1. 使用了orm，所以需要根据自己环境配置model环境（创建lianjia数据库，表会自动创建）

2. 下载安装python并配置环境

3. pip install requirements.txt 安装依赖

4. 运行爬虫
	① scrapy crawl lianjia  运行爬虫（数据存储到数据库中）
	② scrapy crawl lianjia -o info.csv -t csv  运行爬虫（数据存储成csv文件）

>待续...