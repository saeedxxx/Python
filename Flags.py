from Tkinter import *
from random import uniform as uni
from numpy import mean,exp
import tkFont,time
root=Tk()
w= Canvas(root,width=700,height=700,bg='white')
X=650;Y=50
w.create_line(Y,X,X,X,X,Y,Y,Y,Y,X,fill='black', width= 3)
w.pack()
Speed_x=100;Speed_y=0;CheckVar1 = IntVar();CheckVar2 = IntVar();CheckVar3 = IntVar()
CheckVar1.set(1);CheckVar2.set(1);CheckVar3.set(1);
p=[]
rx0=[];ry0=[]
class object:
	def __init__(self,rx,ry,links=(),vx=0,vy=0,fx=0,fy=0):
		rx0.append(rx);ry0.append(ry)
		self.rx,self.ry=rx,ry
		self.vx,self.vy=vx,vy
		self.fx,self.fy=fx,fy
		self.links=[(link,w.create_line(0,0,0,0,fill='magenta')) for link in links if link !=False ]
		self.p= w.create_oval(self.rx,self.ry,self.rx+1,self.ry+1,fill='black')
	def show_up(self):
		w.coords(self.p,self.rx,self.ry,self.rx+5,self.ry+5)
		for link in self.links:
			w.coords(link[1],p[link[0]].rx,p[link[0]].ry,self.rx,self.ry)
	def clear(self):
		w.delete(self.p)
		for link in self.links:
			w.delete(link[1])
		self.links=[]
side=18
b1= lambda x,y: x<side-1 and x+1+y*side
b2= lambda x,y: y<side-1 and x+(1+y)*side
b3= lambda x,y: x<side-1 and 0<y<side and x+1+(y-1)*side
b4= lambda x,y: x<side-1 and y<side-1 and x+1+(y+1)*side
net= lambda m,n: [ object(x*15+m,y*15+n,(b1(x,y),b2(x,y),b3(x,y),b4(x,y))) for y in xrange(side) for x in xrange(side)]

def force(m):
	for n in m.links:
		len= ((m.rx-p[n[0]].rx)**2 + (m.ry - p[n[0]].ry)**2)**0.5
		if len<10:	len=10
		f=((len-17)*5)**3/2.
		R=len**2
		fx=(f/R)*(m.rx-p[n[0]].rx)
		fy=(f/R)*(m.ry-p[n[0]].ry)
		m.fx-=fx
		m.fy-=fy
		p[n[0]].fx+=fx
		p[n[0]].fy+=fy
def wind(m):
	if CheckVar2.get()==1:
		for n in m.links:
			p[n[0]].fx+=(exp(-abs(min(rx0)-m.rx)/100.)*5+Wind_Oscillation(m))*Speed_x
			p[n[0]].fy+=Speed_y
			
def Wind_Oscillation(m):
	tmp=(time.time()+uni(0,2))%5
	if tmp>=2 and abs(min(rx0)-m.rx)>10:
		return tmp
	else:	return 0
def clear_force(m):
	m.fx=0
	m.fy=0
def speed(m):
	m.vx +=0.1*m.fx
	m.vy +=0.1*m.fy
	if (m.rx>X or m.rx<Y):	m.vx=0;m.vy=0
	if m.ry>X or m.ry<Y:	m.vy=0;m.vx=0
def position(m):
	m.rx += 0.002*m.vx
	m.ry += 0.002*m.vy
def attenuation(m):
	if CheckVar3.get()==1:
		m.vx *= 0.98
		m.vy *= 0.98
def graviy(m):
	if CheckVar1.get()==1:
		m.fy += 200
def frame():
	map(graviy,p)
	map(force,p)
	map(wind,p)
	map(speed,p)
	map(clear_force,p)
	map(position,p)
	map(attenuation,p)
	for o in p:
		o.show_up()
	root.after(10,frame) 
frame()
def klik(event):
	r=net(event.x,event.y)
	for n in p: n.clear()
	while p: p.pop()
	for n in r:	p.append(n)
root.bind("<Button-1>",klik)
def updatex(e):
	global Speed_x
	Speed_x=float(e)
def updatey(e):
	global Speed_y
	Speed_y=float(e)
top = Toplevel()
top.title("Speed controller")	
Throttle = Scale(top, from_=0, to=130, length=500,
                tickinterval=10, orient=HORIZONTAL,bg='white',troughcolor='orange', bd=5, command=updatex)
Throttle.set(60)
Throttle.pack()
Throttle = Scale(top, from_=-100, to=100, length=500,
                tickinterval=10, orient=HORIZONTAL,bg='white',troughcolor='orange', bd=5, command=updatey)
Throttle.set(-10)
Throttle.pack()
customFont = tkFont.Font(family="Tahoma", size=20)
C1 = Checkbutton(top, text = "Gravity", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0,font=customFont)
C2 = Checkbutton(top, text = "Wind", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0,font=customFont)
C3 = Checkbutton(top,text = "Attenuation", variable = CheckVar3, \
                 onvalue = 1, offvalue = 0,font=customFont)
C1.pack(side='left',padx=10,pady=5)
C2.pack(side='left',padx=10,pady=5)
C3.pack(side='left',padx=10,pady=5)
root.mainloop()