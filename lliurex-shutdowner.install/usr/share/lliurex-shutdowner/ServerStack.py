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

	INCOMPATIBILITY_HOUR_ERROR=-10
	INCOMPATIBILITY_WEEK_ERROR=-20
	INCOMPATIBILITY_HOUR_AND_WEEK_ERROR=-30

	initClockServerChanged=Signal()
	initWeekDaysServerChanged=Signal()
	serverShutChanged=Signal()
	customServerShutChanged=Signal()

	def __init__(self,ticket=None,passwd=None):

		super().__init__()
		self.core=Core.Core.get_core()
		self.n4dManager=self.core.n4dManager
		self.customShutdownBin="/usr/sbin/shutdown-lliurex-server"
		self.loadError=False

	#def__init__

	@Property(dict,notify=initClockServerChanged)
	def initClockServer(self):

		return self._initClockServer

	#def initClockServer

	@initClockServer.setter
	def initClockServer(self,initClockServer):

		if self._initClockServer!=initClockServer:
			self._initClockServer=initClockServer
			self.initClockServerChanged.emit()

	#def initClockServer

	@Property(dict,notify=initWeekDaysServerChanged)
	def initWeekDaysServer(self):

		return self._initWeekDaysServer

	#def initWeekDaysServer

	@initWeekDaysServer.setter
	def initWeekDaysServer(self,initWeekDaysServer):

		if self._initWeekDaysServer!=initWeekDaysServer:
			self._initWeekDaysServer=initWeekDaysServer
			self.initWeekDaysServerChanged.emit()

	#def initWeekDaysServer
	
	@Property(bool,notify=serverShutChanged)
	def serverShut(self):

		return self._serverShut

	#def serverShut
	
	@serverShut.setter
	def serverShut(self,serverShut):

		if self._serverShut!=serverShut:
			self._serverShut=serverShut
			self.serverShutChanged.emit()

	#def serverShut

	@Property(bool,notify=customServerShutChanged)
	def customServerShut(self):

		return self._customServerShut

	#def customServerShut
	
	@customServerShut.setter
	def customServerShut(self,customServerShut):

		if self._customServerShut!=customServerShut:
			self._customServerShut=customServerShut
			self.customServerShutChanged.emit()

	#def customServerShut
	
	def loadConfig(self):

		serverValues=self.n4dManager.getServerCronValues()

		if serverValues is None:
			self.loadError=True
			return

		if not serverValues:
			self.loadError=True
			return
		
		serverInfo=self.n4dManager.isServerShut()
		self._serverShut=serverInfo.get("status")
		
		if not serverInfo.get("data"):
			self.loadError=True

		self.serverShut=copy.deepcopy(self._serverShut)
		self._customServerShut=serverInfo.get("data")
		self.customServerShut=copy.deepcopy(self._customServerShut)
		self._initClockServer={"hour":serverValues.get("hour"),"minute":serverValues.get("minute")}
		self.clockServerValues=copy.deepcopy(self._initClockServer)
		self._initWeekDaysServer = {str(i): valor for i, valor in enumerate(serverValues.get("weekdays", []))}
		self.weekServerValues=copy.deepcopy(self._initWeekDaysServer)
	
	#def load Config

	def checkCompatClientServer(self,newVar):

		errorWeek=False
		errorClock=False

		if self.core.clientStack._isStandAlone or not newVar.get("cron_enabled"):
			return {"error":False,"code":""}

		cronValues=newVar.get("cron_values",{})
		serverCron=newVar.get("server_cron",{})

		if cronValues.get("server_shutdown") and serverCron.get("custom_shutdown"):

			serverValues=serverCron.get("cron_server_values",{})

			serverTime=(serverValues.get("hour",0)*60+serverValues.get("minute",0))
			clientTime=(cronValues.get("hour",0)*60+cronValues.get("minute",0))
			errorClock=serverTime<clientTime
			serverWeekdays=serverValues.get("weekdays",[])
			clientWeekdays=cronValues.get("weekdays",[])
			errorWeek=any(
				serverDay and not clientDay
				for serverDay,clientDay in zip(serverWeekdays,clientWeekdays)
			)
		
		if errorClock and errorWeek:
			return {"error":True,"code":Bridge.INCOMPATIBILITY_HOUR_AND_WEEK_ERROR}
		elif errorClock:
			return {"error":True,"code":Bridge.INCOMPATIBILITY_HOUR_ERROR}
		elif errorWeek:
			return {"error":True,"code":Bridge.INCOMPATIBILITY_WEEK_ERROR}

		return {"error":False,"code":""}
	
	#def check_compat_client_server

	def gatherValuesServer(self,newVar):

		if not any(self.weekServerValues.values()):
			return newVar

		newVar["server_cron"]["cron_server_values"]["hour"]=self.clockServerValues.get("hour")
		newVar["server_cron"]["cron_server_values"]["minute"]=self.clockServerValues.get("minute")
		for i in range(5):
			key=str(i)
			newVar["server_cron"]["cron_server_values"]["weekdays"][i]=self.weekServerValues.get(key,False)

		newVar["server_cron"]["custom_shutdown"]=self.customServerShut

		selectedDays=[
			str(int(k)+1)
			for k, v in self.weekServerValues.items()
			if v and k.isdigit() and int(k) <5
		]

		days=",".join(selectedDays)
		minute=self.clockServerValues.get("minute")
		hour=self.clockServerValues.get("hour")
		newVar["server_cron"]["cron_server_content"]=self.core.mainStack.cronContent%(minute,hour,days,self.customShutdownBin)

		return newVar
	
	#def gatherValuesServer		

	@Slot(dict)
	def getClockServerValues(self,data):

		changes={key:value for key,value in data.items() if self.initClockServer[key]!=value}

		if changes:
			self.initClockServer={**self.initClockServer,**changes}

		self.clockServerValues=self.initClockServer
								
	#def getClockServerValues
	
	@Slot(dict)
	def getWeekServerValues(self,data):

		changes={key:value for key,value in data.items() if self.initWeekDaysServer[key]!=value}

		if changes:
			self.initWeekDaysServer={**self.initWeekDaysServer,**changes}
		
		self.weekServerValues=self.initWeekDaysServer

	#def getWeekServerValues

	@Slot(bool)
	def getServerShut(self,value):
		
		self.serverShut=value

	#def getServerShut

	@Slot(bool)
	def getCustomServerShut(self,value):
		
		self.customServerShut=value

	#def getCustomServerShut
			
#class Bridge

import Core
