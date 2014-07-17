import os
import json


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
        questionResut['CONTENT'] = question['QUESTION']['CONTENT']
        questionResut['ANSWER'] = finalAnswer[1:]
        questionResut['OPTIONS'] = []
        for index in range(len(question['OPTIONS'])):
            questionResut['OPTIONS'].append(letters[index] + ":" + question['OPTIONS'][index]['CONTENT'])
        resultList.append(questionResut)
    return(resultList)


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


# 文件路径根目录
jsonFileDir = 'C:\\Users\\zhang_jiayang\\Desktop\\test\\json\\java'
# 每个文件对应绝对路径
filePathList = []


for fileObj in os.walk(jsonFileDir):
    # 存在文件名
    if(fileObj[2]):
        # 循环文件名
        for fileName in fileObj[2]:
            # 拼接绝对路径，添加到列表中
            filePathList.append(fileObj[0] + '\\' + fileName)


# 无重复的结果字典列表
resultList = []


# 循环文件绝对路径列表                     
for filePath in filePathList:
    # 对象json
    jsonStr = ''
    # 读取txt文件中json
    with open(filePath,'r',encoding='utf-8') as file:
        while True:
            line = file.readline()
            if not line:
                break
            # 拼接json
            jsonStr += line.strip()


    # 将json转换为原生py对象
    jsonObj = json.loads(jsonStr)
    resultList.extend(changeObjIntoInfo(jsonObj))


resultList = uniqueList(resultList)
print(len(resultList))
