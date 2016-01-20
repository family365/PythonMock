from xml.etree import ElementTree
from MyLib import SingletonBase


class ConfigLoader(SingletonBase):
    URIPath='uriPath'
    Module='module'
    ClassName='className'
    Group='group'
    APIShortName='APIShortName'
    SubPath='subPath'
    
    def __init__(self, configFile):
        self.configPath=configFile
        self._projectInfo=None
            
    def getConfig(self):
        if self._projectInfo is None:
            print 'projectInfo is None'
            self._projectInfo=self.loadConfig()

        print 'return projectInfo'
        return self._projectInfo
            
    def loadConfig(self):
        projectInfo={}
        tree=ElementTree.parse(self.configPath)
        root=tree.getroot()
        projects=root.findall('projects/project')
        for proj in projects:
            configItems={}
            urlPath=proj.find(ConfigLoader.URIPath).text
            module=proj.find(ConfigLoader.Module).text
            className=proj.find(ConfigLoader.ClassName).text
            group=proj.find(ConfigLoader.Group).text
            apiShortName=proj.find(ConfigLoader.APIShortName).text
            subpath=proj.find(ConfigLoader.SubPath).text
            
            configItems[ConfigLoader.URIPath]=urlPath
            configItems[ConfigLoader.Module]=module
            configItems[ConfigLoader.ClassName]=className
            configItems[ConfigLoader.Group]=group
            configItems[ConfigLoader.APIShortName]=apiShortName
            configItems[ConfigLoader.SubPath]=subpath
            
            projectInfo[urlPath]=configItems
        return projectInfo
