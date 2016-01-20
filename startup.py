from flask import Flask,request,jsonify, abort, render_template
from json import *
from MyLib import HttpClient
from MyLib import util
from configLoader import ConfigLoader

app=Flask(__name__)


projectConfig='Project.Config'
configLoader=ConfigLoader(projectConfig)

@app.route('/sms/services/MessageService3.0/sms/send', methods=['POST','GET'])
def smsSend():
    return '{"code":"00000","desc":""}'

@app.route('/<pth1>', methods=['POST','GET'])
@app.route('/<pth1>/<pth2>', methods=['POST','GET'])
@app.route('/<pth1>/<pth2>/<pth3>', methods=['GET','POST'])
@app.route('/<pth1>/<pth2>/<pth3>', methods=['GET','POST'])
def urlMap(pth1,pth2=None,pth3=None,pth4=None):
    currentUrl='/' + pth1
    if pth2 is not None:
        currentUrl += '/' + pth2
    if pth3 is not None:
        currentUrl += '/' + pth3
    if pth4 is not None:
        currentUrl += '/' + pth4
    response=__getResponse(currentUrl, request)
    return response

@app.errorhandler(404) 
def page_not_found(error): 
    return render_template('404.html'),404

def __getResponse(currentUrl, request):
    print '*'*8, currentUrl, '*'*8
    projectInfo=configLoader.getConfig()
    configItems=projectInfo.get(currentUrl)
    if configItems is None:
        print "%s path not found" % currentUrl
        abort(404)
    moduleName=configItems[ConfigLoader.Module]
    className=configItems[ConfigLoader.ClassName]
    group=configItems[ConfigLoader.Group]
    APIShortName=configItems[ConfigLoader.APIShortName]
    print 'URI:', currentUrl, ' will from module:', moduleName, ' import class:', className
    
    module=__import__(moduleName)
    classObj=getattr(module, className)
    processorInstance=classObj()
    
    print request
    srcRequestDict={}
    if request.method=="GET":
        for key in request.args:
            srcRequestDict[key]=request.args[key]
    else: 
        for key in request.form:
            srcRequestDict[key]=request.form[key]
 
    if "target" in srcRequestDict and srcRequestDict['target'] == u'mock':
        del srcRequestDict["target"]
        print 'Save expecatation'
        return processorInstance.saveExpectation(srcRequestDict, group, APIShortName);
    else:
        requestDict=processorInstance.processRequest(srcRequestDict)
        expectationDict=processorInstance.loadExpectation(requestDict, group, APIShortName)
        return processorInstance.getResponse(requestDict, expectationDict)



if __name__ == '__main__':
    Host='0.0.0.0'
    app.run(host=Host,debug=True)

