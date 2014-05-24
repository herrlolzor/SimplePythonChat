from Tkinter import *
from socket import *
from threading import Thread
import time
from easygui import enterbox
from easygui import msgbox
from easygui import passwordbox
from utils import *

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

def updatetext():
	global client
	global scrollbar
	global chatlog
	global usrname
	newtext=client.comm('RETURNNEW$USR$'+usrname)
	if newtext.startswith('SENDBACK'):
		newtext=newtext.split('$')[1]
		chatlog=chatlog+newtext
	
	pos = scrollbar.get()
	text.delete(1.0,END)
	text.insert(INSERT, chatlog)
	
	if pos[1]==1.0:
		text.see(END)
	else:
		pass
	#scrollbar.set(pos[0],pos[1])
	text.after(500,updatetext)
	

def post_message(*useless_argument_thats_not_really_justified_but_oh_well):
	global en
	global client
	global usrname
	txt=en.get()
	en.delete(0,END)
	client.comm(usrname+"$MSG$"+txt)


#Data Stuff
chatlog=''
Host=enterbox('ENTER CHAT SERVER:')
Port=29876
Buffersize=4096
nameok=False
client=ClientObject(Host,Port,Buffersize)

#Username Registry
while nameok==False:
	usrname=enterbox('ENTER USERNAME:')
	pw=passwordbox('ENTER PASSWORD:')
	if usrname=='':
		exit()
	usrreg=client.comm('CONNECTION:'+usrname+':'+pw)
	if usrreg=='ACCESS GRANTED':
		nameok=True
	else:
		msgbox('Wrong password!')

#Main Frame
root = Tk()

#Text Field
text = Text(root)
text.insert(INSERT, "THIS IS A TEST")
text.pack()
thetime=0

#Scroll Bar
scrollbar=Scrollbar(root, command=text.yview)
text.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT,fill=Y)

#Entry field
en=Entry(root,width=60)
en.bind('<Return>', post_message)
en.pack( side = LEFT )
EnterButton=Button(root, text ="Enter", command = post_message)
EnterButton.pack( side = LEFT )

#Update
text.after(500,updatetext)

#Launch
root.title('TEST CHAT - '+usrname)
root.mainloop()
client.comm('LOGOUT:'+usrname+':'+pw)
