from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer
from PySide2.QtGui import QCloseEvent
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class SwitchOverrideShutdown(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.state=args[0]
		self.ret=[]

	#def __init__

	def run (self,*args):

		self.ret=Bridge.n4dManager.switchOverrideShutdown(self.state)
	
	#def run

#class SwitchOverrideShutdown		

class Bridge(QObject):


	def __init__(self,ticket=None,passwd=None):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.n4dManager=self.core.n4dManager
		self.overrideError=False

		#self.initBridge(ticket,passwd)

	#def __init_-

	def loadConfig(self):

		self._isClientShutDownOverride=Bridge.n4dManager.isClientShutdownOverride()

	#def getConfig

	def _getIsClientShutDownOverride(self):

		return self._isClientShutDownOverride

	#def _getIsClientShutDownOverride

	def _setIsClientShutDownOverride(self,isClientShutDownOverride):

		if self._isClientShutDownOverride!=isClientShutDownOverride:
			self._isClientShutDownOverride=isClientShutDownOverride
			self.on_isClientShutDownOverride.emit()

	#def _setIsClientShutDownOverride

	@Slot(bool)
	def overrideShutdownSwitch(self,state):

		self.isClientShutDownOverride=state
		self.overrideShutDown=SwitchOverrideShutdown(self.isClientShutDownOverride)
		self.overrideShutDown.start()
		self.overrideShutDown.finished.connect(self._overrideShutdownSwitch)

	#def overrrideShutdownSwitch

	def _overrideShutdownSwitch(self):

		INCOMPATIBILITY_OVERRIDE_OPTION=-40

		if not self.overrideShutDown.ret[1]:
			if self.overrideShutDown.ret[0]=='Enable':
				self.overrideError=True
				self.core.mainStack.showMessage=[True,INCOMPATIBILITY_OVERRIDE_OPTION]	
		else:
			self.overrideError=False

		self.isClientShutDownOverride=Bridge.n4dManager.isClientShutdownOverride()

	#def _overrrideShutdownSwitch

	on_isClientShutDownOverride=Signal()
	isClientShutDownOverride=Property(bool,_getIsClientShutDownOverride,_setIsClientShutDownOverride,notify=on_isClientShutDownOverride)

#class Bridge

import Core
