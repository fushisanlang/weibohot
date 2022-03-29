from wordcloud import WordCloud
import PIL.Image as image
import numpy as np
import jieba
from OperacteData import selectOperaction
import datetime
from Tools import ReadConf


def transCN(text):
    # 接收分词的字符串
    word_list = jieba.cut(text)
    # 分词后在单独个体之间加上空格
    result = " ".join(word_list)
    return result


def wordPic(SelectTime):
    # 读取数据
    month = SelectTime[:6]
    startTime = datetime.datetime.strptime(SelectTime, "%Y%m%d")
    endTime = startTime+datetime.timedelta(days=1)
    tempStr = ''
    sqlString = 'select node  FROM weibohot_' + month + ' where time between \'' + startTime.strftime(
        '%Y-%m-%d') + '\' and \'' + endTime.strftime('%Y-%m-%d') + '\' '
    sqlResult = selectOperaction(sqlString)
    for node in sqlResult:
        tempStr = tempStr+node[0]+' '
    text = transCN(tempStr)
    mask = np.array(image.open("templates/template.png"))
    replaceList = list(ReadConf('Run-Conf', 'replaceList'))
    for replaceWord in replaceList:
        text = text.replace(replaceWord, '')

    wordcloud = WordCloud(
        scale=8,
        # 添加遮罩层
        mask=mask,
        # 生成中文字的字体,必须要加,不然看不到中文
        font_path="/System/Library/Fonts/STHeiti Light.ttc"
    ).generate(text)
    image_produce = wordcloud.to_image()
    image_produce.save("pics/" + SelectTime + ".png")

def WordPic():
    todayDate = datetime.datetime.now()
    yesterdayDate=todayDate-datetime.timedelta(days=1)
    yesterdayDateStr=yesterdayDate.strftime("%Y-%m-%d")
    wordPic(yesterdayDateStr)
