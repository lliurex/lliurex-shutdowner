from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer
from PySide6.QtGui import QCloseEvent
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class SwitchOverrideShutdown(QThread):

	overrideSwitched=Signal(dict)

	def __init__(self,manager,action):

		super().__init__()
		self,manager=manager
		self.state=action

	#def __init__

	def run (self,*args):

		ret=self.manager.switchOverrideShutdown(self.state)
		self.overrideSwitched.emit(ret)
	
	#def run

#class SwitchOverrideShutdown		

class Bridge(QObject):

	isClientShutDownOverrideChanged=Signal()

	def __init__(self,ticket=None,passwd=None):

		super().__init__()
		self.core=Core.Core.get_core()
		self.n4dManager=self.core.n4dManager
		self.overrideError=False

		#self.initBridge(ticket,passwd)

	#def __init__

	@Property(bool,notify=isClientShutDownOverrideChanged)
	def isClientShutDownOverride(self):

		return self._isClientShutDownOverride

	#def isClientShutDownOverride

	@isClientShutDownOverride.setter
	def isClientShutDownOverride(self,isClientShutDownOverride):

		if self._isClientShutDownOverride!=isClientShutDownOverride:
			self._isClientShutDownOverride=isClientShutDownOverride
			self.isClientShutDownOverrideChanged.emit()

	#def isClientShutDownOverride

	def loadConfig(self):

		self._isClientShutDownOverride=self.n4dManager.isClientShutdownOverride()

	#def getConfig

	@Slot(bool)
	def overrideShutdownSwitch(self,state):

		self.isClientShutDownOverride=state
		self.overrideShutDownT=SwitchOverrideShutdown(self.n4dManager,self.isClientShutDownOverride)
		self.overrideShutDownT.start()
		sekf.overrideShutDownT.overrideSwitched.connect(self._overrideShutdownSwitch)
		self.overrideShutDownT.finished.connect(self.overrideShutDownT.deleteLater)

	#def overrrideShutdownSwitch

	@Slot(dict)
	def _overrideShutdownSwitch(self,ret):

		INCOMPATIBILITY_OVERRIDE_OPTION=-40

		if not ret.get("status"):
			if ret.get("action")=='Enable':
				self.overrideError=True
				self.core.mainStack.showMessage={"show":True,"msgCode":INCOMPATIBILITY_OVERRIDE_OPTION,"type":self.core.mainStack.KIRIGAMI_MSG_ERROR}	
		else:
			self.overrideError=False

		self.isClientShutDownOverride=self.n4dManager.isClientShutdownOverride()

	#def _overrrideShutdownSwitch

#class Bridge

import Core
