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
		self.customShutdownBin="/usr/sbin/shutdown-lliurex-server"
		self.loadError=False
		
	def loadConfig(self):

		serverValues=Bridge.n4dManager.getServerCronValues()

		if serverValues!=None:
			if len(serverValues)>0:
				serverInfo=Bridge.n4dManager.isServerShut()

				self._serverShut=serverInfo[0]
				if len(serverInfo)==1:
					self.loadError=True
				else:
					self.serverShut=copy.deepcopy(self._serverShut)
					self._customServerShut=serverInfo[1]
					self.customServerShut=copy.deepcopy(self._customServerShut)
					self._initClockServer=[serverValues["hour"],serverValues["minute"]]
					self.clockServerValues=copy.deepcopy(self._initClockServer)
					self._initWeekDaysServer=[serverValues["weekdays"][0],serverValues["weekdays"][1],serverValues["weekdays"][2],serverValues["weekdays"][3],serverValues["weekdays"][4]]
					self.weekServerValues=copy.deepcopy(self._initWeekDaysServer)
			else:
				self.loadError=True
		else:
			self.loadError=True

	#def load Config

	def _getInitClockServer(self):

		return self._initClockServer

	#def _getInitClockServer

	def _setInitClockServer(self,initClockServer):

		if self._initClockServer!=initClockServer:
			self._initClockServer=initClockServer
			self.on_initClockServer.emit()

	#def _setInitClockServer	

	def _getInitWeekDaysServer(self):

		return self._initWeekDaysServer

	#def _getInitWeekDaysServer

	def _setInitWeekDaysServer(self,initWeekDaysServer):

		if self._initWeekDaysServer!=initWeekDaysServer:
			self._initWeekDaysServer=initWeekDaysServer
			self.on_initWeekDaysServer.emit()

	#def _setInitWeekDaysServer

	def _getDetectedServerShut(self):

		return self._serverShut

	#def _getServerShut
	
	def _setDetectedServerShut(self,serverShut):

		if self._serverShut!=serverShut:
			self._serverShut=serverShut
			self.on_serverShut.emit()

	#def _setServerShut

	def _getDetectedCustomServerShut(self):

		return self._customServerShut

	#def getCustomServerShut
	
	def _setDetectedCustomServerShut(self,customServerShut):

		if self._customServerShut!=customServerShut:
			self._customServerShut=customServerShut
			self.on_customServerShut.emit()

	#def _setCustomServerShut

	def checkCompatClientServer(self,newVar):

		INCOMPATIBILITY_HOUR_ERROR=-10
		INCOMPATIBILITY_WEEK_ERROR=-20
		INCOMPATIBILITY_HOUR_AND_WEEK_ERROR=-30

		errorClock=False
		errorWeek=False
		if not self.core.clientStack._isStandAlone:
			if newVar["cron_enabled"]:
				if newVar["cron_values"]["server_shutdown"] and newVar["server_cron"]["custom_shutdown"]:
					serverHour=newVar["server_cron"]["cron_server_values"]["hour"]
					serverMinute=newVar["server_cron"]["cron_server_values"]["minute"]
					
					if serverHour<newVar["cron_values"]["hour"]:
						errorClock=True
					elif serverHour==newVar["cron_values"]["hour"]:
						if serverMinute<newVar["cron_values"]["minute"]:
							errorClock=True
					
					serverWeekdays=newVar["server_cron"]["cron_server_values"]["weekdays"]

					if serverWeekdays!=newVar["cron_values"]["weekdays"]:
						for item in range(0,len(serverWeekdays)):
							if serverWeekdays[item]:
								if not newVar["cron_values"]["weekdays"][item]:
									errorWeek=True
									break
		
		if errorClock and errorWeek:
			return [True,INCOMPATIBILITY_HOUR_AND_WEEK_ERROR]
		elif errorClock:
			return [True,INCOMPATIBILITY_HOUR_ERROR]
		elif errorWeek:
			return [True,INCOMPATIBILITY_WEEK_ERROR]
		else:
			return [False,""]
	
	#def check_compat_client_server

	def gatherValuesServer(self,newVar):

		dayConfigured=False

		for item in self.weekServerValues:
			if item:
				day_configured=True
				break
		if day_configured:
			newVar["server_cron"]["cron_server_values"]["hour"]=self.clockServerValues[0]
			newVar["server_cron"]["cron_server_values"]["minute"]=self.clockServerValues[1]
			newVar["server_cron"]["cron_server_values"]["weekdays"][0]=self.weekServerValues[0]
			newVar["server_cron"]["cron_server_values"]["weekdays"][1]=self.weekServerValues[1]
			newVar["server_cron"]["cron_server_values"]["weekdays"][2]=self.weekServerValues[2]
			newVar["server_cron"]["cron_server_values"]["weekdays"][3]=self.weekServerValues[3]
			newVar["server_cron"]["cron_server_values"]["weekdays"][4]=self.weekServerValues[4]
			newVar["server_cron"]["custom_shutdown"]=self.customServerShut

			days=""
			count=1
			for day in newVar["server_cron"]["cron_server_values"]["weekdays"]:
				if day:
					days+="%s,"%count
					count+=1
			days=days.rstrip(",")
			newVar["server_cron"]["cron_server_content"]=self.core.mainStack.cronContent%(self.clockServerValues[1],self.clockServerValues[0],days,self.customShutdownBin)

		return newVar
	
	#def gatherValuesServer		

	@Slot('QVariantList')
	def getClockServerValues(self,values):

		if values[0]=="H":
			self.clockServerValues[0]=values[1]
		
		else:
			self.clockServerValues[1]=values[1]

		self.initClockServer=self.clockServerValues
								
	#def getClockServerValues
	
	@Slot('QVariantList')
	def getWeekServerValues(self,values):

		if values[0]=="MO":
			self.weekServerValues[0]=values[1]
		elif values[0]=="TU":
			self.weekServerValues[1]=values[1]
		elif values[0]=="WE":
			self.weekServerValues[2]=values[1]	
		elif values[0]=="TH":
			self.weekServerValues[3]=values[1]
		elif values[0]=="FR":
			self.weekServerValues[4]=values[1]

		self.initWeekDaysServer=self.weekServerValues	

	#def getWeekServerValues

	@Slot(bool)
	def getServerShut(self,value):
		
		self.serverShut=value

	#def getServerShut

	@Slot(bool)
	def getCustomServerShut(self,value):
		
		self.customServerShut=value

	#def getCustomServerShut
	
	on_initClockServer=Signal()
	initClockServer=Property('QVariantList',_getInitClockServer,_setInitClockServer,notify=on_initClockServer)
	
	on_initWeekDaysServer=Signal()
	initWeekDaysServer=Property('QVariantList',_getInitWeekDaysServer,_setInitWeekDaysServer,notify=on_initWeekDaysServer)

	on_serverShut=Signal()
	serverShut=Property(bool,_getDetectedServerShut,_setDetectedServerShut,notify=on_serverShut)
	
	on_customServerShut=Signal()
	customServerShut=Property(bool,_getDetectedCustomServerShut,_setDetectedCustomServerShut, notify=on_customServerShut)
	
#class Bridge

import Core
