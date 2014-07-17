import os
import json
import urllib.request
import urllib.parse
import http.cookiejar


# 根据问题对象返回答案选项
def changeObjIntoInfo(jsonObj):
    # 26个字母
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # 一个json.txt文档的结果列表
    resultList = []
    for question in jsonObj:
        # 问题答案字典
        questionResut = {}
        # 选项数
        optionsLen = len(question['OPTIONS'])
        # 原始答案字符串 A:2^0 B:2^1 C:2^2 D:2^3以此类推，答案为数字之和
        answerStr = question['QUESTION']['ANSWER']
        # 原始字符串转换为二进制字符串
        answerStr = str(bin(int(answerStr))[2:])
        # 补全位数
        answerNum = ''.join(reversed('0' * (optionsLen - len(answerStr)) + answerStr))
        # 答案选项
        finalAnswer = ''
        for isCorrectIndex in range(len(answerNum)):
            if(int(answerNum[isCorrectIndex])):
                finalAnswer += ',' + letters[isCorrectIndex]
        questionResut['A_CONTENT'] = question['QUESTION']['CONTENT']
        questionResut['B_ANSWER'] = finalAnswer[1:]
        questionResut['C_OPTIONS'] = []
        for index in range(len(question['OPTIONS'])):
            questionResut['C_OPTIONS'].append(letters[index] + ":" + question['OPTIONS'][index]['CONTENT'])
        resultList.append(questionResut)
    return resultList


# 去除列表中重复字典
def uniqueList(L):  
    (output, temp) = ([],[])  
    for l in L:  
        for k, v in l.items():  
            flag = False  
            if (k,v) not in temp:  
                flag = True  
                break  
        if flag:  
            output.append(l)  
        temp.extend(l.items())  
    return output


# 爬虫爬取题目json方法 examType:考试科目编号
def getQuestionJson(examType):
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
    return file.read().decode('utf-8')


# 根据考试类型下载试题方法
def getQuestionByType(examType):
    # 无重复的结果字典列表
    resultList = []
    # 下载次数
    downloadNum = 1
    # 下载0题的次数
    noneDownload = 0
    for getTimeNum in range(downloadNum):
        print('-------- 第'+str(getTimeNum+1)+'次下载试题开始 --------')
        # 对象json
        jsonStr = getQuestionJson(examType)
        # 将json转换为原生py对象
        jsonObj = json.loads(jsonStr)
        # 下载前试题数
        beforeSize = len(resultList)
        # 合并试题集合
        resultList.extend(changeObjIntoInfo(jsonObj))
        # 去重复
        resultList = uniqueList(resultList)
        # 下载后试题数
        afterSize = len(resultList)
        print('-------- 已下载'+str(afterSize - beforeSize)+'题新试题 --------')
        # 连续5次无下载题，停止下载
        if(0 == (afterSize - beforeSize)):
            noneDownload += 1
            if(5 == noneDownload):
                break
        else:
            noneDownload = 0
    return resultList


examTypeMap = {
    '1':'信息安全管理规定',
    '2':'CMMI项目开发章程（设计类）',
    '3':'CMMI项目开发章程（开发类）',
    '4':'CMMI项目开发章程（测试类）',
    '5':'项目开发章程&现场作业管理章程（项目管理）',
    # '6':'测试-Web应用',
    # '7':'测试-移动应用',
    # '8':'测试-整机测试',
    # '9':'开发-Andriod',
    # '10':'应届生',
    # '11':'开发-dotnet',
    # '12':'开发-IOS',
    # '24':'开发-Java',
    # '14':'开发-C',
}


for typeNum in examTypeMap:
    with open('/Users/Fantasy_Elf/' + examTypeMap[typeNum] + '.txt','w',encoding='GBK') as f:
        f.write(json.dumps(getQuestionByType(typeNum), sort_keys=True, indent=1, ensure_ascii=False))
