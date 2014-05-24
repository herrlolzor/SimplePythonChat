from socket import *
from threading import Thread
import time
def wait(z):
    time.sleep(float(z))
class ClientObject():
    def __init__(self,HOST,PORT,BUFFERSIZE):
        self.HOST=HOST
        self.PORT=PORT
        self.ADDR=(HOST,PORT)
        self.BUFSIZE=BUFFERSIZE
        self.login=''
        self.data=''
    def comm(self,msg):
        cli = socket( AF_INET,SOCK_STREAM)
        cli.connect((self.ADDR))
        self.login = cli.recv(self.BUFSIZE)
        cli.send(msg)
        self.data = cli.recv(self.BUFSIZE)
        cli.close()
        return self.data
Host='localhost'
Port=29876
Buffersize=4096
client=ClientObject(Host,Port,Buffersize)

chatlog=''
username=raw_input("ENTER USERNAME: ")
client.comm('CONNECTION:'+username)
try:
	while 1:
		print chatlog
		msg=raw_input(">")
		client.comm(username+"$MSG$"+msg)
		newtext=client.comm('RETURNNEW$USR$'+username)
		if newtext.startswith('SENDBACK'):
			newtext=newtext.split('$')[1]
			chatlog=chatlog+newtext
except KeyboardInterrupt:
	pass
