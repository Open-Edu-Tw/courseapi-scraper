# Scraper
CourseAPI 開放式課程資訊匯流學院 爬蟲 repo

![Scraper](https://i.imgur.com/frOE8GC.png)

## 注意！！！

本 repo 仍在開發中，僅完成國立台灣大學開放式課程、TOCEC、中華開放教育平台以及學聯網

您可基於個人需求於 local 更改程式，但請勿做出侵權或違法的行為。

## 如何使用？

1. 下載 Python 和 Poetry（這是最基本的xD）
   1. [Python (3.10 或以上版本)](https://www.python.org/downloads/)
      1. Ubuntu 可以使用這個命令安裝：`sudo apt install python3.10 python3.10-distutils`  
      2. 更建議使用 pyenv 安裝 Python
   3. [Poetry](https://python-poetry.org/docs/)
2. 啟動 MongoDB
   1. Docker 可以直接執行 `docker run mongo` 
   2. Linux 可以：`sudo systemctl start mongod`
3. 複製本儲存庫
   1. 點下本儲存庫的右上角「Code」
   2. 選擇偏好方式（HTTPS 或 SSH）後執行裡面出現的命令
4. 之後輸入以下命令：
   ```shell
   cd Scraper       # 切換到 Scraper 工作目錄
   poetry install   # 安裝依賴關係
   
   # 這裡的 PlatformName 可以是 ntu/openedu/...
   # 詳見 ocw/spiders 資料夾裡面的檔案名稱
   poetry run scrapy crawl PlatformName
   ```
5. 可以進 MongoDB 看爬下來的資料啦！
