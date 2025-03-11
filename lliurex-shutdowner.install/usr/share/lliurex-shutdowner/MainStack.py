from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer
from PySide2.QtGui import QCloseEvent
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class GatherInfo(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
	
	#def __init__
		
	def run(self,*args):
		
		time.sleep(1)
		self.ret=Bridge.n4dManager.loadInfo()

	#def run

class Bridge(QObject):

	def __init__(self):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.n4dManager=self.core.n4dManager
		self.cronContent="%s %s * * %s root %s >> /var/log/syslog\n"
		self._isThereAreError=False


	def initBridge(self):

		self._currentStack=0
		self._currentOptionStack=0
		self._showMessage=[False,""]
		self.previousError=""

		Bridge.n4dManager.setServer(sys.argv[1],sys.argv[2])
		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadConfig)

	#def initBridge	
	
	def _loadConfig(self):

		if self.gatherInfo.ret:
			self.core.clientStack.loadConfig()
			self.core.serverStack.loadConfig()
			self.core.settingsStack.loadConfig()
			
			self.saveValuesTimer = QTimer(None)
			self.saveValuesTimer.timeout.connect(self.saveValues)
			self.saveValuesTimer.start(5000)
			self.countToShowError=0
			self.waitTimeError=20
			self.currentStack=1
		else:
			self.isThereAreError=True

	#def _loadInfo	

	def _getCurrentStack(self):

		return self._currentStack

	#def _getCurrentStack	

	def _setCurrentStack(self,currentStack):
		
		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.on_currentStack.emit()	

	#def _setcurrentStack

	def _getCurrentOptionStack(self):

		return self._currentOptionStack

	#def _getCurrentOptionStack	

	def _setCurrentOptionStack(self,currentOptionStack):
		
		if self._currentOptionStack!=currentOptionStack:
			self._currentOptionStack=currentOptionStack
			self.on_currentOptionStack.emit()	

	#def _setcurrentOptionStack

	def _getShowMessage(self):

		return self._showMessage

	#def _getShowMessage
	
	def _setShowMessage(self,showMessage):

		if self._showMessage!=showMessage:
			self._showMessage=showMessage
			self.on_showMessage.emit()

	#def _setShowMessage

	def _getIsThereAreError(self):

		return self._isThereAreError

	#def _getIsThereAreError

	def _setIsThereAreError(self,isThereAreError):

		if self._isThereAreError!=isThereAreError:
			self._isThereAreError=isThereAreError
			self.on_isThereAreError.emit()

	#def _setIsThereAreError

	def checkChanges(self):

		newVar=self.core.clientStack.gatherValues()
		if newVar!=Bridge.n4dManager.shutdownerVar:
			error=self.core.serverStack.checkCompatClientServer(newVar)
			if not error[0]:
				self.countToShowError=0
				Bridge.n4dManager.shutdownerVar=newVar
				self.previousError=""
				Bridge.n4dManager.setShutdownerValues()
				dayConfigured=False
				for item in self.core.clientStack.weekClientValues:
					if item:
						dayConfigured=True
						break
				
				if self.core.clientStack.cronSwitch and not dayConfigured:
					return True
			
				return True
			else:
				if self.previousError!=error[1]:
					self.showMessage=error
					self.previousError=error[1]
				return False
		
		return True
	
	#def checkChanges	

	def saveValues(self):

		newVar=self.core.clientStack.gatherValues()

		if newVar!=Bridge.n4dManager.shutdownerVar:
			error=self.core.serverStack.checkCompatClientServer(newVar)
			if not error[0]:
				if not self.core.settingsStack.overrideError:
					self.showMessage=[False,""]
				self.previousError=""
				Bridge.n4dManager.shutdownerVar=newVar
				self.countToShowError=0
				t=threading.Thread(target=Bridge.n4dManager.setShutdownerValues)
				t.daemon=True
				t.start()
			else:
				self.countToShowError+=5
				if self.countToShowError>self.waitTimeError:
					if self.previousError!=error[1]:
						self.showMessage=error
						self.previousError=error[1]
						self.countToShowError=0
		else:
			if not self.core.settingsStack.overrideError:
				self.showMessage=[False,""]	
				self.previousError=""
				self.countToShowError=0
	
	#def saveValues

	@Slot()
	def openHelp(self):
		lang=os.environ["LANG"]

		if 'valencia' in lang:
			self.helpCmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Lliurex+Shutdowner.'
		else:
			self.helpCmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Lliurex-Shutdowner'
		
		self.openHelpT=threading.Thread(target=self._openHelp)
		self.openHelpT.daemon=True
		self.openHelpT.start()

	#def OpenHelp

	def _openHelp(self):

		os.system(self.helpCmd)

	#def _openHelp

	@Slot(int)
	def manageTransitions(self,stack):

		if self.currentOptionStack!=stack:
			self.currentOptionStack=stack
			self.core.settingsStack.overrideError=False

	#def manageTransitions

	@Slot(bool,result=bool)
	def closeShutdowner(self,state):
		
		if not self.isThereAreError:
			acceptedClose=self.checkChanges()
			if acceptedClose:
				if not self.core.clientStack._isStandAlone:
					self.core.clientStack.clientTimer.stop()
				self.saveValuesTimer.stop()
				return True
			else:
				return False
		else:
			return True

	#def closeShutdowner	

	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)

	on_currentOptionStack=Signal()
	currentOptionStack=Property(int,_getCurrentOptionStack,_setCurrentOptionStack, notify=on_currentOptionStack)

	on_showMessage=Signal()
	showMessage=Property('QVariantList',_getShowMessage,_setShowMessage, notify=on_showMessage)

	on_isThereAreError=Signal()
	isThereAreError=Property(bool,_getIsThereAreError,_setIsThereAreError,notify=on_isThereAreError)

#class Bridge

import Core
