import requests
import json
import random
import uuid
import time
import cv2
import numpy as np
from aesEncode import encryptAesEcb, decryptAesEcb
import base64

#项目还在调试勿用


current_time_seconds = time.time()
timestamp_milliseconds = int(current_time_seconds * 1000)







def login(phone,passwd,encrypted_token):
    url = "http://gwsxapp.gzzjzhy.com/api/user/login"
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6013 Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.101 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/30.47619)",
        "Content-Type": "application/json",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    data = {
        "phonenumber":phone,
        "password":passwd,
        "captchaVerification":encrypted_token
    }
    response = requests.post(url,data=json.dumps(data),headers=headers)
    print(response.json())
    return response.json()

def checkVerification(encryptedVerification,tokenCoordinateByte):
    url = "http://gwsxapp.gzzjzhy.com//captcha/check"
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6013 Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.101 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/30.47619)",
        "Content-Type": "application/json",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    data = {
        "captchaType":"blockPuzzle",
        "pointJson":encryptedVerification,
        "token":tokenCoordinateByte
    }
    response = requests.post(url,data=json.dumps(data),headers=headers)
    print(response.json())
    return response.json()
def captchaGget():
    url = "http://gwsxapp.gzzjzhy.com//captcha/get"
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6013 Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.101 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/30.47619)",
        "Content-Type": "application/json",
        "Content-Length": "106",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    data = {
        "captchaType":"blockPuzzle",
        "clientUid":f"slider-{uuid.uuid4()}",
        "ts":int(current_time_seconds * 1000)
    }

    response = requests.post(url,data=json.dumps(data),headers=headers)

    return response.json()


returnData = captchaGget()
def calculateOffset(originalImgBase64, jigsawImgBase64):
    originalEdge = cv2.Canny(cv2.imdecode(np.frombuffer(base64.b64decode(originalImgBase64), np.uint8), cv2.IMREAD_UNCHANGED), 100, 200)
    jigsawEdge = cv2.Canny(cv2.imdecode(np.frombuffer(base64.b64decode(jigsawImgBase64), np.uint8), cv2.IMREAD_UNCHANGED), 100, 200)

    _, _, _, offset = cv2.minMaxLoc(cv2.matchTemplate(originalEdge, jigsawEdge, cv2.TM_CCOEFF_NORMED))
    offset = offset[0]
    return f"{offset:.14f}"


secretKeyBytes = returnData["repData"]["secretKey"].encode('utf-8')
token = returnData["repData"]["token"].encode('utf-8')
originalImgBase64 = returnData["repData"]["originalImageBase64"]
jigsawImgBase64 = returnData["repData"]["jigsawImageBase64"]


xOffsetResult = calculateOffset(originalImgBase64,jigsawImgBase64)
coordinateBytes = json.dumps({"x": xOffsetResult, "y": 5}, separators=(',', ':'))

tokenCoordinateBytes = (token.decode('utf-8') + "---" + coordinateBytes).encode('utf-8')


encryptedVerification = encryptAesEcb(coordinateBytes.encode("utf-8"), secretKeyBytes)
# print(encryptedVerification)
captchaVerification = encryptAesEcb(tokenCoordinateBytes, secretKeyBytes)
# 验证码验证
checkVerification(encryptedVerification,token.decode('utf-8'))

phone = 10000000000000
passwd = "12345678"
login(phone,passwd,captchaVerification)
