#-------------------------------------------------------------------------------
# Name:        PunchOut
# Purpose:
# Author:      oconnellb
#
# rev 2.2      05Feb2015
#-------------------------------------------------------------------------------

import os, datetime, fnmatch, time, sys, ntplib
from time import gmtime, strftime
from EasyGui import enterbox, codebox, msgbox

TimeLog_path = r'C:\Users\oconnellb\My Documents\Time'
TimeFile = os.path.join(TimeLog_path,r'Time.log')
BackUpPath = r"\\Dbs5\Engineering\Personal\Brian O'Connell\logs"

#TimeLog_path = r'/home/brian/Desktop/time'
#TimeFile = os.path.join(TimeLog_path,r'Time.log')
#BackUpPath = r'/home/brian/Desktop/time/bu'

TEST = True

def TimeInterval(start,stop):
    from datetime import datetime
    FMT = '%H:%M:%S'
    return datetime.strptime(stop, FMT) - datetime.strptime(start, FMT)

def DailyTotal():
    f=os.path.join(TimeLog_path,TimeFile)
    todayentry = strftime("%d %b")
    data=[]
    Sums=[]
    with open(f,'r') as log:
        for line in log:
            s=line.strip('\n')
            if todayentry in s:
                data.append(s)
    if TEST: print data
    count=len(data)
    for x in range(count):
        print 'outer loop '+str(x)
        if 'START' in data[x]:
            s=data[x]
            starttime=s[-8:]
            projnum=s[:4]
            stopstr = str(projnum)+r' STOP '+strftime("%d %b")
            for n in range(count-x):
                print 'inner loop '+str(n)
                if stopstr in data[n]:
                    stoptime=data[n][-8:]
                    if TEST: print 'stoptime '+str(stoptime)
                    FoundStop=True
                    Sums.append(str(projnum)+' '+str(TimeInterval(starttime,stoptime))+' '+todayentry)
                    break
                if n>count:
                    stoptime=strftime("%d %b")
                    Sums.append(str(projnum)+' '+str(TimeInterval(starttime,stoptime))+' '+todayentry)
    return Sums

def ProjectIsOpen(num):
    # match number of starts w/number of stops
    IsOpen=False
    starttime=stoptime='0:0:0'
    startcount = stopcount = 0
    if not os.path.isfile(TimeFile): return IsOpen
    startstr = str(num)+r' START '+strftime("%d %b")
    stopstr = str(num)+r' STOP '+strftime("%d %b")
    with open(TimeFile,'r') as log:
        s=log.read().replace('\n', ' ')
    startcount=s.count(startstr)
    stopcount=s.count(stopstr)
    IsOpen=startcount>stopcount and startcount>0
    if not IsOpen:
        s=[]
        x=0
        with open(TimeFile,'r') as log:
            s=log.readlines()
        while True:
            if startstr in s[x]:
                if x==startcount:
                    starttime=s[-8:]
                    x+=1
                    while True:
                        if stopstr in s[x]:
                            stoptime=s[-8:]
                            break
                        else: continue
    return IsOpen, TimeInterval(starttime,stoptime)

def CloseAll():
    f=os.path.join(TimeLog_path,TimeFile)
    with open(f,'a') as log:
        log.write('\n'+'=======Daily Totals=======')
        sigmas=DailyTotal()
        for proj in sigmas:
            log.write('\n'+proj)
        log.write('\n'+str(0)+' STOP '+strftime("%d %b %Y %X"))
        log.write('\n'+'==========================')


def CloseProject(num):
    f=os.path.join(TimeLog_path,TimeFile)
    with open(f,'a') as log:
        log.write('\n'+str(num)+' STOP '+strftime("%d %b %Y %X"))
    return True

def punchout(projectnum):
    if str(projectnum)=='0':
        CloseAll()
        s=str('all projects closed for the day - do NOT reopen for this date')
        msgbox(s)
        return
    IsOpen,Interval=ProjectIsOpen(projectnum)
    if IsOpen:
        if CloseProject(projectnum):
            s=str(projectnum)+' stopped at '+str(Interval)
            msgbox(s)
        else:
            s=str(projectnum)+' not able to stop'
            msgbox(s)
    else:
        s=str(projectnum)+' was not open - no data entry to time log'
        msgbox(s)

def main():
    if len(sys.argv) == 1:
        s = enterbox('Enter project number to stop: ')
        if s:
            punchout(s)

if __name__ == '__main__':
    main()
