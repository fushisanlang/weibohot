import random
import configparser
import requests
import json


def ReadConf(section, itemKey):
    confFile = "./conf.ini"
    cf = configparser.ConfigParser()
    cf.read(confFile)
    ItenValue = cf.get(section, itemKey)
    return ItenValue


def GetColor():
    i = ['0', '1', '2', '3', '4', '5', '6',
         '7', '8', '9', 'a', 'b', 'c', 'e', 'f']
    x = 0
    ColorCode = '#'
    while x < 6:
        index = random.randint(0, 14)
        ColorCode = ColorCode + i[index]
        x = x + 1
    return ColorCode


def Alert(message):
    url = ReadConf("Qywx-Robot", "url")
    messagejson = {"msgtype": "text", "text": {"content": message}}
    messagejsondumps = json.dumps(messagejson)
    requests.post(url, messagejsondumps, headers={
                  'Content-Type': 'application/json;charset=utf-8'})
    return


