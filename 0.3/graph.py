import pygame
import fonts
from utils import *
import serial.tools.list_ports
import serial
import thread
import images
import json
import ast
from serialModule import *
import colors
from random import *
from Queue import *

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 700

baudrates = [4800 ,9600 , 14400 , 19200 , 28800 , 38400, 57600 , 115200]
intervals = [60000 , 30000 , 20000, 18000 ,15000 , 12000 , 10000 , 7500 , 5000 , 3000, 2000 , 1000]

def AddBorder(surface):
	pygame.draw.line(surface, (0,0,0), (0,0), (0,surface.get_size()[1]),2)
	pygame.draw.line(surface, (0,0,0), (0,0), (surface.get_size()[0],0),2)

	pygame.draw.line(surface, (0,0,0), (surface.get_size()[0]-2,0), (surface.get_size()[0]-2,surface.get_size()[1]),2)
	pygame.draw.line(surface, (0,0,0), (0,surface.get_size()[1]-2), (surface.get_size()[0],surface.get_size()[1]-2),2)

class Selector:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 20
    def Refresh(self, screen):
        mx , my = pygame.mouse.get_pos()
        if mx > self.x - self.size/2 and mx < self.x + self.size/2 and my > self.y - self.size/2 and my < self.y + self.size/2:
            color = (0,100,0)
        else:
            color = (100,100,100)

        surface = pygame.surface.Surface((self.size,self.size))
        surface.fill(color)
        screen.blit(surface,(self.x - surface.get_size()[0]/2 ,self.y - surface.get_size()[1]/2))
    def Pressed(self):
        mx , my = pygame.mouse.get_pos()
        if mx > self.x - self.size/2 and mx < self.x + self.size/2 and my > self.y - self.size/2 and my < self.y + self.size/2:
            if pygame.mouse.get_pressed()[0]:
                return True
        return False

class BasicApp:
	def __init__(self):
		self.headGlobal = None
		self.screen = None

	def Refresh(self):
		pass
	def QuitFor(self, app):
		if app == None:
			self.headGlobal.Quit()
		else:
			self.headGlobal.SetNewApp( app )
	def Kill(self):
		pass

class OptionSelector:
	def __init__(self , width , x , y , size = 50 , textsize = 30 , centermode = False):
		self.options = []
		self.width = width
		self.x = x
		self.y = y
		self.selected = 0
		self.size = size
		self.textSize = textsize
		self.centermode = centermode
	def AddOption( self , icon , text):
		self.options.append({"icon":icon,"text":text})
	def Refresh(self , screen):
		add = self.x

		mx , my = pygame.mouse.get_pos()
		for x in range(len(self.options)):
			if x == self.selected:
				sel = 1
			else:
				sel = 0
			if sel:
				background = (100,100,100)
			else:
				background = (50,50,50)

			size = self.width / len(self.options)
			surface = pygame.surface.Surface((size,self.size))
			surface.fill(background)
			text = fonts.adamCG[str(self.textSize)].render(self.options[x]["text"],1,(200,200,200))
			if self.centermode:
				BlitInCenter(surface,text)
			else:
				BlitInFirstQuarterX(surface,text)
			if self.options[x]["icon"]:
				BlitInCenterY(surface,self.options[x]["icon"],size-20-self.options[x]["icon"].get_size()[0])
			screen.blit(surface,(add, self.y))
			
			if mx > self.x + add and mx < self.x + add + size and my > self.y and my < self.y + 50:
				if pygame.mouse.get_pressed()[0]:
					self.selected = x

			add += size
	def GetSelected(self):
		return self.options[self.selected]["text"]

class ShowItem:
	def __init__(self , x , y  , color , name ):
		self.x = y
		self.y = x
		self.btx = x 
		self.bty = y
		self.speed = 2
		self.color = color
		self.name = name
		self.last_update = None
		self.status = True
		self.last_press = False
	def SetPosition(self , tx,ty):
		self.btx = tx
		self.bty = ty
		self.tx = tx
		self.ty = ty
	def UpdatePosition(self):
		if self.last_update == None:
			self.last_update = time.time()
			return 0
		dif = time.time() - self.last_update
		self.last_update = time.time()

		self.x += (-self.x+self.tx) * self.speed * dif 
		self.y += (-self.y+self.ty) * self.speed * dif 
	def Focused(self):
		mx , my = pygame.mouse.get_pos()
		if mx > self.x and mx < self.x + 200:
			if my > self.y and my < self.y + 30:
				return True
		return False
	def Refresh(self,screen):

		if not pygame.mouse.get_pressed()[0]:
			self.last_press = False
		
		if self.status:
			if self.Focused():
				self.ty = self.bty
				self.tx = self.btx + 10
				if pygame.mouse.get_pressed()[0] and not self.last_press:
					self.status = False
					self.last_press = True
			else:
				self.ty = self.bty
				self.tx = self.btx
		else:
			if self.Focused():
				if pygame.mouse.get_pressed()[0] and not self.last_press:
					self.status = True
					self.last_press = True
			self.tx = self.btx + 150
			self.ty = self.bty

		surface = pygame.surface.Surface((200,30))
		surface.fill(self.color)
		nameSurface = fonts.adamCG[str(22)].render(self.name,1,(0,0,0))
		BlitInCenterX(surface,nameSurface,5)
		AddBorder(surface)

		screen.blit(surface,(self.x,self.y))

