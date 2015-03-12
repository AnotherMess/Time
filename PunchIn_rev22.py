#-------------------------------------------------------------------------------
# Name:        PunchIn.py
# Purpose:
# Author:      oconnellb
#
# rev 2.2      05Feb2015
#-------------------------------------------------------------------------------

import os, datetime, fnmatch, time, sys, ntplib
from time import gmtime, strftime
from EasyGui import enterbox, codebox, msgbox
import shutil as sh

TimeLog_path = r'C:\Users\oconnellb\My Documents\Time'
TimeFile = os.path.join(TimeLog_path,r'Time.log')
BackUpPath = r"\\Dbs5\Engineering\Personal\Brian O'Connell\logs"

#TimeLog_path = r'/home/brian/Desktop/time'
#TimeFile = os.path.join(TimeLog_path,r'Time.log')
#BackUpPath = r'/home/brian/Desktop/time/bu'

TEST = True

#if first entry for day and >2500 lines then archive
#save copy of current log, then rename and move to archive path
def DoBackUp():
    with open(TimeFile,'r') as log:
        data=log.readlines()
    #log.close()
    today = strftime("%d %b")
    if len(data)>2500 and today not in data:
        if TEST: print 'doing time log bu'
        BackUpFname = r'TimeLog'+strftime("%d %b %y")+r'.log'
        sh.copy(TimeFile,os.path.join(BackUpPath,r'Time.log'))
        sh.move(TimeFile, BackUpFname)

def ProjectIsOpen(num):
    startcount = stopcount = 0
    if not os.path.isfile(TimeFile): return False
    startstr = str(num)+r' START '+strftime("%d %b")
    stopstr = str(num)+r' STOP '+strftime("%d %b")
    with open(TimeFile,'r') as log:
        s=log.read().replace('\n', ' ')
    startcount=s.count(startstr)
    stopcount=s.count(stopstr)
    if TEST:
        print 'start '+str(startcount)
        print 'stop '+str(stopcount)
    return ((startcount>stopcount) and (startcount>0))

def StartProject(num):
    with open(TimeFile,'a') as log:
        log.write('\n'+str(num)+r' START '+strftime("%d %b %Y %X"))
    return True

def punchin(projectnum):
    if ProjectIsOpen(projectnum):
        s=str(projectnum)+' is already open'
        if TEST: print s
        msgbox(s)
    else:
        if StartProject(projectnum):
            s=str(projectnum)+' time start'
            msgbox(s)
        else:
            s=str(projectnum)+' not able to start'
            msgbox(s)

def main():
    DoBackUp()
    if len(sys.argv) == 1:
        s=enterbox('Enter Project Number: ')
        if s:
            punchin(s)

if __name__ == '__main__':
    main()
