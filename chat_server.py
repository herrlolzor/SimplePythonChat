from socket import *      #import the socket library
from utils import *
from threading import Thread
import time
def wait(z):
	time.sleep(float(z))
class ioctrl():
	def __init__(self):
		self.outflag=0
		self.out=''
	def ioctrl(self):
		if self.outflag==1:
			print self.out
			self.out=''
			self.outflag=0
class SocketServerObject():
	def __init__(self):
		pass
	def serve(self):
		HOST = ''
		PORT = 29876
		ADDR = (HOST,PORT)
		BUFSIZE = 4096
		DATA=()
		serv = socket( AF_INET,SOCK_STREAM)
		log=''
		msglog=[[time.time(),'SERVER STARTED']]
		lastping={}
		usrlist=['admin']
		userpw={}
		userpw['admin']='7bba8ac2526a26c235dfb27518e8be8f'
		serv.bind((ADDR))
		serv.listen(10)
		IObus=ioctrl()
		end=0
		print 'SERVER ACTIVATED'
		try:
			while end==0:
				conn, addr=serv.accept()
				conn.send('LOGIN')
				DATA=conn.recv(BUFSIZE)
				#print DATA
				if DATA!=():
					
					if DATA.startswith('RETURNNEW'):
						user=DATA.split('$USR$')[1]
						sendback=[]
						for i in msglog:
							if i[0]>lastping[user]: sendback.append(i[1])
						sendbacktxt=''
						for i in sendback:
							sendbacktxt=sendbacktxt+i+'\n'
						conn.send('SENDBACK$'+sendbacktxt)
						conn.close()
						lastping[user]=time.time()
						
					elif DATA.find('$MSG$')> -1:
						log=log+str(time.time())+':'+str(DATA)+'\n'
						msgsplit=DATA.split('$MSG$')
						user=msgsplit[0]
						msg=msgsplit[1]
						print user,':',msg
						msglog.append([time.time(),user+": "+msg])
						conn.send('ACK')
						conn.close()
					
					elif DATA.startswith('CONNECTION'):
						log=log+str(time.time())+':'+str(DATA)+'\n'
						user=DATA.split(':')[1]
						pw=md5(DATA.split(':')[2])
						print 'CONNECTION: ',user
						lastping[user]=time.time()
						try:
							usrlist.index(user)
							if userpw[user]!=pw:
								conn.send('WRONG PASSWORD')
								conn.close()
							else:
								print user,'GOOD LOGIN'
								conn.send('ACCESS GRANTED')
								conn.close()
						except ValueError:
							usrlist.append(user)
							userpw[user]=md5(DATA.split(':')[2])
							conn.send('ACCESS GRANTED')
							conn.close()
							msglog.append([time.time(),'SERVER: '+user+' HAS CONNECTED'])
						
					elif DATA.startswith('LOGOUT'):
						dat=DATA.split(':')
						user=dat[1]
						pw=md5(dat[2])
						del dat
						if pw==userpw[user]:
							usrlist.remove(user)
							del userpw[user]
						conn.send('ACK')
						conn.close()
							
					else:
						conn.send('ACK')
						conn.close()
						
				while len(msglog)>100:
					msglog.remove(msglog[0])
		except KeyboardInterrupt:
			print 'SERVER CLOSED'
			serv.close()
			raw_input("ANY KEY TO EXIT")

SERVER=SocketServerObject()
SERVER.serve()