def GetTimeName(ms):
	if ms <= 3000:
		return str(ms)+"ms"

	if ms < 1000 * 120:
		ms = int(ms)
		ms /= 100
		ms = float(ms)
		ms /= 10
		return str(ms) +"s"
	ms = int(ms)
	ms /= 6000
	ms = float(ms)
	ms /= 10
	return str(ms) +"m"

def GetValueName(v):
	if v < 0:
		add = '-'
		v = -v
	else:
		add = ''

	if v <= 500:
		return str(v)
	v /= 100
	v = float(v)
	v /= 10
	if (v <= 500):
		return add + str(v) + "k"
	v = int(v)
	v /= 100
	v = float(v)
	v /= 10
	if (v <= 500):
		return add + str(v) + "M"
	v = int(v)
	v /= 100
	v = float(v)
	v /= 10
	return add + str(v) + "MM"
def GetValueName2(v):
	if v < 0:
		add = '-'
		v = -v
	else:
		add = ''

	if v <= 500:
		return str(v)
	v /= 10
	v = float(v)
	v /= 100
	if (v <= 500):
		return add + str(v) + "k"
	v = int(v)
	v /= 10
	v = float(v)
	v /= 100
	if (v <= 500):
		return add + str(v) + "M"
	v = int(v)
	v /= 10
	v = float(v)
	v /= 100
	return add + str(v) + "MM"

class GraphData:
	def __init__(self , name , color , show_item):

		self.name = name 
		self.color = color
		self.last_pkg = 0
		self.graph_max = 1
		self.graph_min = -1
		self.graph_content = dict()
		
		self.last_value = 0
		self.hold_value = 0
		self.timeDraw = 60000

		self.width =  200
		self.height = 200
		self.last_value = 0
		self.show_item = show_item
		self.sorted = []

		self.circle_y = 0
		self.cty = 0
		self.speed = 20
		self.last_update = 0
	def EraseAll(self):
		self.graph_content = dict()
		self.sorted = []
	def SetHold(self):
		self.hold_value = self.last_value
	def GetEnabled(self):
		return self.show_item.status
	def UpdateCircleY(self):
		if self.last_update == 0:
			self.circle_y = self.cty 
			self.last_update = time.time()
			return
		dif = time.time() - self.last_update
		prop = -self.circle_y + self.cty
		self.circle_y += (-self.circle_y + self.cty ) * dif * self.speed
		self.last_update = time.time()
	def SetCircleY(self,cty):
		self.cty = cty
	def SetSize(self,w,h):
		self.width = w 
		self.height = h
	def AddNewContent(self,value):
		try:
			mkm = time.time()*1000
			if int(self.last_value) != 0 and mkm - int(self.last_value) < 1000:
				return 0
			mkm = int(mkm)

			self.graph_content[str(mkm)] = value
			self.sorted.append(str(mkm));
			self.last_value = value
		except:
			pass
	def GetMax(self):
		max_value = -1
		for x in range(len(self.graph_content.keys())):
			if self.graph_content[ self.graph_content.keys()[x] ] > max_value:
				max_value = self.graph_content[ self.graph_content.keys()[x] ]
		return max_value
	def GetMin(self):
		min_value = -1
		for x in range(len(self.graph_content.keys())):
			if self.graph_content[ self.graph_content.keys()[x] ] < min_value:
				min_value = self.graph_content[ self.graph_content.keys()[x] ]
		return min_value
	def GetPeak(self):
		return max( self.GetMax() , -self.GetMin())
	def SetTimeDraw(self, time):
		self.timeDraw = time
	def GetDrawPoints(self):
		areaShow = self.GetPeak()
	def GetLastData(self):
		return self.last_value	

