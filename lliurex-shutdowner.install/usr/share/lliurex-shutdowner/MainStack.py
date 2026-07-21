from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,QUrl
from PySide6.QtGui import QCloseEvent,QDesktopServices
import os 
import sys
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class GatherInfo(QThread):

	infoGathered=Signal(bool)

	def __init__(self,manager):

		super().__init__()
		self.manager=manager
	
	#def __init__
		
	def run(self,*args):
		
		ret=self.manager.loadInfo()
		self.infoGathered.emit(ret)

	#def run

class SaveInfo(QThread):

	def __init__(self,manager,newVar):

		super().__init__()
		self.manager=manager
		self.newVar=newVar
	
	#def __init__
		
	def run(self,*args):
		
		self.manager.setShutdownerValues(self.newVar)

	#def run

class Bridge(QObject):

	INCORRECT_SERVER_ERROR=-50
	LOAD_INFO_ERROR=-60

	KIRIGAMI_MSG_OK=0
	KIRIGAMI_MSG_ERROR=1
	KIRIGAMI_MSG_WARNING=2
	KIRIGAMI_MSG_INFO=3

	currentStackChanged=Signal()
	currentOptionStackChanged=Signal()
	showMessageChanged=Signal()
	isThereAnErrorChanged=Signal()
	closeGuiChanged=Signal()

	def __init__(self):

		super().__init__()
		self.core=Core.Core.get_core()
		self.n4dManager=self.core.n4dManager
		self.cronContent="%s %s * * %s root %s >> /var/log/syslog\n"
		self._isThereAnError={"show":False,"msgCode":""}
		self._closeGui=False
		self.saveInfoT=None

	@Property(int, notify=currentStackChanged)
	def currentStack(self):

		return self._currentStack

	#def currentStack	

	@currentStack.setter
	def currentStack(self,currentStack):
		
		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.currentStackChanged.emit()	

	#def currentStack

	@Property(int,notify=currentOptionStackChanged)
	def currentOptionStack(self):

		return self._currentOptionStack

	#def currentOptionStack	

	@currentOptionStack.setter
	def currentOptionStack(self,currentOptionStack):
		
		if self._currentOptionStack!=currentOptionStack:
			self._currentOptionStack=currentOptionStack
			self.currentOptionStackChanged.emit()	

	#def _setcurrentOptionStack

	@Property(dict,notify=showMessageChanged)
	def showMessage(self):

		return self._showMessage

	#def showMessage
	
	@showMessage.setter
	def showMessage(self,showMessage):

		if self._showMessage!=showMessage:
			self._showMessage=showMessage
			self.showMessageChanged.emit()

	#def showMessage

	@Property(dict, notify=isThereAnErrorChanged)
	def isThereAnError(self):

		return self._isThereAnError

	#def isThereAnError

	@isThereAnError.setter
	def isThereAnError(self,isThereAnError):

		if self._isThereAnError!=isThereAnError:
			self._isThereAnError=isThereAnError
			self.isThereAnErrorChanged.emit()

	#def isThereAnError

	@Property(bool,notify=closeGuiChanged)
	def closeGui(self):

		return self._closeGui

	#def closeGui

	@closeGui.setter
	def closeGui(self,closeGui):

		if self._closeGui!=closeGui:
			self._closeGui=closeGui
			self.closeGuiChanged.emit()

	#def closeGui

	def initBridge(self):

		self._currentStack=0
		self._currentOptionStack=0
		self._showMessage={"show":False,"msgCode":"","type":""}
		self.previousError=""

		ret=self.n4dManager.setServer(sys.argv[1],sys.argv[2])
		if not ret:
			self.isThereAnError={"show":True,"msgCode":Bridge.INCORRECT_SERVER_ERROR}
			return
		
		self.gatherInfoT=GatherInfo(self.n4dManager)
		self.gatherInfoT.start()
		self.gatherInfoT.infoGathered.connect(self._loadConfig)
		self.gatherInfoT.finished.connect(self.gatherInfoT.deleteLater)

	#def initBridge	
	
	@Slot(bool)
	def _loadConfig(self,ret):

		if not ret:
			self.isThereAnError={"show":True,"msgCode":Bridge.LOAD_INFO_ERROR}
			return

		self.core.clientStack.loadConfig()
		self.core.serverStack.loadConfig()
		self.core.settingsStack.loadConfig()
		
		if self.core.clientStack.loadError and self.core.serverStack.loadError:
			self.isThereAnError={"show":True,"msgCode":Bridge.LOAD_INFO_ERROR}
			return

		self.saveValuesTimer = QTimer(None)
		self.saveValuesTimer.timeout.connect(self.saveValues)
		self.saveValuesTimer.start(5000)
		self.countToShowError=0
		self.waitTimeError=20
		self.currentStack=1

	#def _loadInfo	

	def checkChanges(self):

		newVar=self.core.clientStack.gatherValues()
		if newVar==self.n4dManager.shutdownerVar:
			return True

		error=self.core.clientStack.checkAnyDayChecked()
		if error.get("error"):
			if self.previousError!=error.get("code"):
				self.previousError=error.get("code")
				self.showMessage={"show":True,"msgCode":error.get("code"),"type":Bridge.KIRIGAMI_MSG_ERROR}
			return False

		error=self.core.serverStack.checkCompatClientServer(newVar)
		if error.get("error"):
			if self.previousError!=error.get("code"):
				self.previousError=error.get("code")
				self.showMessage={"show":True,"msgCode":error.get("code"),"type":Bridge.KIRIGAMI_MSG_ERROR}
			return False
		
		self.countToShowError=0
		self.previousError=""
		self.n4dManager.setShutdownerValues(newVar)
		dayConfigured=False
		
		if self.core.clientStack.cronSwitch and not any(self.core.clientStack.weekClientValues.values()):
			return False
		
		return True
	
	#def checkChanges	

	def saveValues(self):

		newVar=self.core.clientStack.gatherValues()

		if newVar==self.n4dManager.shutdownerVar:
			if not self.core.settingsStack.overrideError:
				self.showMessage={"show":False,"msgCode":"","type":""}	
				self.previousError=""
				self.countToShowError=0
			return

		error=self.core.clientStack.checkAnyDayChecked()
		if error.get("error"):
			if self.previousError!=error.get("code"):
				self.previousError=error.get("code")
				self.showMessage={"show":True,"msgCode":error.get("code"),"type":Bridge.KIRIGAMI_MSG_ERROR}
				self.countToShowError=0
			return 

		error=self.core.serverStack.checkCompatClientServer(newVar)
		if error.get("error"):
			self.countToShowError+=5
			if self.countToShowError>self.waitTimeError:
				if self.previousError!=error.get("code"):
					self.previousError=error.get("code")
					self.showMessage={"show":True,"msgCode":error.get("code"),"type":Bridge.KIRIGAMI_MSG_ERROR}
					self.countToShowError=0

			return

		if not self.core.settingsStack.overrideError:
			if self.saveInfoT is not None and self.saveInfoT.isRunning():
				return
			self.showMessage={"show":False,"msgCode":"","type":""}
			self.previousError=""
			self.countToShowError=0
			self.saveInfoT=SaveInfo(self.n4dManager,newVar)
			self.saveInfoT.start()

	#def saveValues

	def stopServices(self):

		if hasattr(self,'saveValuesTimer'):
			self.saveValuesTimer.stop()

		if self.saveInfoT is not None and self.saveInfoT.isRunning():
			self.saveInfoT.requestInterruption()
			self.saveInfoT.wait()

	#def stopServices

	@Slot()
	def openHelp(self):

		helpUrl='https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Lliurex+Shutdowner'
		QDesktopServices.openUrl(QUrl(helpUrl))

	@Slot(int)
	def manageTransitions(self,stack):

		if self.currentOptionStack!=stack:
			self.currentOptionStack=stack
			self.core.settingsStack.overrideError=False

	#def manageTransitions

	@Slot()
	def closeShutdowner(self):
		
		if self.isThereAnError.get("show"):
			self.closeGui=False

		acceptedClose=self.checkChanges()
		
		if acceptedClose:
			if not self.core.clientStack._isStandAlone:
				self.core.clientStack.clientTimer.stop()
			self.saveValuesTimer.stop()
			self.closeGui=True
		else:
			self.closeGui=False
	
	#def closeShutdowner	

#class Bridge

import Core
