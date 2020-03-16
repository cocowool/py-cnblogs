# 抓取博客园或其他博客的文章
#
# Author: Wang Shiqiang
import os, sys, getopt
import requests

# 入口函数，输入文章列表页地址后进行文件抓取
def main(argv):
    try :
        opts,args = getopt.getopt(argv,"hl:",["link="])
    except getopt.GetoptError:
        print("Usage: python3 main.py -l <blog_post_list_link>")

    for opt, arg in opts:
        if opt in ("-l", "--link"):
            parse_list(arg)
            pass
        else:
            print("Usage: python3 main.py -l <blog_post_list_link>")


def parse_list(url):
    response = requests.get("https://www.baidu.com")
    print(response.text)


if __name__ == "__main__":
    # print(__name__)
    main(sys.argv[1:])