class GraphDisplay:
	def __init__(self , widthTotal , heightTotal , x , y):
		colors.SetColors()
		self.variables = []
		self.reference = dict()
		self.settles = dict() ## points on time that divides the table

		self.timeId = 0
		self.timeShow = intervals[self.timeId] ### 30 seconds of memory
		self.X0change = 0
		self.X1change = 0
		self.Y0change = 0
		self.Y1change = 0
		self.last_pressed = False

		self.timer = Timer()
		self.widthA = widthTotal * 75 / 100
		self.widthB = widthTotal * 25 / 100
		self.widthTotal = widthTotal
		self.graphH = heightTotal - 10
		self.graphW = self.widthA-10
		self.height = heightTotal

		self.x = x
		self.y = y
		self.showItems = []

		self.graphMax = 1
		self.graphMin = -1

		self.holdSelector = OptionSelector(widthTotal * 35 / 100 , self.x , self.y + self.height , 30 , 20 , True)
		self.holdSelector.AddOption(None , "Release")
		self.holdSelector.AddOption(None , "Hold")
		self.holdTime = 0

		self.playing = True

		self.drawMark = None
		self.drawMarkX = 0
		self.drawMarkY = 0

		self.new_hold = None
	def UpdateVariable(self , variable , value):
		self.reference[variable].AddNewContent(value)
	def CreateVariable(self , name , color):
		self.variables.append( name )
		show = ShowItem( SCREEN_WIDTH , SCREEN_HEIGHT , color , name)
		self.reference[name] = GraphData(name,color,show)
		self.UpdateShowPositions()
	def UpdateShowPositions(self):
		center_y = self.height / 2 + self.y 
		distance = 40
		start_y = center_y - len(self.variables)*20
		for x in range(len(self.variables)):
			self.reference[self.variables[x]].show_item.SetPosition(self.x+self.widthA+10 , start_y)
			start_y += distance

	def FreshValue(self, variable , value , color):
		#print variable , value
		if not self.playing:
			return 0
		try:
			if int(value) > 100000000:
				print "overflow" , value
				return 0
			if int(value) < -100000000:
				print "overflow",value
				return 0
			if not self.reference.has_key(variable):
				self.CreateVariable( variable , color)
			
			#print variable , value 
			self.UpdateVariable(variable , value)
		except:
			print "value error"
	def CalcGraph(self):
		pass
	def GetArea(self):
		area = 2

		for x in range(len(self.variables)):
			if not self.reference[ self.variables[x] ].GetEnabled():
				continue
			#print x , self.reference[ self.variables[x] ] .GetPeak()
			if int ( self.reference[ self.variables[x] ].GetPeak() ) * 2 > area:
				area = self.reference[ self.variables[x] ].GetPeak() * 2
				print "edit"
		
		self.area = area

	def GetGraphSurface(self):
		self.GetArea()

		graph_surface = pygame.surface.Surface((self.widthA , self.height))
		graph_surface.fill((100,100,100))

		background = pygame.surface.Surface((self.widthA-10,self.height-10))
		background.fill((220,220,220))
		pygame.draw.line(background,(0,0,0),(0,self.graphH/2),(self.graphW,self.graphH/2))
		
		pygame.draw.line(background,(0,0,0),(25,0),(25,self.graphH))
		pygame.draw.line(background,(0,0,0),(self.graphW-25,0),(self.graphW-25,self.graphH))

		text = fonts.fontConsole[str(20)].render(GetTimeName(self.timeShow),1,(0,0,0))
		background.blit(text ,(27,self.graphH/2-20))
		self.X0change = 27
		self.X1change = 27 + text.get_size()[0]
		self.Y0change = self.graphH/2-20
		self.Y1change = self.graphH/2-20 + text.get_size()[1]

		#higher = 1
		#lower  = -1
		if self.playing:
			current_time = time.time()*1000
		else:
			if self.new_hold:
				current_time = self.new_hold
			else:
				current_time = self.holdTime

		drawn = False

		mx , my = pygame.mouse.get_pos()
		mx -= self.x
		my -= self.y
		flagcont = True
		for x in range(len(self.variables)):
			if not self.reference[ self.variables[x] ].GetEnabled():
				continue
			#lentime = self.reference[ self.variables[x] ] . timeDraw
			lentime = self.timeShow
			vref =  self.reference[ self.variables[x] ]
			content = self.reference[self.variables[x]].graph_content
			#data = []
			color = self.reference[self.variables[x]].color
			delete = []
			sordel = []
			last_x = 0
			last_y = 0
			points = []
			for y in range(len(vref.sorted)):
				moment = vref.sorted[y]
				value = int ( content[ str(moment) ] )
				
				dif = int(current_time) - int(moment)
				if dif > intervals[0]:
					delete.append(vref.sorted[y] )
					sordel.append(y)
					#continue # too much time

				start_x = 25
				end_x = self.graphW - 25
				#print start_x , end_x

				value = (-value) + int(self.area)/2
				min_draw = 20
				max_draw = self.graphH - 20
			
				position_y = float(value) / float(self.area) * (max_draw-min_draw) + min_draw;
				position_x = float(lentime-dif) / float(lentime)
				real_x = start_x + (end_x-start_x) * position_x #(position_x goest from 0 to 1)
				#print real_x
				position_y = int(position_y)
				real_x = int(real_x)

				
				if last_x != 0:
					#pygame.draw.circle(background,color,(real_x,position_y),1)
					pygame.draw.line(background,color,(last_x,last_y),(real_x,position_y),1)
				last_x = real_x
				last_y = position_y

				points.append([real_x,position_y])
			pos = 0

			for y in range(len(vref.sorted)):
				real_x = points[y][0]
				position_y = points[y][1]
				special = False
				if not self.playing and not drawn:
					if mx > real_x-10 and mx < real_x+10 and my > position_y - 10 and my < position_y + 10:
						drawn = True
						pos = y
						special = True
				if (not self.playing) and (not special):
					pygame.draw.circle(background , self.reference[self.variables[x]].color , (real_x,position_y) , 3)
					pygame.draw.circle(background , (200,200,200), (real_x,position_y) , 2)
				
			
			if drawn and flagcont and not self.playing:
				absolute = vref.sorted[pos]

				value = content[str(absolute)]
				if not self.new_hold:
					timea = int(current_time) - int(absolute)
				else:
					timea = int(self.holdTime) - int(absolute)
				flagcont = False
				real_x = points[pos][0]
				position_y = points[pos][1]
				pygame.draw.circle(background , self.reference[self.variables[x]].color , (real_x,position_y) , 10)
				pygame.draw.circle(background , (200,200,200), (real_x,position_y) , 7)
				surface = pygame.surface.Surface((200,20))
				surface.fill((255,255,255))
				AddBorder(surface)
				textValue = fonts.fontConsole[str(15)].render( GetTimeName( timea ) + " ; "+ GetValueName2( value ) , 1,(0,0,0) )
				BlitInCenter(surface,textValue)
				self.drawMark = surface 
				self.drawMarkX = real_x - 80 
				self.drawMarkY = position_y - 25
				if pygame.mouse.get_pressed()[0] and not self.last_pressed:
					self.last_pressed = True
					self.UpdateMode(self.timeId+1)
					if self.timeId == 0:
						self.new_hold = None
					else:
						self.new_hold = int(absolute)+intervals[self.timeId]/2


					
				#background.blit(surface , (real_x - 80 , position_y - 25))
				#data.append( [real_x , position_y] )
			delete.sort()
			for y in range(len(delete)-1,-1,-1):
				if self.reference[ self.variables[x] ].graph_content.has_key(delete[y]):
					del self.reference[ self.variables[x] ].graph_content[ delete[y] ]
			sordel.sort()
			for y in range(len(sordel)-1,-1,-1):				
				del self.reference[ self.variables[x] ].sorted[sordel[y]]
			#print len(self.reference[self.variables[x]].graph_content.keys())
			#data.sort()
			#for x in range(len(data)):
			#	if x != 0:
			#		pygame.draw.line(background,color,(data[x-1][0],data[x-1][1]),(data[x][0],data[x][1]))
			#	pygame.draw.circle(background,color,(data[x][0],data[x][1]),2)
		
		if flagcont == True:
			self.drawMark = None

		for x in range(len(self.variables)):
			if not self.reference[ self.variables[x] ].GetEnabled():
				continue
			value = (-self.reference[ self.variables[x] ].GetLastData()) + self.area/2
			#print self.reference[ self.variables[x] ].GetLastData() , value , area/2
			color = self.reference[ self.variables[x] ].color
			min_draw = 20
			max_draw = self.graphH - 20
			real_position = min_draw + (max_draw-min_draw) * value / (self.area)

			#print "real = " , value , area , real_position 
			if self.playing:
				self.reference[ self.variables[x] ].SetCircleY(real_position)
				self.reference[ self.variables[x] ].UpdateCircleY()

		for x in range(len(self.variables)):
			if not self.reference[ self.variables[x] ] .GetEnabled():
				continue
			y_pos = int( self.reference[ self.variables[x] ].circle_y )

			pygame.draw.circle(background, self.reference[self.variables[x]].color, (self.graphW-25,y_pos), 8)
			pygame.draw.circle(background, (200,200,200), (self.graphW-25,y_pos), 5)

		for x in range(len(self.settles.keys())):
			name = self.settles.keys()[x]
			moment = self.settles[name]["time"]
			color = self.settles[name]["color"]

			dif = int(current_time) - int(moment)
			lentime = self.timeShow

			start_x = 25
			end_x = self.graphW - 25
			position_x = float(lentime - dif) / float(lentime)

			real_x = start_x + (end_x-start_x) * position_x
			real_x = int(real_x)

			#text = fonts.adamCG[str(15)].render(name , 1 ,color)
			#text = pygame.transform.rotate(text,90)
			text = self.settles[name]["text"]

			pygame.draw.line(background,color,(real_x,0),(real_x,self.height))
			background.blit(text , (real_x-15,5))

		AddBorder(background)
		BlitInCenter(graph_surface,background)

		return graph_surface
	def GetRelPos(self,x):
		return self.reference[self.variables[x]].circle_y
	def GetListSurface(self):
		list_surface = pygame.surface.Surface((self.widthB,self.height))
		list_surface.fill((150,150,150))

		return list_surface
	def ClearData(self):
		for x in range(len(self.variables)):
			self.reference[ self.variables[x] ].EraseAll()
		self.settles = dict()
	def Refresh(self,screen):
		self.UpdateChangeScale() #check if user clicked to change scale
		self.CalcGraph()
		total_surface = pygame.surface.Surface((self.widthTotal,self.height))
		total_surface.blit( self.GetGraphSurface() , (0,0))
		total_surface.blit( self.GetListSurface () , (self.widthA,0))
		#self.BlitMaxMin( total_surface )
		screen.blit(total_surface,(self.x,self.y))
		for x in range(len(self.variables)):
			self.reference[self.variables[x]].show_item.UpdatePosition()
			self.reference[self.variables[x]].show_item.Refresh(screen)
		for x in range(len(self.variables)):
			if not self.reference[ self.variables[x] ].GetEnabled():
				continue
			if self.playing:
				last_value = self.reference[ self.variables[x] ].last_value
			else:
				last_value = self.reference[self.variables[x]].hold_value
			surface = pygame.surface.Surface((40,20))
			surface.fill((255,255,255))
			AddBorder(surface)
			textValue = fonts.adamCG[str(15)].render( GetValueName( last_value ),1,(0,0,0))
			BlitInCenter(surface,textValue)
			#print self.GetRelPos(x)
			screen.blit(surface , (self.x + self.widthA - 20 , self.y + self.GetRelPos(x) - 5 ))
		self.holdSelector.Refresh(screen)
		if self.holdSelector.GetSelected() == "Release":
			self.Release()
		elif self.holdSelector.GetSelected() == "Hold":
			self.Hold()

		if pygame.key.get_pressed()[pygame.K_h]:
			self.Hold()
			
		if pygame.key.get_pressed()[pygame.K_r]:
			self.Release()
			
		if self.drawMark:
			screen.blit(self.drawMark,(self.x + self.drawMarkX,self.y + self.drawMarkY))
	def Release(self):
		if self.playing == False:
			self.holdSelector.selected = 0
			self.ClearData()
			self.playing = True
			self.new_hold = None
	def Hold(self):
		if self.playing == True:
			print "Hold"
			self.holdSelector.selected = 1
			self.holdTime = time.time() * 1000
			for x in range(len(self.variables)):
				self.reference[ self.variables[x] ].SetHold()
			self.playing = False
	def UpdateChangeScale(self):
		if not pygame.mouse.get_pressed()[0]:
			self.last_pressed = False
		mx , my = pygame.mouse.get_pos()
		if mx > self.x + self.X0change and mx < self.x + self.X1change:
			if my > self.y + self.Y0change and my < self.y + self.Y1change:
				if pygame.mouse.get_pressed()[0] and not self.last_pressed:
					self.UpdateMode( self.timeId + 1)
					self.last_pressed = True
	def UpdateMode(self, mode):
		if mode >= len(intervals):
			mode = 0
		self.timeId = mode
		self.timeShow = intervals[self.timeId]
		for x in range(len(self.variables)):
			self.reference[ self.variables[x] ] . timeDraw = self.timeShow

	def BlitMaxMin(self , surface):
		textMax = fonts.adamCG[str(20)].render( GetValueName( self.area/2 ),1,(0,0,0))
		textMin = fonts.adamCG[str(20)].render( GetValueName( self.area/2 ),1,(0,0,0))
		textH = textMax.get_size()[1]/2 - 2
		surface.blit( textMax , (self.widthA + 20 , 25 - textH) )
		surface.blit( textMin , (self.widthA + 20 , self.graphH-25 - textH) )
	def AddSettle(self , name , color ):
		text = fonts.adamCG[str(15)].render(name , 1 ,color)
		text = pygame.transform.rotate(text,90)
		self.settles[name] = {"color":color , "time":time.time() * 1000,"text":text} ## settle moment

