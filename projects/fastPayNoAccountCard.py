import os
import json
from MyLib import util
from MyLib import BaseResponseProcessor
from MyLib import FileWrapper

class FastPayNoAccountCard(BaseResponseProcessor):
    def getResponse(self, requestDict, expectationDict):
        if expectationDict is None:
            expectationDict={}

        for value in expectationDict.values():
            if value.find('EXCEPTION') >=0:
                print 'Raise an exception to match expectation'
                raise Exception('Raise exception')

        merchId=expectationDict.get('merchId', '0000323')
        actSttlmAmt=expectationDict.get('actSttlmAmt', '100.00')
        bizId=expectationDict.get('bizId', '20150908112353201')
        authId=expectationDict.get('authId', '010258911150722185225155BLLAmrYer')
        signInfo=expectationDict.get('signInfo', '7da3d117188e94c2dcdd38fd2df45c9a')
        state=expectationDict.get('state', '02')
        txId=expectationDict.get('txId', 'CEX150819141309187461368552')
        amount=expectationDict.get('amount', '100.00')
        respDescription=expectationDict.get('respDescription', 'success')
        bankId=expectationDict.get('bankId', '0104')
        cardTp=expectationDict.get('cardTp', '01')
        paymentTp=expectationDict.get('paymentTp', '02')
        classObj=expectationDict.get('class', 'com.creditease.ns.adapter.fastpay.data.FastPayNoAccountCardResponse')
        completeTime=expectationDict.get('completeTime', util.date2Str(format='%Y%m%d%H%M%S'))
        respCode=expectationDict.get('respCode', '100001')

        resDict={}
        resDict['merchId']=merchId
        resDict['actSttlmAmt']=actSttlmAmt
        resDict['bizId']=bizId
        resDict['authId']=authId
        resDict['signInfo']=signInfo
        resDict['state']=state
        resDict['txId']=txId
        resDict['amount']=amount
        resDict['respDescription']=respDescription
        resDict['bankId']=bankId
        resDict['cardTp']=cardTp
        resDict['paymentTp']=paymentTp
        resDict['classObj']=classObj
        resDict['completeTime']=completeTime
        resDict['respCode']=respCode
        
        jsonStr=json.dumps(resDict)
        return jsonStr
        
