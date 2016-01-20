# -*- coding: UTF-8 -*-
import sys
from xml.etree import ElementTree
from xml.dom.minidom import Document
from MyLib import FileWrapper
from MyLib import util
from MyLib import BaseResponseProcessor

import random
import os


'''
ElementTree support xpath, so use it to parse the xml file, and return a dict object to the caller 
Document不支持xpath查询, use it to write xml file
获取element的方法 http://blog.csdn.net/yueguanghaidao/article/details/7265246
a) 通过getiterator 获取子节点的迭代对象
b) 通过 getchildren 获取子节点列表
c) find方法 支持xpath查询，查询第一个匹配的节点
d) findall方法 支持xpath查询，查询所有匹配的节点
.//a 表示从当前节点依次便利所有子节点，查找所有的a节点
*/a   同上
'''
class CGBFundMessageProcessor(BaseResponseProcessor):
    def __init__(self):
        self.doc=Document()
        self.privatePath="D:\\shared\\CGB(CGBCC)\\CGB(CGBCC)\\publicAndPrivateForMerchant\955081150000001.pfx"
        self.privatePassword="123456"

    def processRequest(self, message):
        nodeValueMap={}
        doc=ElementTree.fromstring(message)
        messageElement=doc.find("Message");
        focusedNode=messageElement.getchildren()[0]
        command=focusedNode.tag
        nodeValueMap["command"]=command
        __parseNode(focusedNode,nodeValueMap)
        print nodeValueMap
        return nodeValueMap

    def getWorkingPath(self, group, APIShortName, command):
        pathTemp="D:\\Project\\Python\\cache\\{0}"
        workingPath=pathTemp.format(command)
        if not os.path.exists(workingPath):
            os.mkdir(workingPath)
        return workingPath

    def saveExpectation(self, expectationDict, group, APIShortName):
        requestCommand=expectationDict['command']
        if not self.__isSupportedCommand(requestCommand):
            raise Exception(requestCommand, " request does not support")
        
        workingPath=self.getWorkingPath(group, APIShortName, requestCommand)
        expectationFile=self.getExpectationPath(workingPath)
        fileHandler=FileWrapper(expectationFile)
        return fileHandler.saveDictAsJsonFile(expectationDict)

    def loadExpectation(self, requestDict, group, APIShortName):
        requestCommand=expectationDict['command']
        if not self.__isSupportedCommand(requestCommand):
            raise Exception(requestCommand, " request does not support")
        
        workingPath=self.getWorkingPath(group, APIShortName, requestCommand)
        expectationFile=self.getExpectationPath(workingPath)
        fileHandler=FileWrapper(expectationFile)
        if not fileHandler.isExist() or fileHandler.expired():
            return {}

        return fileHandler.loadDictFromJsonFile()

    def getResponse(self, requestDict, expectationDict):
        if expectationDict is None:
            expectationDict={}
            
        if expectationDict.get('errorDetail') is not None:
            return self._createErroResponse(requestDict, expectationDict)
        
        srcCmd=requestDict['command']
        command=srcCmd.lower()
        print 'Current command: ', command
        if command=="fiqreq":
            return self._createFundInfoQueryResponse(requestDict, expectationDict)
        elif command=="arreq":
            return self._createAccountRegistResponse(requestDict, expectationDict)
        elif command=="arqreq":
            return self._createQueryAccountRegistResultResponse(requestDict, expectationDict)
        elif command=="fareq":
            return self._createFundApplyResponse(requestDict, expectationDict)
        elif command=="frreq":
            return self._createFundRedeemResponse(requestDict, expectationDict)        
        elif command=="fidqreq":
            pass
        elif command=="fuqreq":
            pass
        elif command=="trqreq":
            return self._createQueryTradeResultResponse(requestDict, expectationDict)
        else:
            return '{"errorMessage":"request not surport by mock platform"}'

    def __isSupportedCommand(self, command):
        command=command.lower()
        supportedCommands=('fiqreq','arreq','arqreq','fareq','frreq','trqreq','','','','','','')
        print 'Current command: ', command
        return command  in supportedCommands
    
    def _createFundInfoQueryResponse(self, requestDict, expectationDict):
        totalNum=expectationDict.get("totalNum", 19)
        beginPos=requestDict["beginPos"]
        pageNum=requestDict["pageNum"]

        print "Input param: ", str(requestDict)
        if beginPos >= totalNum:
            endPos=beginPos
            itemCount=0
            currentPageIndex=0
            print "beginPos is out of total number, return null item"
        else:
            endPos=beginPos + pageNum
            if endPos > (totalNum - 1):
                endPos = totalNum
            itemCount=endPos - beginPos
            print "beginPos=", str(beginPos), ", endPos=", endPos, ", itemCount=", itemCount

        instId=requestDict.get('instId', 'CGB(CGBCC)')
        certId=requestDict.get('certId', '0001')
        errorCode=expectationDict.get('errorCode', '0000')
        errorMessage=expectationDict.get('errorMessage', '查询成功')
        
        root=self.__createElement('SoEv', parentNode=self.doc)
        message=self.__createElement("Message", parentNode=root, attrDict={"id":util.date2Str()})
        responseBody=self.__createElement("FIQRes", parentNode=message,attrDict={"id":"FIQRes"})
        version=self.__createElement("version", parentNode=responseBody, text="1.0.1")
        instId=self.__createElement("instId", parentNode=responseBody, text=instId)
        certId=self.__createElement("certId", parentNode=responseBody, text=certId)
        errorCode=self.__createElement("errorCode", parentNode=responseBody, text=errorCode)
        errorMessage=self.__createElement("errorMessage", parentNode=responseBody, text=errorMessage)
        totalNum=self.__createElement("totalNum", parentNode=responseBody, text=str(totalNum))
        curPageNum=self.__createElement("curPageNum", parentNode=responseBody, text=str(itemCount))
        iFundDetailList=self.__createElement("iFundDetailList", parentNode=responseBody)

        for index in range(beginPos, endPos):
            item=self.__createElement("item", parentNode=iFundDetailList)
            self.__createElement("fundComNo", parentNode=item, text=index + 1)
            self.__createElement("productNo", parentNode=item, text=str(100000+index + 1))
            self.__createElement("fundCode", parentNode=item, text='%06d' % (300+index + 1))
            self.__createElement("fundName", parentNode=item, text="广发天天红货币"+str(index + 1))
            self.__createElement("fundType", parentNode=item, text='%03d' % (random.randint(1,9)))
            self.__createElement("feesType", parentNode=item, text="0")
            self.__createElement("shareType", parentNode=item, text="0")
            self.__createElement("state", parentNode=item, text=str(random.randint(1,9)))
            self.__createElement("millionOfIncome", parentNode=item, text='{0:.4f}'.format(1 + random.random()))
            self.__createElement("sevenIncome", parentNode=item, text='{0:.4f}'.format(3 + random.random()))
            self.__createElement("fundsMon", parentNode=item, text='{0:.4f}'.format(random.random()))
            self.__createElement("fundDate", parentNode=item, text=util.date2Str(format="%Y-%m-%d"))

        signedMessage=self.__saveAndSign("FIQRes")
        return signedMessage

    def _createAccountRegistResponse(self, requestDict, expectationDict):
        root=self.__createElement('SoEv', parentNode=self.doc)
        message=self.__createElement('Message', parentNode=root, attrDict={"id":util.date2Str()})
        responseBody=self.__createElement('ARQRes', parentNode=message, attrDict={"id":util.date2Str()})

        instId=requestDict.get('instId', 'CGB(CGBCC)')
        certId=requestDict.get('certId', '0001')
        channelSeq=requestDict.get('channelSeq', '12345678909999999')
        errorCode=expectationDict.get('errorCode', '0000')
        errorMessage=expectationDict.get('errorMessage', '开户结果查询成功')
        dealRes=expectationDict.get('dealRes', '0')
        accountNo=expectationDict.get('accountNo', None)
        certNo=requestDict.get('certNo', None)
        cusName=requestDict.get('cusName', None)
        phoneNo=requestDict.get('phoneNo', None)
        cardNo=requestDict.get('cardNo', None)

        self.__createElement("version", parentNode=responseBody, text="1.0.1")
        self.__createElement("instId", parentNode=responseBody, text=instId)
        self.__createElement("certId", parentNode=responseBody, text=certId)
        self.__createElement("channelSeq", parentNode=responseBody, text=channelSeq)
        self.__createElement("errorCode", parentNode=responseBody, text=errorCode)
        self.__createElement("errorMessage", parentNode=responseBody, text=errorMessage)
        self.__createElement("DealRes", parentNode=responseBody, text=dealRes)
        self.__createElement("accountNo", parentNode=responseBody, text=accountNo)
        self.__createElement("certNo", parentNode=responseBody, text=certNo)
        self.__createElement("cusName", parentNode=responseBody, text=cusName)
        self.__createElement("phoneNo", parentNode=responseBody, text=phoneNo)
        self.__createElement("cardNo", parentNode=responseBody, text=cardNo)

        signedMessage=self.__saveAndSign("ARQRes")
        return signedMessage     
        

    def _createQueryAccountRegistResultResponse(self, requestDict, expectationDict):
        root=self.__createElement('SoEv', parentNode=self.doc)
        message=self.__createElement('Message', parentNode=root, attrDict={"id":util.date2Str()})
        responseBody=self.__createElement('ARQRes', parentNode=message, attrDict={"id":util.date2Str()})

        instId=requestDict.get('instId', 'CGB(CGBCC)')
        certId=requestDict.get('certId', '0001')
        channelSeq=requestDict.get('channelSeq', '123456789009877782')
        errorCode=expectationDict.get('errorCode', '0000')
        errorMessage=expectationDict.get('errorMessage', '开户结果查询成功')
        dealRes=expectationDict.get('dealRes', '0')
        accountNo=expectationDict.get('accountNo', None)
        certNo=expectationDict.get('certNo', None)
        cusName=expectationDict.get('cusName', None)
        phoneNo=expectationDict.get('phoneNo', None)
        cardNo=expectationDict.get('cardNo', None)

        self.__createElement("version", parentNode=responseBody, text="1.0.1")
        self.__createElement("instId", parentNode=responseBody, text=instId)
        self.__createElement("certId", parentNode=responseBody, text=certId)
        self.__createElement("channelSeq", parentNode=responseBody, text=channelSeq)
        self.__createElement("errorCode", parentNode=responseBody, text=errorCode)
        self.__createElement("errorMessage", parentNode=responseBody, text=errorMessage)
        self.__createElement("DealRes", parentNode=responseBody, text=dealRes)
        self.__createElement("accountNo", parentNode=responseBody, text=accountNo)
        self.__createElement("certNo", parentNode=responseBody, text=certNo)
        self.__createElement("cusName", parentNode=responseBody, text=cusName)
        self.__createElement("phoneNo", parentNode=responseBody, text=phoneNo)
        self.__createElement("cardNo", parentNode=responseBody, text=cardNo)

        signedMessage=self.__saveAndSign("ARQRes")
        return signedMessage

    def _createFundApplyResponse(self, requestDict, expectationDict):
        root=self.__createElement('SoEv', parentNode=self.doc)
        message=self.__createElement('Message', parentNode=root, attrDict={"id":util.date2Str()})
        responseBody=self.__createElement('FAReq', parentNode=message, attrDict={"id":util.date2Str()})

        instId=requestDict.get('instId', 'CGB(CGBCC)')
        certId=requestDict.get('certId', '0001')
        channelSeq=requestDict.get('channelSeq', '123456789009877782')
        errorCode=expectationDict.get('errorCode', '0000')
        errorMessage=expectationDict.get('errorMessage', '申购成功')
        dealRes=expectationDict.get('dealRes', '0')

        self.__createElement("version", parentNode=responseBody, text="1.0.1")
        self.__createElement("instId", parentNode=responseBody, text=instId)
        self.__createElement("certId", parentNode=responseBody, text=certId)
        self.__createElement("channelSeq", parentNode=responseBody, text=channelSeq)
        self.__createElement("errorCode", parentNode=responseBody, text=errorCode)
        self.__createElement("errorMessage", parentNode=responseBody, text=errorMessage)
        self.__createElement("dealRes", parentNode=responseBody, text=dealRes)
        self.__createElement("bussDate", parentNode=responseBody, text=util.date2Str(format='%Y%m%d'))

        signedMessage=self.__saveAndSign("FAReq")
        return signedMessage

        
    def _createFundRedeemResponse(self, requestDict, expectationDict):
        root=self.__createElement('SoEv', parentNode=self.doc)
        message=self.__createElement('Message', parentNode=root, attrDict={"id":util.date2Str()})
        responseBody=self.__createElement('FRRes', parentNode=message, attrDict={"id":util.date2Str()})

        instId=requestDict.get('instId', 'CGB(CGBCC)')
        certId=requestDict.get('certId', '0001')
        channelSeq=requestDict.get('channelSeq', '123456789009877782')
        errorCode=expectationDict.get('errorCode', '0000')
        errorMessage=expectationDict.get('errorMessage', '基金赎回成功')
        dealRes=expectationDict.get('dealRes', '0')
        
        self.__createElement("version", parentNode=responseBody, text="1.0.1")
        self.__createElement("instId", parentNode=responseBody, text=instId)
        self.__createElement("certId", parentNode=responseBody, text=certId)
        self.__createElement("channelSeq", parentNode=responseBody, text=channelSeq)
        self.__createElement("errorCode", parentNode=responseBody, text=errorCode)
        self.__createElement("errorMessage", parentNode=responseBody, text=errorMessage)
        self.__createElement("dealRes", parentNode=responseBody, text=dealRes)
        self.__createElement("bussDate", parentNode=responseBody, text=util.date2Str(format='%Y%m%d'))

        signedMessage=self.__saveAndSign("FRRes")
        return signedMessage

    def _createQueryFundProfitResponse(self, requestDict, expectationDict):
        root=self.__createElement('SoEv', parentNode=self.doc)


    def _createQueryFundUnitResponse(self, requestDict, expectationDict):
        root=self.__createElement('SoEv', parentNode=self.doc)

    def _createQueryTradeResultResponse(self, requestDict, expectationDict):
        root=self.__createElement('SoEv', parentNode=self.doc)
        message=self.__createElement('Message', parentNode=root, attrDict={"id":util.date2Str()})
        responseBody=self.__createElement('FRRes', parentNode=message, attrDict={"id":util.date2Str()})

        instId=requestDict.get('instId', 'CGB(CGBCC)')
        certId=requestDict.get('certId', '0001')
        channelSeq=requestDict.get('channelSeq', '123456789009877782')
        errorCode=expectationDict.get('errorCode', '0000')
        errorMessage=expectationDict.get('errorMessage', '交易查询成功')
        dealRes=expectationDict.get('dealRes', '0')
        
        self.__createElement("version", parentNode=responseBody, text="1.0.1")
        self.__createElement("instId", parentNode=responseBody, text=instId)
        self.__createElement("certId", parentNode=responseBody, text=certId)
        self.__createElement("channelSeq", parentNode=responseBody, text=channelSeq)
        self.__createElement("errorCode", parentNode=responseBody, text=errorCode)
        self.__createElement("errorMessage", parentNode=responseBody, text=errorMessage)
        self.__createElement("dealRes", parentNode=responseBody, text=dealRes)
        self.__createElement("bussDate", parentNode=responseBody, text=util.date2Str(format='%Y%m%d'))
        self.__createElement("dealRes", parentNode=responseBody, text=util.date2Str(format='%Y%m%d%H%M%S'))

        signedMessage=self.__saveAndSign("FRRes")
        return signedMessage

    def _createErroResponse(self, requestDict, expectationDict):
        root=self.__createElement('SoEv', parentNode=self.doc)
        message=self.__createElement('Message', parentNode=root, attrDict={"id":util.date2Str()})
        errorBody=self.__createElement('Error', parentNode=message)
        
        instId=requestDict.get('instId', 'CGB(CGBCC)')
        certId=requestDict.get('certId', '0001')
        errorCode=expectationDict.get('errorCode', '1000')
        errorMessage=expectationDict.get('errorMessage', '操作失败')
        dealRes=expectationDict.get('errorDetail', 'error detail')
        dealRes=expectationDict.get('vendorCode', '6789')
        
        self.__createElement("version", parentNode=responseBody, text="1.0.1")
        self.__createElement("instId", parentNode=responseBody, text=instId)
        self.__createElement("certId", parentNode=responseBody, text=certId)
        self.__createElement("errorCode", parentNode=responseBody, text=errorCode)
        self.__createElement("errorMessage", parentNode=responseBody, text=errorMessage)
        self.__createElement("errorDetail", parentNode=responseBody, text=dealRes)
        self.__createElement("vendorCode", parentNode=responseBody, text=dealRes)

        signedMessage=self.__saveAndSign("FRRes")
        return signedMessage

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

    def __saveAndSign(self, signNode, parentNode="Message"):
        workingPath=self.getWorkingPath(signNode)
        targetFile=os.path.join(workingPath, "message.txt")
        print targetFile
        file=FileWrapper(targetFile)
        xmlContent=self.doc.toprettyxml(indent='    ')
        file.write(xmlContent) 
        file_name = os.path.dirname(__file__)
        projectPath = os.path.abspath(file_name)
        signerPath=os.path.join(projectPath, 'MessageSigner.jar')
        command='java -jar %s -f %s -m "XML(RSA_SHA1)" -n %s -pn %s -p %s -pp %s' % (signerPath, targetFile, signNode, parentNode, self.privatePath, self.privatePassword)
        signedMessage=util.runCmd(command) 
        #print signedMessage
        return signedMessage

    def __parseNode(node,nodeValueMap):
        if node is None:
            return nodeValueMap
        
        for node in node.getchildren():
            key=node.tag
            value=node.text
            nodeValueMap[key]=value