class Console:
	def __init__(self , x , y , width , height):
		self.x = x 
		self.y = y
		self.width = width
		self.height = height
		self.commands = []
		self.maxSize = 15
	def Refresh(self,screen):
		surface = pygame.surface.Surface((self.width , self.height))
		surface.fill((100,100,100))

		into = pygame.surface.Surface((self.width-20,self.height-20))
		into.fill((200,200,200))
		add = 0
		for x in range(len(self.commands)):
			text = fonts.fontConsole[str(25)].render(self.commands[x]["content"],1,self.commands[x]["color"])
			into.blit(text , (20,add))
			add += text.get_size()[1] + 5
		BlitInCenter(surface,into)
		screen.blit(surface,(self.x,self.y))

	def AddCommand(self, command , color):
		self.commands.append({"content":command,"color":color})
		if len(self.commands) > self.maxSize:
			self.commands = self.commands[1:len(self.commands)]

class ConnectionWindow(BasicApp):
	def __init__(self, port , baud , bnumber):
		self.port = port
		self.baudrate = baud
		self.bnumber = bnumber

		self.text = "Conneting to "+str(self.port)+" at "+str(self.baudrate)
		self.timer = Timer()

		self.selector = OptionSelector(SCREEN_WIDTH-100 , 50 , 70)
		self.selector.AddOption(images.icon_terminal,"Console")
		self.selector.AddOption(images.icon_graph,"Graph")
		#print self.port , self.baudrate
		
		self.ConnectionAlive = True

		self.plot = []
		self.console = []
		self.console_size = 20

		self.Console = Console(50 ,120,SCREEN_WIDTH-100,SCREEN_HEIGHT-200)
		self.graphDisplay = GraphDisplay(SCREEN_WIDTH-100,SCREEN_HEIGHT-200,50,120)


		self.last = ""
		self.recv = []
		self.timer.Play()
		self.serial = None
		self.area = 1
		#self.testThread = threading.Thread(target=self.ThreadConnection, args=())
		#self.testThread.start()
		#thread.start_new_thread(self.ThreadConnection,())
		self.exitSelector = Selector()
		self.pressed = False
	def Refresh(self):
		if pygame.key.get_pressed()[pygame.K_RETURN] and self.flag == False:
			self.flag = True
			self.graphDisplay.CreateVariable("Random name "+str(randrange(100)),colors.randomColor() )
		if not pygame.key.get_pressed()[pygame.K_RETURN]:
			self.flag = False

		self.UpdateConnection()

		self.screen.fill((200,200,200))

		text = fonts.adamCG[str(35)].render(self.text , 1, (40,40,40))
		BlitInCenterX(self.screen,text,20)
		mx , my = pygame.mouse.get_pos()

		if not pygame.mouse.get_pressed()[0]:
			self.pressed = False
		if my > 20 and my < text.get_size()[1] and not self.pressed:
			if pygame.mouse.get_pressed()[0]:
				self.pressed = True
				self.bnumber += 1
				if self.bnumber >= len(baudrates):
					self.bnumber = 0
				self.baudrate = baudrates[self.bnumber]
				self.serial = None
				self.text = "Conneting to "+str(self.port)+" at "+str(self.baudrate)
		self.selector.Refresh(self.screen)
		if self.selector.GetSelected() == "Console":
			self.shownArea = self.Console
		elif self.selector.GetSelected() == "Graph":
			self.shownArea = self.graphDisplay
		if pygame.key.get_pressed()[pygame.K_LEFT]:
			self.selector.selected = 0
		if pygame.key.get_pressed()[pygame.K_RIGHT]:
			self.selector.selected = 1

		self.shownArea.Refresh(self.screen)
		#if self.timer.MS() > 1000:
		#	self.timer.Reset()
		#	self.timer.Play()
		self.UpdateData()

		textExit = fonts.adamCG[str(35)].render("Go Back",1,(40,40,40))
		textX = SCREEN_WIDTH/7*6 - textExit.get_size()[0]/2 
		self.screen.blit(textExit, (textX , SCREEN_HEIGHT - textExit.get_size()[1] - 20))
		self.exitSelector.y = SCREEN_HEIGHT - textExit.get_size()[1] - 16 + self.exitSelector.size / 2
		self.exitSelector.x = textX + textExit.get_size()[0] + 30
		self.exitSelector.Refresh(self.screen)
		if self.exitSelector.Pressed():
			self.GoBack()


	def Handle(self,data):
		#print data
		try:
			converted = ast.literal_eval(data)
		except:
			return
		if not converted.has_key("COM"):
			return
		if converted["COM"] == "line":
			if not converted.has_key("value"):
				return
			if converted.has_key("color"):
				self.Console.AddCommand(converted["value"] , converted["color"])
			else:
				self.Console.AddCommand(converted["value"],(0,0,0))
		elif converted["COM"] == "plot":
			if not converted.has_key("name"):
				return 
			if not converted.has_key("value"):
				return
			if converted.has_key("color"):
				self.graphDisplay.FreshValue(converted["name"],converted["value"],converted["color"])
			else:
				self.graphDisplay.FreshValue(converted["name"],converted["value"],colors.randomColor())
		elif converted["COM"] == "Hold":
			self.graphDisplay.Hold()
		elif converted["COM"] == "Release":
			self.graphDisplay.Release()
		elif converted["COM"] == "Settle":
			if not converted.has_key("name"):
				return
			if not converted.has_key("color"):
				return
			self.graphDisplay.AddSettle( converted["name"] , converted["color"])
	def UpdateData(self):
		recv = self.recv
		self.recv = []
		for x in range(len(recv)):
			for y in range(len(recv[x])):
				self.Handle(recv[x][y])
	def UpdateConnection(self):
		if not self.serial:
			self.serial = SerialModule()
			self.serial.ConnectTo(self.port,self.baudrate)
			return 0
	
		#if self.serial.timer.MS() > 500:
		self.serial.Update()
		data = self.serial.GetData()
		if data != "":
			self.recv.append(data)
	def ThreadConnection(self):
		print "Thread connection started",self.port,self.baudrate

		while self.ConnectionAlive:
			testSerial = SerialModule()
			testSerial.ConnectTo(self.port,self.baudrate )
			
			testSerial.Update()
			data = testSerial.GetData()
			
		testSerial.Kill()
	def Kill(self):
		self.ConnectionAlive = False
	def GoBack(self):
		self.QuitFor(SelectionWindow())

