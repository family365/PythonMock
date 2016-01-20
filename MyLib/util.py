# -*- coding: utf-8 -*-
import time
import datetime
import os
import subprocess
from fileWrapper import FileWrapper

def date2Str(date=datetime.datetime.now(), format='%Y%m%d%H%M%S%f'):
    '''
     %y 两位数的年份表示（00-99）
     %Y 四位数的年份表示（000-9999）
     %m 月份（01-12）
     %d 月内中的一天（0-31）
     %H 24小时制小时数（0-23）
     %I 12小时制小时数（01-12）
     %M 分钟数（00=59）
     %S 秒（00-59）
     %f 微妙（0,999999）
     datetime.datetime.strftime(dd, format)
     dd.strftime(format)
    '''
    return date.strftime(format)

def chdir(dest):
    os.chdir(dest)

def runCmd(command):
    '''
    import os
    os.popen("dir")

    import subprocess
    P=subprocess.Popen("dir", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    '''
    process=subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output=[]
    while True:
        line=process.stdout.readline()
        if line=='' or line is None:
            break
        output.append(line)
    allLines=''.join(output)
    print allLines
    return allLines


