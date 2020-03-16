# 抓取博客园或其他博客的文章
#
# Author: Wang Shiqiang
import requests

response = requests.get("https://www.baidu.com")
print(response.text)