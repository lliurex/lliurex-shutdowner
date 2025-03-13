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

	def __init__(self,ticket=None,passwd=None):

		QObject.__init__(self)
		self.core=Core.Core.get_core()
		Bridge.n4dManager=self.core.n4dManager
		self.shutdownBin="/usr/sbin/shutdown-lliurex"
		self._isStandAlone=Bridge.n4dManager.standAlone
		self._isClient=Bridge.n4dManager.isClient
		self._detectedClients="0"
		self.loadError=False

	#def __init__

	def loadConfig(self):

		clientValues=Bridge.n4dManager.getCronValues()	

		if clientValues!=None:
			if len(clientValues)>0:
				self._isCronEnabled=Bridge.n4dManager.isCronEnabled()
				self.cronSwitch=copy.deepcopy(self._isCronEnabled)

				self._initClockClient=[clientValues["hour"],clientValues["minute"]]
				self.clockClientValues=copy.deepcopy(self._initClockClient)
				self._initWeekDaysClient=[clientValues["weekdays"][0],clientValues["weekdays"][1],clientValues["weekdays"][2],clientValues["weekdays"][3],clientValues["weekdays"][4]]
				self.weekClientValues=copy.deepcopy(self._initWeekDaysClient)

				if not self._isStandAlone:
					self.clientTimer = QTimer(None)
					self.clientTimer.timeout.connect(self.getClient)
					self.clientTimer.start(2000)
			else:
				self.loadError=True
		else:
			self.loadError=True

	#def loadConfig	

	def getClient(self):

		self.detectedClients=str(Bridge.n4dManager.detectedClients)

	#def getClient

	def _getIsStandAlone(self):

		return self._isStandAlone

	#def _getIsStandAlone

	def _getIsClient(self):
		
		return self._isClient

	#def _getIsClient	

	def _getIsCronEnabled(self):

		return self._isCronEnabled

	#def _getIsCronEnabled

	def _setIsCronEnabled(self,isCronEnabled):

		if self._isCronEnabled!=isCronEnabled:
			self._isCronEnabled=isCronEnabled
			self.on_isCronEnabled.emit()

	#def _setIsCronEnabled

	def _getInitClockClient(self):

		return self._initClockClient

	#def _getinitClockClient

	def _setInitClockClient(self,initClockClient):

		if self._initClockClient!=initClockClient:
			self._initClockClient=initClockClient
			self.on_initClockClient.emit()

	#def _setInitClockClient	

	def _getInitWeekDaysClient(self):

		return self._initWeekDaysClient

	#def _getInitWeekDaysClient

	def _setInitWeekDaysClient(self,initWeekDaysClient):

		if self._initWeekDaysClient!=initWeekDaysClient:
			self._initWeekDaysClient=initWeekDaysClient
			self.on_initWeekDaysClient.emit()

	#def _setInitWeekDaysClient	

	def _getDetectedClients(self):

		return self._detectedClients

	#def _getDetectedClients	

	def _setDetectedClients(self,detectedClients):

		if self._detectedClients!=detectedClients:
			self._detectedClients=detectedClients
			self.on_detectedClients.emit()	

	#def _setDetectedClients

	def gatherValues(self):

		getServerValues=False
		newVar=copy.deepcopy(Bridge.n4dManager.shutdownerVar)
		newVar["cron_enabled"]=self.cronSwitch

		if self.cronSwitch:

			dayConfigured=False

			for item in self.weekClientValues:
				if item:
					dayConfigured=True
					break
			
			if dayConfigured:

				newVar["cron_values"]["weekdays"][0]=self.weekClientValues[0]
				newVar["cron_values"]["weekdays"][1]=self.weekClientValues[1]
				newVar["cron_values"]["weekdays"][2]=self.weekClientValues[2]
				newVar["cron_values"]["weekdays"][3]=self.weekClientValues[3]
				newVar["cron_values"]["weekdays"][4]=self.weekClientValues[4]
				newVar["cron_values"]["server_shutdown"]=self.core.serverStack.serverShut
				newVar["cron_values"]["hour"]=self.clockClientValues[0]
				newVar["cron_values"]["minute"]=self.clockClientValues[1]

				days=""
				count=1
				for day in newVar["cron_values"]["weekdays"]:
					if day:
						days+="%s,"%count
					count+=1
				days=days.rstrip(",")
				newVar["cron_content"]=self.core.mainStack.cronContent%(self.clockClientValues[1],self.clockClientValues[0],days,self.shutdownBin)
				if not self._isStandAlone and self.core.serverStack.serverShut:
					if self.core.serverStack.customServerShut:
						newVar=self.core.serverStack.gatherValuesServer(newVar)	
					else:
						newVar["server_cron"]["custom_shutdown"]=False

			else:
				newVar["cron_enabled"]=False
		
		return newVar

	#def gatherValues
	
	@Slot(bool)
	def getCronSwitchValue(self,state):
		
		self.cronSwitch=state
		self.isCronEnabled=state

	#getCronSwitchValue
	
	@Slot('QVariantList')
	def getClockClientValues(self,values):

		if values[0]=="H":
			self.clockClientValues[0]=values[1]
		else:
			self.clockClientValues[1]=values[1]
		
		self.initClockClient=self.clockClientValues

	#def getClokClientValues
	
	@Slot('QVariantList')
	def getWeekClientValues(self,values):

		if values[0]=="MO":
			self.weekClientValues[0]=values[1]
		elif values[0]=="TU":
			self.weekClientValues[1]=values[1]
		elif values[0]=="WE":
			self.weekClientValues[2]=values[1]	
		elif values[0]=="TH":
			self.weekClientValues[3]=values[1]
		elif values[0]=="FR":
			self.weekClientValues[4]=values[1]	

		self.initWeekDaysClient=self.weekClientValues
	
	#def getWeekClientValues

	@Slot()
	def shutdownClientsNow(self):
		
		Bridge.n4dManager.shutdownClients()
	
	#def shutdownClientsNow

	isStandAlone=Property(bool,_getIsStandAlone,constant=True)
	isClient=Property(bool,_getIsClient,constant=True)

	on_isCronEnabled=Signal()
	isCronEnabled=Property(bool,_getIsCronEnabled,_setIsCronEnabled,notify=on_isCronEnabled)
	
	on_initClockClient=Signal()
	initClockClient=Property('QVariantList',_getInitClockClient,_setInitClockClient,notify=on_initClockClient)
	
	on_initWeekDaysClient=Signal()
	initWeekDaysClient=Property('QVariantList',_getInitWeekDaysClient,_setInitWeekDaysClient,notify=on_initWeekDaysClient)
	
	on_detectedClients=Signal()
	detectedClients=Property(str,_getDetectedClients,_setDetectedClients, notify=on_detectedClients)
	
#class Bridge

import Core