def different(a ,b):
	if len(a) != len(b):
		return True
	for x in range(len(a)):
		if a[x]["data"] != b[x]["data"]:
			return True
	return False



class SelectionWindow(BasicApp):
	def __init__(self):
		BasicApp.__init__(self)
		self.status = 0
		self.ports = []
		
		self.timer = Timer()
		self.testConnection = True

		#self.testThread = threading.Thread(target=self.TestingThread, args=())
		#self.testThread.start()
		#thread.start_new_thread(self.TestingThread,())
		self.testing = -1
		self.status = 0
		self.baud   = 0

		self.serial = None
		self.last_pressed = False
	def Kill(self):
		self.testConnection = False
	def Refresh(self):
		self.UpdateConnection()

		self.screen.fill((200,200,200))
		text = fonts.adamCG[str(40)].render("Serial port selection",1,(0,0,0))
		BlitInFirstQuarterY(self.screen,text)
		mx , my = pygame.mouse.get_pos()
		y = 1
		for port in self.ports:
	
			if time.time() - port["last_time"] > 2:
				color = (100,100,100)
			else:
				color = (0,0,0)
			xdraw = SCREEN_WIDTH/2-150
			ydraw = SCREEN_HEIGHT/4+y*60

			text = fonts.adamCG[str(30)].render(port["data"][0] + " (" + str(port["baudrate"]) + ")" ,1,color)
			self.screen.blit(text,(xdraw,ydraw))
			port["button"].x = xdraw + 400 
			port["button"].y = ydraw + text.get_size()[1]/2
			port["button"].Refresh(self.screen)
			if port["button"].Pressed():
				self.Connect( port["data"][0] , port["baudrate"] , port["bnumber"])

			if mx > xdraw and mx < xdraw + text.get_size()[0] and my > ydraw and my < ydraw + text.get_size()[1]:
				if pygame.mouse.get_pressed()[0] and not self.last_pressed:
					self.last_pressed = True
					port["bnumber"] += 1
					if port["bnumber"] == len(baudrates):
						port["bnumber"] = 0
					port["baudrate"] = baudrates[port["bnumber"]]
			y += 1
		if self.timer.MS() > 2000:
			self.GetPorts()
		if not pygame.mouse.get_pressed()[0]:
			self.last_pressed = False
	def UpdateConnection(self):
		if self.testing == -1:
			return 0 # no testing at all
		#print "updating"
		if self.status == 0:
			self.status = 1
			self.serial = SerialModule()
			try:
				self.serial.ConnectTo(self.ports[self.testing]["data"][0] , self.ports[self.testing]["baudrate"])
			except OSError:
				self.status = 0
				print "Error permision denied"
		elif self.status == 1:
			self.status = 2
			self.serial.Update()
			data = self.serial.GetData()
			if len(data) == 0:
				self.testing += 1
				if self.testing >= len(self.ports):
					self.testing = 0
			else:
				self.ports[self.testing]["last_time"] = time.time()
				#self.ports[self.testing]["baudrate"] = baudrates[self.baud]
				#self.ports[self.testing]["bnumber"] = self.baud
				#self.baud = 0
				self.testing += 1
				if self.testing >= len(self.ports):
					self.testing = 0
			self.serial.Kill()
		elif self.status == 2:
			self.status = 0
	def GetPorts(self):
		try:
			ports = list(serial.tools.list_ports.comports())
		except:
			print "Error trying to obtain ports"
		real = []
		for p in ports:
			if p[2] != 'n/a':
				real.append({"status":"dead","data":p,"baudrate":4800,"last_time":0,"button":Selector(),"bnumber":0})
		
		if different(real , self.ports):
			self.ports = real
			self.testing = 0
	def Connect(self,port,baudrate,bnumber):
		self.serial.Kill()
		self.Kill()
		self.QuitFor(ConnectionWindow(port,baudrate ,bnumber))

