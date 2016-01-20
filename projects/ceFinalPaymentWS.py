import os
import json
from MyLib import util
from MyLib import BaseResponseProcessor
from MyLib import FileWrapper
from xml.dom.minidom import Document

class CeFinalPaymentWS(BaseResponseProcessor):
    def __init__(self):
        self.doc=Document()
        
    def getResponse(self, requestDict, expectationDict):
        if expectationDict is None:
            expectationDict={}

        for value in expectationDict.values():
            if value.find('EXCEPTION') >=0:
                print 'Raise an exception to match expectation'
                raise Exception('Raise exception')
            
        
        envelope=self.__createElement('soap:Envelope', parentNode=self.doc, attrDict={"xmlns:soap":"http://schemas.xmlsoap.org/soap/envelope/"})
        body=self.__createElement('soap:Body', parentNode=envelope)
        response=self.__createElement('ns1:singlePaymentResponse', parentNode=body, attrDict={"xmlns:ns1":"http://impl.channel.adapter.ns.creditease.com/"})
        returnNode=self.__createElement('return', parentNode=response)
        
        amount=expectationDict.get('amount', requestDict.get('amount', '100.00'))
        bizId=expectationDict.get('bizId', requestDict.get('bizId', 'chu1311091522420070223'))
        failReason=expectationDict.get('failReason', '0')
        merchId=expectationDict.get('merchId', requestDict.get('merchId', '0000323'))
        respCode=expectationDict.get('respCode', '0000')
        respDescription=expectationDict.get('respDescription', 'success')
        state=expectationDict.get('state', '01')
        completeTime=expectationDict.get('completeTime', util.date2Str(format='%Y-%m-%d %H:%M:%S'))
        txId=expectationDict.get('txId', 'CEX150825104635190462133038')
        signInfo=expectationDict.get('signInfo', '166605404c302c36882a83dca4f2fd00')
        
        self.__createElement("amount", parentNode=returnNode, text=amount)
        self.__createElement("bizId", parentNode=returnNode, text=bizId)
        self.__createElement("failReason", parentNode=returnNode, text=failReason)
        self.__createElement("merchId", parentNode=returnNode, text=merchId)
        self.__createElement("respCode", parentNode=returnNode, text=respCode)
        self.__createElement("respDescription", parentNode=returnNode, text=respDescription)
        self.__createElement("state", parentNode=returnNode, text=state)
        self.__createElement("completeTime", parentNode=returnNode, text=completeTime)
        self.__createElement("txId", parentNode=returnNode, text=txId)
        self.__createElement("signInfo", parentNode=returnNode, text=signInfo)

        xmlContent=self.doc.toprettyxml(indent='    ')
        print xmlContent
        return xmlContent


    def __createElement(self, tag, parentNode=None, attrDict=None, text=None):
        element=self.doc.createElement(tag);
        if attrDict is not None:
            for key in attrDict:
                element.setAttribute(key, str(attrDict[key]))
        if text is not None:
            textNode=self.doc.createTextNode(str(text))
            element.appendChild(textNode)
        if parentNode is not None:
            parentNode.appendChild(element)
        return element
