import blogreporter as br

# 支持自动抓取博客园文章，并生成Markdown格式的年度报告
br = br.generate('https://www.cnblogs.com/cocowool', '2020')
br.run()

