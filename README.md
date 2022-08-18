# Scraper
CourseAPI 開放式課程資訊匯流學院 爬蟲 repo

![Scraper](https://i.imgur.com/frOE8GC.png)

## 注意！！！

本 repo 仍在開發中，僅完成國立台灣大學開放式課程、TOCEC、中華開放教育平台以及學聯網

您可基於個人需求於 local 更改程式，但請勿做出侵權或違法的行為。

## 開發

### Gitpod

您可以使用 Gitpod，使用我們預先配置好的環境，直接在雲端主機上進行開發。使用 Gitpod 就不需要自行設定 MongoDB、Python 3.10 以及 Poetry。
使用 Gitpod 可以省下很大的環境配置時間，惟您可能需要注意 Gitpod 的 `Remaining hours` 開發時間限制。

[![在 Gitpod 開啟](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Open-Edu-Tw/Scraper)

### 自行配置

1. 下載 Python 和 Poetry（這是最基本的xD）
   1. [Python (3.10 或以上版本)](https://www.python.org/downloads/)
      1. Ubuntu 可以使用這個命令安裝：`sudo apt install python3.10 python3.10-distutils`  
      2. 更建議使用 pyenv 安裝 Python
   2. [PDM](https://pdm.fming.dev)
2. 啟動 MongoDB
   1. Docker 可以直接執行 `docker run mongo` 
   2. Linux 可以：`sudo systemctl start mongod`
3. 複製本儲存庫
   1. 點下本儲存庫的右上角「Code」
   2. 選擇偏好方式（HTTPS 或 SSH）後執行裡面出現的命令
4. 之後輸入以下命令：
   ```shell
   cd Scraper       # 切換到 Scraper 工作目錄
   pdm install      # 安裝依賴關係
   
   # 這裡的 PlatformName 可以是 ntu/openedu/...
   # 詳見 ocw/spiders 資料夾裡面的檔案名稱
   pdm run crawl PlatformName
   ```
5. 可以進 MongoDB 看爬下來的資料啦！
