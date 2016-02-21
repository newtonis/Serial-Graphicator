import time

class Timer:
	def __init__(self):
		self.reference = 0
		self.stopRef   = 0
		self.stoped = False
		self.ms = 0
		self.s  = 0
		self.m  = 0
	def Reset(self):
		self.stoped = False
	def Stop(self):
		self.stopRef = time.time()
		self.stoped = True
	def Play(self):
		if self.stoped:
			self.reference = time.time() - ( time.time()-self.stopRef ) #set the current referece
			self.stoped = False
		else:
			self.reference = time.time()
	def Update(self):
		dif = time.time() - self.reference 
		self.ms = (dif * 1000) % 1000
		self.s  = dif % 60
		self.m  = dif / 60
	def GetTime(self):
		self.Update()
		return {"ms":self.ms,"s":self.s,"m":self.m}
	def MS(self):
		dif = time.time() - self.reference
		return dif*1000



def BlitInCenter(a , b):
	aw , ah = a.get_size()
	bw , bh = b.get_size()

	a.blit(b , (aw/2-bw/2 , ah/2-bh/2))
def BlitInFirstQuarterX(a,b):
	aw , ah = a.get_size()
	bw , bh = b.get_size()

	a.blit(b , (aw/4-bw/2, ah/2-bh/2+3) )
def BlitInFirstQuarter(a , b):
	aw , ah = a.get_size()
	bw , bh = b.get_size()

	a.blit(b , (aw/4-bw/2 , ah/4-bh/2))
def BlitInThirdQuarter(a , b):
	aw , ah = a.get_size()
	bw , bh = b.get_size()

	a.blit(b , (aw/4*3-bw/2 , ah/4*3-bh/2))
def BlitInCenterX(a , b , y):
	aw , ah = a.get_size()
	bw , bh = b.get_size()

	a.blit(b , (aw/2-bw/2 , y))

def BlitInCenterY(a , b , x):
	aw , ah = a.get_size()
	bw , bh = b.get_size()

	a.blit(b , (x , ah/2-bh/2))

def BlitInFirstQuarterY(a , b):
	aw , ah = a.get_size()
	bw , bh = b.get_size()

	a.blit(b , (aw/2-bw/2 , ah/4-bh/2))