class TestApp(BasicApp):
	def __init__(self):
		BasicApp.__init__(self)
		self.status = 0
		self.timer = Timer()
		self.timer.Play()

		self.showText = []

		self.show1 = False 
		self.show2 = False
		self.show3 = False 
		self.show3pos = 0
		self.whiteCycle = False

	def Refresh(self):
		if not self.whiteCycle:
			self.screen.fill((0,0,0))
		else:
			grey = self.timer.MS() *200 / 1000
			if grey > 200:
				grey = 200
				self.QuitFor(SelectionWindow())
			self.screen.fill((grey,grey,grey))
		if self.status == 0:
			if self.timer.MS() >= 200:
				self.status = 1
		elif self.status == 1:
			self.show1 = True
			if self.timer.MS() >= 400:
				self.status = 2
				self.timer.Reset()
				self.timer.Play()
		elif self.status == 2:
			self.show2 = True
			
			if self.timer.MS() >= 1000:
				self.status = 3
				self.timer.Reset()
				self.timer.Play()
				self.show3 = 1
				self.show3pos = -self.timer.MS()+SCREEN_WIDTH
		elif self.status == 3:
			self.show3pos = -self.timer.MS()+SCREEN_WIDTH
			if self.show3pos < 30:
				self.status = 4
				self.timer.Reset()
				self.timer.Play()
		elif self.status == 4:
			self.whiteCycle = True
		if self.show1:
			text = fonts.adamCG[str(110)].render("Serial",1,(200,200,200))
			BlitInFirstQuarter(self.screen,text)
		if self.show2:
			text2 = fonts.adamCG[str(110)].render("Graph",1,(200,200,200))
			BlitInThirdQuarter(self.screen,text2)
		if self.show3:
			text3 = fonts.adamCG[str(40)].render("Version 1.0 - available open source in github",1,(200,200,200))
			BlitInCenterY(self.screen,text3,self.show3pos)

