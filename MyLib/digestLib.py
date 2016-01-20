# coding: UTF-8
import hashlib
class DigestLib(object):
    @staticmethod
    def md5(srcStr,signKey=""):
        
        md5=hashlib.md5()
        md5.update(srcStr)
        if signKey!="":
            md5.update(signKey)
        dest=md5.hexdigest()
        print dest

if __name__=="__main__":
    srcStr='bankCity=001&bankCode=0104&bankName=中国人民银行&bankProv=111&bgRet=http://www.creditease.cn/bg/superAccount&bizCode=yixin&cardNo=6226620208536870&cardType=1&customerName=张三&idNo=62112519880317230x&idType=111&merchantCode=superAccTeam&orderNo=20150824080623383&orderTime=20150824080623&pageRet=http://www.creditease.cn/fg/superAccount&source=01&userId=20150824080622498&userIp=127.0.0.1&version=20150616&withdrawAmount=100.00'
    #srcStr='bizCode=yixin&merchantCode=superAccTeam&orderNo=20150824080623383&version=20150616'
    signKey='securityKey001'
    SignUtils.md5(srcStr,signKey)
