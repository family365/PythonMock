import os
import json
from MyLib import util
from MyLib import BaseResponseProcessor
from MyLib import FileWrapper
from xml.dom.minidom import Document


class CeVerifyWS(BaseResponseProcessor):
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
        response=self.__createElement('ns1:singleCertAndAccountVerifyResponse', parentNode=body, attrDict={"xmlns:ns1":"http://impl.channel.adapter.ns.creditease.com/"})
        returnNode=self.__createElement('return', parentNode=response)
        
        merchId=expectationDict.get('merchId', requestDict.get('merchId', '0000323'))
        respCode=expectationDict.get('respCode', '0000')
        respDescription=expectationDict.get('respDescription', 'success')
        respId=expectationDict.get('respId', '1')
        state=expectationDict.get('state', '01')
        
        self.__createElement("merchId", parentNode=returnNode, text=merchId)
        self.__createElement("respCode", parentNode=returnNode, text=respCode)
        self.__createElement("respDescription", parentNode=returnNode, text=respDescription)
        self.__createElement("respId", parentNode=returnNode, text=respId)
        self.__createElement("state", parentNode=returnNode, text=state)

        xmlContent=self.doc.toprettyxml(indent='    ')
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
