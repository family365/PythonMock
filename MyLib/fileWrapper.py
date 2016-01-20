import os
from json import *
import datetime

class FileWrapper:
    def __init__(self, filePath):
        self.filePath=filePath

    def readAllLinesToString(self):
        if self.isExist() and self.isFile():
            fileHandler=open(self.filePath, mode='r')
            lines=fileHandler.readlines()
            strLine="".join(lines)
            return strLine
        else:
            raise Exception("File not found: %s", self.filePath)

    def readAllLines(self):
        if self.isExist() and self.isFile():
            fileHandler=open(self.filePath, mode='r')
            lines=fileHandler.readlines()
            fileHandler.close()
            return lines
        else:
            raise Exception("File not found: %s", self.filePath)

    def write(self, content, append=False):
        try:
            if append:
                fileHandler=open(self.filePath,mode='a')
            else:
                fileHandler=open(self.filePath,mode='w')
            fileHandler.writelines(content)
        finally:
                fileHandler.close()

    def isExist(self):
        return os.path.exists(self.filePath)

    def isFile(self):
        return os.path.isfile(self.filePath)

    def isDirectory(self):
        return os.path.isdir(self.filePath)

    def expired(self, timeslot=5*60):
        '''
        timedelta only support days, seconds, microseconds,
        in other words, if you want to use other unit for timeslot you need do some convert
        By default, the file will be expired in 5min when you complete the modification
        '''
        timestamp=os.path.getmtime(self.filePath)
        modifyTime=datetime.datetime.fromtimestamp(timestamp)
        expiredTime=modifyTime + datetime.timedelta(seconds=timeslot)
        if expiredTime < datetime.datetime.now():
            return True
        else:
            return False
        
    def getFileNameWithouExt(self):
        if self.isExist(self.filePath):
            return os.path.basename(filePath)
        else:
            raise Exception("file not found")

    def getFileName(self):
        if self.isExist(self.filePath):
            pathPlusFileName=os.path.split(self.filePath)
            return pathPlusFileName[1]
        else:
            raise Exception("file not found")

    def saveDictAsJsonFile(self, dictMap):
        jsonStr=JSONEncoder().encode(dictMap)
        self.write(jsonStr)
        return jsonStr

    def loadDictFromJsonFile(self):
        file=FileWrapper(self.filePath)
        if not self.isExist():
            raise Exception("File not found")
        lines=[]
        for line in self.readAllLines():
            if line.strip()=="":
                continue
            lines.append(line.strip())
        jsonStr=" ".join(lines)
        dictMap=JSONDecoder().decode(jsonStr)
        return dictMap
