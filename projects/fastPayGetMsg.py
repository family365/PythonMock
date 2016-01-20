import os
import json
from MyLib import util
from MyLib import BaseResponseProcessor
from MyLib import FileWrapper


class FastPayGetMsg(BaseResponseProcessor):
    def getResponse(self, requestDict, expectationDict):
        if expectationDict is None:
            expectationDict={}

        for value in expectationDict.values():
            if value.find('EXCEPTION') >=0:
                print 'Raise an exception to match expectation'
                raise Exception('Raise exception')

        merchId=expectationDict.get('merchId', 'superAccTeam')
        respDescription=expectationDict.get('respDescription', 'success')
        respCode=expectationDict.get('respCode', '0032')
        respId=expectationDict.get('respId', '10016046641375293440')
        userID=expectationDict.get('userID', '1234')
        tokenCd=expectationDict.get('tokenCd', '08121636400020Rfi7TQeNWu')
        smsFlag=expectationDict.get('smsFlag', None)
        paymentTp=expectationDict.get('paymentTp', '11')
        bankId=expectationDict.get('bankId', '0104')

        resDict={}
        resDict['merchId']=merchId
        resDict['respDescription']=respDescription
        resDict['respCode']=respCode
        resDict['respId']=respId
        resDict['userID']=userID
        resDict['tokenCd']=tokenCd
        resDict['smsFlag']=smsFlag
        resDict['paymentTp']=paymentTp
        resDict['bankId']=bankId

        jsonStr=json.dumps(resDict)
        return jsonStr
        