if __name__=='__main__':
    processor=CGBFundMessageProcessor()
    requestDict=None
    #requestDict['command']='fiqreq'
    #requestDict["totalNum"]=19
    #requestDict["beginPos"]=15
    #requestDict["pageNum"]=6
    #requestDict["instId"]="955081150000001" 
    #requestDict["certId"]="00011"
    print processor.getResponse(requestDict, None)


    message='''<?xml version="1.0" encoding="UTF-8"?>
                <SoEv>
                <Message id="955081150000001">
                <FIQReq id="FIQReq">
                        <version>1.0.1</version>
                        <instId>955081150000001</instId>
                        <certId>0001</certId>
                        <channelDate/>
                        <productNo/>
                        <beginPos>0</beginPos>
                        <pageNum>10</pageNum>
                        <extension>测试中文数据是否乱码</extension>
                </FIQReq>
                <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                <ds:SignedInfo>
                <ds:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
                <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
                <ds:Reference URI="#FIQReq">
                <ds:Transforms>
                <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
                </ds:Transforms>
                <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
                <ds:DigestValue>yizm56maZILE0D3PSXUh1RrZzv4=</ds:DigestValue>
                </ds:Reference>
                </ds:SignedInfo>
                <ds:SignatureValue>QqXSs+L6PN737DcS6rnSlz+0VWv1Ar+EigSBdGQRst0VASM0802FdDNOBDz6warDJIpn0g7RWQAd
                71aaR6lU4lUxngoiL+epYXmN5QrbUvAEH47b6kopzQeKb6G1xtFOqbAlh/JGcMk5ukEVcVlsthVq
                1Y/JRQjHTZC1Ys+Ac1Y=
                </ds:SignatureValue>
                </ds:Signature>
                </Message>
                </SoEv>
                '''
    #parseMessage(message)
