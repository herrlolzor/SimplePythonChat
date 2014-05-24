#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64,hashlib,binascii,random,subprocess,time,os

def Exec(cmde):
    if cmde:
        execproc = subprocess.Popen(cmde, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        cmdoutput = execproc.stdout.read() + execproc.stderr.read()
        return cmdoutput
    else:
        return "Enter a command.\n"       
def md5(*strings):
    key=hashlib.md5()
    for i in strings:
            key.update(i)
    this=key.hexdigest()
    del key
    return this
def sha512(*strings):
    key=hashlib.sha512()
    for i in strings:
            key.update(i)
    this=key.hexdigest()
    del key
    return this
def write_file(DATA,FILE):
    A=open(FILE,'w')
    A.write(DATA)
    A.close()
def read_file(FILE):
    A=open(FILE,'r')
    B=A.read()
    A.close()
    return B
def readbin(FILE):
    A=open(FILE,'rb')
    B=A.read()
    A.close()
    return B
def writebin(DATA,FILE):
    A=open(FILE,'wb')
    A.write(DATA)
    A.close()
def randstr(n):
    abc='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTSTUVWXYZ'
    H=''.join(random.choice(abc) for x in range(n))
    return H
def wait(T):
    time.sleep(float(T))
def replace(Str,left,right,inject,Buffer):
	rk0=Str.find(left)
	rk1=Str.find(right)
	RK0=Str[:rk0+len(left)]
	RK1=Str[rk1:]
	nstr=RK0+Buffer+str(inject)+Buffer+RK1
	return nstr
def fetchSTR(Str,left,right):
	rk0=Str.find(left)
	nstr=Str[rk0+len(left):]
	rk1=nstr.find(right)
	nstr=nstr[:rk1]
	return nstr
def OSslash():
	if os.name=='nt':
		return '\\'
	elif os.name=='posix':
		return '//'
def find_loc(STR):
	S=STR.split('.')
	return S
