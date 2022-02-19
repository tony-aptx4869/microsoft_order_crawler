# Microsoft Order Crawler

Python scripts for crawling Microsoft orders information.

用来爬虫Microsoft订单信息的Python脚本。

## What you need? | 你需要什么？

The only two strings you need are `__RequestVerificationToken` in HTTPS request's header and `AMCSecAuth` in Cookie.

您需要的唯一两个字符串是 HTTPS 请求标头中的 `__RequestVerificationToken` 和 Cookie 中的 `AMCSecAuth`。

## How to use? | 如何使用

Step 1: Get your own `__RequestVerificationToken` and `AMCSecAuth`

Step 2: Copy the file `config.example.conf` and rename it as `config.conf`

Step 3: Set your own `__RequestVerificationToken` and `AMCSecAuth` values in the file `config.conf`

Step 4: Run the script `main.py` and the results, a csv file, will be saved in the directory `csv_files/[DATE_TODAY]` with the filename format as `csv_file_[TIME_NOW]`

第 1 步：获取自己的 `__RequestVerificationToken` 和 `AMCSecAuth`

第 2 步：复制文件 `config.example.conf` 并将其重命名为 `config.conf`

第 3 步：在文件 `config.conf` 中设置您自己的 `__RequestVerificationToken` 和 `AMCSecAuth` 值

第 4 步：运行脚本 `main.py`，结果，一个 csv 文件，将保存在目录 `csv_files/[DATE_TODAY]` 中，文件名格式为 `csv_file_[TIME_NOW]`
