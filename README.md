# Scraper
CourseAPI 開放式課程資訊匯流學院 爬蟲repo

![Scraper](https://i.imgur.com/frOE8GC.png)

## 注意！！！

本 repo 仍在開發中，僅完成國立台灣大學開放式課程、TOCEC 及中華開放教育平台

您可基於個人需求於 local 更改程式，但請勿做出侵權或違法的行為。

## 如何使用？

1. 下載 Python（這是最基本的xD）
2. 啟動 MongoDB（`sudo systemctl start mongod`）
3. `git clone https://github.com/Open-Edu-Tw/scraping.git`
   若有需要，可自行加上 Personal Access Token
3. `cd scraping`
4. `pip install -r requirements.txt`
5. `cd src/ocw`
6. `scrapy crawl <platform name>` 這裡 <platform name> 放 ntu/openedu/tocec
7. 可以進 MongoDB 看爬下來的資料啦！
