from json import *
from fileWrapper import *
import urllib
import urllib2

class HttpClient(object):
    def __init__(self,filePath,tempPath=""):
        self.filePath=filePath
        self.tempFile=tempPath
        
    def doSaveAsJson(self,request):
        dictMap=self.__loadDictFromFile(self.tempFile)
        for key in request.args:
            if key not in dictMap:
                print "Warning: the key [%s] not represent in temp, skip it" % key
                continue
            print "change property to: %s=%s" % (key, request.args[key])
            dictMap[key]=request.args[key]
        self.__saveDict(self.filePath, dictMap)
        return dictMap

    def doLoadJson(self):
        jsonStr=self.__readAllLinesToString(self.filePath)
        return jsonStr

    def doOverrideSoapMessage(self, request,defaultParam):
        soapFmt=self.__readAllLinesToString(self.tempFile)
        for key in request.args:
            if key not in defaultParam:
                print "Warning: the key [%s] not represent in temp, skip it" % key
                continue
            print "change property to: %s=%s" % (key, request.args[key])
            defaultParam[key]=request.args[key]
        soap=soapFmt % defaultParam
        fileMsg=FileWrapper(self.filePath)
        fileMsg.write(soap)
        return soap
        
    def doLoadSoap(self):
        soap=self.__readAllLinesToString(self.filePath)
        return soap

    def doGet(self, url, param):
        queryStr=urllib.urlencode(param)
        fullURLPath=url + '?' + queryStr
        resData=urllib2.urlopen(fullURLPath) # file handler returned
        response=resData.readlines()
        return response
    
    def doPost(self, url, param):
        requestParam=urllib.urlencode(param)
        resData=urllib2.urlopen(url,requestParam) # file handler returned
        response=resData.readlines()
        return response
    
    def __saveDict(self,filePath, dictMap):
        file=FileWrapper(filePath)
        jsonStr=JSONEncoder().encode(dictMap)
        file.write(jsonStr)
        
    def __loadDictFromFile(self,filePath):
        file=FileWrapper(filePath)
        if not file.isExist():
            raise Exception("File not found: %s" % filePath)
        lines=[]
        for line in file.readAllLines():
            if line.strip()=="":
                continue
            lines.append(line.strip())
        jsonStr=" ".join(lines)
        dictMap=JSONDecoder().decode(jsonStr)
        return dictMap
        
    def __readAllLinesToString(self, filePath):
        file=FileWrapper(filePath)
        return file.readAllLinesToString()

    
            
