import urllib.request
import urllib.parse
import http.cookiejar

# 考试科目
examType = '13'
username = '000002471'
password = '1234'
# cookic处理
cookie_support = urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
urllib.request.install_opener(opener)
# 请求参数设置
params = urllib.parse.urlencode({'textname': username, 'password': password, 'n': '0', 'id': 'downloadQuestion'})
params = params.encode('utf-8')
# 模拟登陆操作
loginRequest = urllib.request.Request("http://webapp.hoperun.com:8190/Exam/welcomeAction.do")
urllib.request.urlopen(loginRequest, params)
# 模拟选题操作
chooseTypeRequest = urllib.request.Request("http://webapp.hoperun.com:8190/Exam/staffAction.do?examID="+examType+"&courseID="+examType)
urllib.request.urlopen(chooseTypeRequest)
# ----------------------------------------------------------------
getJsonRequest = urllib.request.Request("http://webapp.hoperun.com:8190/Exam/controller.jsp")
file = urllib.request.urlopen(getJsonRequest, params)
print(file.read().decode('utf-8'))
