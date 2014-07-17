hoperuntest
===========
江苏润和职级在线考试试题爬虫
-----------
### ./html:
	test_no_ie.html —— 去除IE限制的html静态文件，让chrome可以访问考试系统，方便调试
	test.html —— 原登陆页面直接command+s
	BaseTool.js —— 原页面JS
	Startexam.js —— 原页面JS
### ./py:
	get_html.py —— 初版爬虫，只能爬一次一科50题
	get_question.py —— 最终版爬虫，根据配置爬出所有配置科目的所有不重复题目及答案
	xxx.py —— 根据二进制数计算答案核心算法
### ./result:
	*.txt —— 对应科目试题及答案，文本格式为json

fuck hoperun! fuck exam!
-----------