class ApplicationGlobal:
	def __init__(self):
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption("Serial graphicator")
		self.status = True
		self.App = None
		self.flag = False
		self.lastpresssed = False
		self.fullscreen = 0
	def SetNewApp(self , app):
		self.App = app
		self.App.headGlobal = self
		self.App.screen = self.screen
	def Refresh(self):
		self.screen.fill((255,255,255))
		self.App.Refresh()
		pygame.display.update()
		if not pygame.key.get_pressed()[pygame.K_LCTRL]:
			self.flag = False
		if not pygame.key.get_pressed()[pygame.K_LCTRL]:
			self.flag = False
		if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_s] and not self.flag:
			self.flag = True
			name =  str( time.time() )+ ".png"
			pygame.image.save(self.screen , str( time.time() )+ ".png")
			print "screenshot ",name," saved"

		if pygame.key.get_pressed()[ pygame.K_F11 ] and not self.lastpresssed:
			self.lastpresssed = True
			if self.fullscreen == 0:
				self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.FULLSCREEN)
				self.fullscreen = 1
			else:
				self.fullscreen = 0
				self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

		if not pygame.key.get_pressed()[pygame.K_F11]:
			self.lastpresssed  = False
	def Quit(self):
		self.App.Kill()
		self.status = False

intialApp = TestApp()
connnectWindow = SelectionWindow()
def main():
	app = ApplicationGlobal()
	app.SetNewApp ( intialApp )

	while app.status:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				app.Quit()
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			app.Quit()

		app.Refresh()


if __name__ == "__main__":
	main()