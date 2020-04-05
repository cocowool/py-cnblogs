# 支持将html内容转换为markdown格式文档
# Author: Wang Shiqiang
# Date: 2020/03/29

__author__ = "Wang Shiqiang"
__version__ = "0.0.1"

from bs4 import BeautifulSoup
import re
import sys

from .html2markdown import html2markdown
from .blog2html import blog2html

