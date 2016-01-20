from digestLib import *

class SignUtils:
    @staticmethod
    def signBySortedMap(dictParam, method, signKey=''):
        keys=dictParam.keys()
        keys.sort()
        signedStr=''
        for key in keys:
            signedStr += '%s=%s&' % (key, dictParam[key])
        signedStr=signedStr[:-1]
        method=method.lower()
        if method=='md5':
            return DigestLib.md5(signedStr, signKey)
        elif method=='rsa':
            pass
        elif method=='ssh1':
            pass
