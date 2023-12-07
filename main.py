import requests
import json
import random
import uuid
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


import base64
import random

#目前还差验证码坐标获取
#项目还在调试勿用


current_time_seconds = time.time()
timestamp_milliseconds = int(current_time_seconds * 1000)




def encrypt_aes(plaintext, key):
    aes = AES.new(key, AES.MODE_ECB)
    padded_data = pad(plaintext, AES.block_size)
    ciphertext = aes.encrypt(padded_data)
    encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return encoded_ciphertext

def decrypt_aes(ciphertext, key):
    aes = AES.new(key, AES.MODE_ECB)
    encrypted_data = base64.b64decode(ciphertext)
    decrypted_data = aes.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode("utf-8")


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
    print(encryptedVerification)
    print(tokenCoordinateByte)
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



# 给定的密文和密钥
# ciphertext = b"ZKHO/QX3AL4R/7tTthmTvI0L5369XzpCKx30VBE9kg0="
# ciphertext = b"Jw/34CLVbYs/BoPuVAsQl8pVz8FZ2oUGdSgLC0ouFVGQjzEvu8G73hzClOfS8oo2"
ciphertext = b"yJ9ZFg2+Ug6B52s99hijHtKYJtRHxDolHCtIsRxbEtY="
key = b"0Ry4Rnby1JT0050j"
print(1)
print(decrypt_aes(ciphertext,key))


# coordinateBytes = json.dumps({"x": random.uniform(140, 230), "y": 5})
coordinateBytes = json.dumps({"x": random.uniform(140, 230), "y": 5}, separators=(',', ':')).encode('utf-8')

print(2)
print(coordinateBytes)
# tokenCoordinateBytes = (returnData["repData"]["token"] + "---" + coordinateBytes).encode('utf-8')
tokenCoordinateBytes = (returnData["repData"]["token"] + "---" + coordinateBytes.decode('utf-8')).encode('utf-8')

# print("token")
# print(tokenCoordinateBytes)

secretKeyBytes = returnData["repData"]["secretKey"].encode('utf-8')
# print("key")
# print(secretKeyBytes)
encryptedVerification = encrypt_aes(tokenCoordinateBytes, secretKeyBytes)

encryptedTokenVerification = encrypt_aes(tokenCoordinateBytes, secretKeyBytes)
# print("密文")


print(coordinateBytes)
tokenCoordinateByte = returnData["repData"]["token"]

# 验证码验证
checkVerification(encryptedVerification,tokenCoordinateByte)
# 登录

phone = 11111111111111111
passwd = 1234567
# login(phone,passwd,encryptedTokenVerification)

