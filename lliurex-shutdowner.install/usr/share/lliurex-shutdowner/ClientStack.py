from PySide6.QtCore import QObject,Signal,Slot,QThread,Property,QTimer
from PySide6.QtGui import QCloseEvent
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class Bridge(QObject):

	isCronEnabledChanged=Signal()
	initClockClientChanged=Signal()
	initWeekDaysClientChanged=Signal()
	detectedClientsChanged=Signal()
	
	def __init__(self,ticket=None,passwd=None):

		super().__init__()
		self.core=Core.Core.get_core()
		self.n4dManager=self.core.n4dManager
		self.shutdownBin="/usr/sbin/shutdown-lliurex"
		self._isStandAlone=self.n4dManager.standAlone
		self._isClient=self.n4dManager.isClient
		self._detectedClients="0"
		self.loadError=False

	#def __init__

	@Property(bool,notify=isCronEnabledChanged)
	def isCronEnabled(self):

		return self._isCronEnabled

	#def isCronEnabled

	@isCronEnabled.setter
	def isCronEnabled(self,isCronEnabled):

		if self._isCronEnabled!=isCronEnabled:
			self._isCronEnabled=isCronEnabled
			self.isCronEnabledChanged.emit()

	#def isCronEnabled

	@Property(dict,notify=initClockClientChanged)
	def initClockClient(self):

		return self._initClockClient

	#def initClockClient

	@initClockClient.setter
	def initClockClient(self,initClockClient):

		if self._initClockClient!=initClockClient:
			self._initClockClient=initClockClient
			self.initClockClientChanged.emit()

	#def initClockClient

	@Property(dict,notify=initWeekDaysClientChanged)
	def initWeekDaysClient(self):

		return self._initWeekDaysClient

	#def initWeekDaysClient

	@initWeekDaysClient.setter
	def initWeekDaysClient(self,initWeekDaysClient):

		if self._initWeekDaysClient!=initWeekDaysClient:
			self._initWeekDaysClient=initWeekDaysClient
			self.initWeekDaysClientChanged.emit()

	#def initWeekDaysClient

	@Property(str,notify=detectedClientsChanged)
	def detectedClients(self):

		return self._detectedClients

	#def detectedClients	

	@detectedClients.setter
	def detectedClients(self,detectedClients):

		if self._detectedClients!=detectedClients:
			self._detectedClients=detectedClients
			self.detectedClientsChanged.emit()	

	#def detectedClients

	@Property(bool,constant=True)
	def isStandAlone(self):

		return self._isStandAlone

	#def isStandAlone

	@Property(bool,constant=True)
	def isClient(self):
		
		return self._isClient

	#def isClient	

	def loadConfig(self):

		clientValues=self.n4dManager.getCronValues()	

		if clientValues is None:
			self.loadError=True
			return

		if not clientValues:
			self.loadError=True
			return

		self._isCronEnabled=self.n4dManager.isCronEnabled()
		self.cronSwitch=copy.deepcopy(self._isCronEnabled)
		self._initClockClient={"hour":clientValues.get("hour"),"minute":clientValues.get("minute")}
		self.clockClientValues=copy.deepcopy(self._initClockClient)
		self._initWeekDaysClient={str(i):valor for i, valor in enumerate(clientValues.get("weekdays"))}
		self.weekClientValues=copy.deepcopy(self._initWeekDaysClient)

		if not self._isStandAlone:
			self.clientTimer = QTimer(None)
			self.clientTimer.timeout.connect(self.getClient)
			self.clientTimer.start(2000)
	
	#def loadConfig	

	def getClient(self):

		self.detectedClients=str(self.n4dManager.detectedClients)

	#def getClient

	def gatherValues(self):

		getServerValues=False
		newVar=copy.deepcopy(self.n4dManager.shutdownerVar)
		newVar["cron_enabled"]=self.cronSwitch

		if not self.cronSwitch or not any(self.weekClientValues.values()):
			newVar["cron_enabled"]=False
			return newVar

		for i in range(5):
			key=str(i)
			newVar["cron_values"]["weekdays"][i]=self.weekClientValues.get(key,False)

		newVar["cron_values"]["server_shutdown"]=self.core.serverStack.serverShut
		newVar["cron_values"]["hour"]=self.clockClientValues.get("hour")
		newVar["cron_values"]["minute"]=self.clockClientValues.get("minute")

		selectedDays=[
			str(int(k)+1)
			for k, v in self.weekClientValues.items()
			if v and k.isdigit() and int(k) <5
		]

		days=",".join(selectedDays)
		minute=self.clockClientValues.get("minute")
		hour=self.clockClientValues.get("hour")
		newVar["cron_content"]=self.core.mainStack.cronContent%(minute,hour,days,self.shutdownBin)
		
		if not self._isStandAlone and self.core.serverStack.serverShut:
			if self.core.serverStack.customServerShut:
				newVar=self.core.serverStack.gatherValuesServer(newVar)	
			else:
				newVar["server_cron"]["custom_shutdown"]=False
		
		return newVar

	#def gatherValues
	
	@Slot(bool)
	def getCronSwitchValue(self,state):
		
		self.cronSwitch=state
		self.isCronEnabled=state

	#getCronSwitchValue
	
	@Slot(dict)
	def getClockClientValues(self,data):

		changes={key:value for key,value in data.items() if self.initClockClient[key]!=value}

		if changes:
			self.initClockClient={**self.initClockClient,**changes}
		
		self.clockClientValues=self.initClockClient

	#def getClokClientValues
	
	@Slot(dict)
	def getWeekClientValues(self,data):

		changes={key:value for key,value in data.items() if self.initWeekDaysClient[key]!=value}

		if changes:
			self.initWeekDaysClient={**self.initWeekDaysClient,**changes}
		
		self.weekClientValues=self.initWeekDaysClient
	
	#def getWeekClientValues

	@Slot()
	def shutdownClientsNow(self):
		
		self.n4dManager.shutdownClients()
	
	#def shutdownClientsNow

#class Bridge

import Core
