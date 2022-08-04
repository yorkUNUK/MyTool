#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 依赖Crypto类库
# sudo pip3 install pycrypto  python3 安装Crypto
# API说明
# getEncryptedMap 生成回调处理成功后success加密后返回的json数据
# decrypt  用于接收到回调请求后

import io, base64, binascii, hashlib, string, struct, time
from random import choice

from Crypto.Cipher import AES

class Callback_python:
    def __init__(self, token, encodingAesKey, clientId):
        self.encodingAesKey = encodingAesKey
        self.clientId = clientId
        self.token = token
        self.aesKey = base64.b64decode(self.encodingAesKey + '=')

    ## 生成回调处理完成后的success加密数据
    def getEncryptedMap(self, content):
        encryptContent = self.encrypt(content)
        timeStamp = str(int(time.time()))
        nonce = self.generateRandomKey(16)
        sign = self.generateSignature(nonce, timeStamp, self.token,encryptContent)
        return {'msg_signature':sign,'encrypt':encryptContent,'timeStamp':timeStamp,'nonce':nonce}

    ##解密发送的数据
    def getDecryptMsg(self, msg_signature, timeStamp, nonce, content, msg_type):
        """
        解密
        :param content:
        :return:
        """
        sign = self.generateSignature(nonce, timeStamp, self.token, content, msg_type)
        if msg_signature != sign:
            raise ValueError('signature check error')

        content = base64.decodebytes(content.encode('UTF-8'))  ##返回的消息体

        iv = self.aesKey[:16]  ##初始向量
        aesDecode = AES.new(self.aesKey, AES.MODE_CBC, iv)
        decodeRes = aesDecode.decrypt(content)
        #pad = int(binascii.hexlify(decodeRes[-1]),16)
        pad = int(decodeRes[-1])
        if pad > 32:
            raise ValueError('Input is not padded or padding is corrupt')
        decodeRes = decodeRes[:-pad]
        l = struct.unpack('!i', decodeRes[16:20])[0]
        ##获取去除初始向量，四位msg长度以及尾部clientId
        nl = len(decodeRes)

        if decodeRes[(20+l):].decode() != self.clientId:
            raise ValueError('clientId 校验错误')
        return decodeRes[20:(20+l)].decode()

    def encrypt(self, content):
        """
        加密
        :param content:
        :return:
        """
        msg_len = self.length(content)
        content = ''.join([self.generateRandomKey(16) , msg_len.decode() , content , self.clientId])
        contentEncode = self.pks7encode(content)
        iv = self.aesKey[:16]
        aesEncode = AES.new(self.aesKey, AES.MODE_CBC, iv)
        aesEncrypt = aesEncode.encrypt(contentEncode)
        return base64.encodebytes(aesEncrypt).decode('UTF-8')

    ### 生成回调返回使用的签名值
    def generateSignature(self, nonce, timestamp, token, msg_encrypt, msg_type):
        signList = sorted([timestamp, token, msg_encrypt, msg_type, nonce])
        signString = ''.join(signList[:4])
        return hashlib.sha1(signString.encode()).hexdigest()


    def length(self, content):
        """
        将msg_len转为符合要求的四位字节长度
        :param content:
        :return:
        """
        l = len(content)
        return struct.pack('>l', l)

    def pks7encode(self, content):
        """
        安装 PKCS#7 标准填充字符串
        :param text: str
        :return: str
        """
        l = len(content)
        output = io.StringIO()
        val = 32 - (l % 32)
        for _ in range(val):
            output.write('%02x' % val)
        # print "pks7encode",content,"pks7encode", val, "pks7encode", output.getvalue()
        return content + binascii.unhexlify(output.getvalue()).decode()

    def pks7decode(self, content):
        nl = len(content)
        val = int(binascii.hexlify(content[-1]), 16)
        if val > 32:
            raise ValueError('Input is not padded or padding is corrupt')

        l = nl - val
        return content[:l]


    def generateRandomKey(self, size,
                          chars=string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase + string.digits):
        """
        生成加密所需要的随机字符串
        :param size:
        :param chars:
        :return:
        """
        return ''.join(choice(chars) for i in range(size))




if __name__ == '__main__':
    # 组装你的的开发者信息    Callback_python(token, encodingAesKey, clientId)
    test = Callback_python("Q5WYPc", "shR2GFpZHWCnyps2WsHBsQK2Gm5DS2r7SBd3byPPEi4", "1626074470012587260")

    #组装你的加密信息  test.getDecryptMsg(msg_signature, timeStamp, nonce, content, msg_type)
    text = test.getDecryptMsg("6a3d8de520c8328108f24665ae16829584dafa94", "1656929204242", "IuLBSQrN", 'JYCzpnhOjicSfwlESMs5ezC7Abbq/aqU7+cEOMZa1IZHTLdtiby1Qh6KkT8CT76d1+r+XleECm9mRvtsm2TEdqnKCShhEH3X1bCaDlaO9Q0jx+Bq18mYpz4+3Sq6tpeHkHQyTPd5eVfw6Gp3ZjdgdGR1xjHW7rlpMmL0LoJ3nUUBtSv+V8v04WUsqzaghTMuETWhW8OXjDgM9+HG00JqYBERmGFS63E0EpBbwTkAu+65B7kEuHU+o0j49D7HRksa/w9Lqg+B791rnfn4nEyhDfFiEDgMGMVtt2fWrnc2yhkNW9zIt/epF6xfl/t4PzBsgibglFx0lAxpu3uCDp4Y9f85FDmdJaVFb3aMBFXjEAsFoENpBY/QPbFIobllEh9i', "CONTRACT_SEND_RESULT")
    print(text)