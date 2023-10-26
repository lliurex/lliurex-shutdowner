#!/usr/bin/env python3

import sys


import N4dManager
import SettingsStack
import ServerStack
import ClientStack
import MainStack

class Core:
	
	singleton=None
	DEBUG=False
	
	@classmethod
	def get_core(self):
		
		if Core.singleton==None:
			Core.singleton=Core()
			Core.singleton.init()

		return Core.singleton
		
	
	def __init__(self,args=None):

	
		self.dprint("Init...")
		
	#def __init__
	
	def init(self):

	
		self.n4dManager=N4dManager.N4dManager()
		self.settingsStack=SettingsStack.Bridge()
		self.serverStack=ServerStack.Bridge()
		self.clientStack=ClientStack.Bridge()
		self.mainStack=MainStack.Bridge()
		
		self.mainStack.initBridge()
	
		
	#def init

	def dprint(self,msg):
		
		if Core.DEBUG:
			
			print("[CORE] %s"%msg)
	
	#def  dprint
