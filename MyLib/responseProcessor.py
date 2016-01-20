import abc
import util
import os
from fileWrapper import FileWrapper
'''
For every response mocking, you need to be drived from this class
'''
class BaseResponseProcessor:
    def processRequest(self, request):
        '''
        sometimes you need to get involved the processing of the request parameter
        for example, when we get a xml formatted request, we need to extract the parameter from the xml,
        and put them into a dict object, in thi case, it require you re-implement this method in your own response processor.

        by default, this method will assume the request is a dict type of object, and no more action on it,
        so this method will do nothing, just get the request parameter return, 
        '''
        return request
    
    def getWorkingPath(self, group, APIShortName):
        workingPath='D:\\Project\\Python\\cache\\%s\\%s' % (group, APIShortName) 
        if not os.path.exists(workingPath):
            os.makedirs(workingPath)
        return workingPath

    def getExpectationPath(self, directory):
        return os.path.join(directory, 'expectation.txt')
    
    def saveExpectation(self, expectationDict, group, APIShortName):
        '''
        Currently, we save these expectation into file with json format. In the future, we will move them into Redis or memcache 
        '''
        workingPath=self.getWorkingPath(group, APIShortName)
        expectationFile=self.getExpectationPath(workingPath)
        fileHandler=FileWrapper(expectationFile)
        return fileHandler.saveDictAsJsonFile(expectationDict)

    def loadExpectation(self, requestDict, group, APIShortName):
        '''
        Currently, these expectation were save into file. In the future, we will move them into Redis or memcache 
        '''        
        workingPath=self.getWorkingPath(group, APIShortName)
        expectationFile=self.getExpectationPath(workingPath)
        fileHandler=FileWrapper(expectationFile)
        if not fileHandler.isExist() or fileHandler.expired(5000):
            print 'Expectation file is not found or have been expired'
            return {}

        print 'Expectation file is avaliable'
        return fileHandler.loadDictFromJsonFile()

    @abc.abstractmethod
    def getResponse(self, requestDict, expectationDict):
        '''
        You will handle the concrete the step about how to generate the response
        according to these two "requestDict" and "expectationDict" DICT object
        '''
        pass
