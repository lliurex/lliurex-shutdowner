from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer
from PySide2.QtGui import QCloseEvent
import os 
import N4dManager
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
		self.manager=Bridge.n4d_man.load_info()

	#def run

class Bridge(QObject):

	n4d_man=N4dManager.N4dManager()

	def __init__(self,ticket=None,passwd=None):

		QObject.__init__(self)
		self.initBridge(ticket,passwd)

	def initBridge(self,ticket,passwd):

		self.cron_content="%s %s * * %s root %s >> /var/log/syslog\n"
		self.shutdown_bin="/usr/sbin/shutdown-lliurex"
		self.custom_shutdown_bin="/usr/sbin/shutdown-lliurex-server"
		self._currentStack=0
		self._currentOptionStack=0
		self._detectedClients="0"
		self._showMessage=[False,""]
		self.previousError=""
		self._isStandAlone,self._isClient=Bridge.n4d_man.is_standalone_mode()

		Bridge.n4d_man.set_server(ticket,passwd)
		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadInfo)

	
	#def _init	
	
	def getShutInfo(self):

		self._currentStack=0
		t = threading.Thread(target=self._loadInfo)
		t.daemon=True
		t.start()
	
	#def getShutInfo		
	
	def _loadInfo(self):

		client_values=Bridge.n4d_man.get_cron_values()	
		server_values=Bridge.n4d_man.get_server_cron_values()
		server_info=Bridge.n4d_man.is_server_shut()

		self._isCronEnabled=Bridge.n4d_man.is_cron_enabled()
		self.cronSwitch=copy.deepcopy(self._isCronEnabled)
	
		self._serverShut=server_info[0]
		self.serverShut=copy.deepcopy(self._serverShut)
		self._customServerShut=server_info[1]
		self.customServerShut=copy.deepcopy(self._customServerShut)

		self._initClockClient=[client_values["hour"],client_values["minute"]]
		self.clockClientValues=copy.deepcopy(self._initClockClient)
		self._initWeekDaysClient=[client_values["weekdays"][0],client_values["weekdays"][1],client_values["weekdays"][2],client_values["weekdays"][3],client_values["weekdays"][4]]
		self.weekClientValues=copy.deepcopy(self._initWeekDaysClient)
		
		self._initClockServer=[server_values["hour"],server_values["minute"]]
		self.clockServerValues=copy.deepcopy(self._initClockServer)
		self._initWeekDaysServer=[server_values["weekdays"][0],server_values["weekdays"][1],server_values["weekdays"][2],server_values["weekdays"][3],server_values["weekdays"][4]]
		self.weekServerValues=copy.deepcopy(self._initWeekDaysServer)

		if not self._isStandAlone:
			self.client_timer = QTimer(None)
			self.client_timer.timeout.connect(self.getClient)
			self.client_timer.start(2000)
		self.saveValues_timer = QTimer(None)
		self.saveValues_timer.timeout.connect(self.saveValues)
		self.saveValues_timer.start(5000)
		self.countToShowError=0
		self.waitTimeError=20
		self.currentStack=1

	#def _loadInfo	

	def getClient(self):

		self.detectedClients=str(Bridge.n4d_man.detected_clients)

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

	def _getDetectedClients(self):

		return self._detectedClients

	#def _getDetectedClients	


	def _setDetectedClients(self,detectedClients):

		if self._detectedClients!=detectedClients:
			self._detectedClients=detectedClients
			self.on_detectedClients.emit()	

	#def _setDetectedClients

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

	def _getShowMessage(self):

		return self._showMessage

	#def _getShowMessage
	
	def _setShowMessage(self,showMessage):

		if self._showMessage!=showMessage:
			self._showMessage=showMessage
			self.on_showMessage.emit()

	#def _setShowMessage


	def check_changes(self):

		new_var=self.gather_values()
		if new_var!=Bridge.n4d_man.shutdowner_var:
			error=self.check_compat_client_server(new_var)
			if not error[0]:
				self.countToShowError=0
				Bridge.n4d_man.shutdowner_var=new_var
				self.previousError=""
				print("[LliurexShutdowner] Updating value on close signal...")
				Bridge.n4d_man.set_shutdowner_values()
				day_configured=False
				for item in self.weekClientValues:
					if item:
						day_configured=True
						break
				
				if self.cronSwitch and not day_configured:
					return True
			
				return True
			else:
				if self.previousError!=error[1]:
					self.showMessage=error
					self.previousError=error[1]
				return False
		
		return True
	
	#def check_changes	

	def check_compat_client_server(self,new_var):

		INCOMPATIBILITY_HOUR_ERROR=-10
		INCOMPATIBILITY_WEEK_ERROR=-20
		INCOMPATIBILITY_HOUR_AND_WEEK_ERROR=-30

		errorClock=False
		errorWeek=False
		if not self._isStandAlone:
			if new_var["cron_enabled"]:
				if new_var["cron_values"]["server_shutdown"] and new_var["server_cron"]["custom_shutdown"]:
					server_hour=new_var["server_cron"]["cron_server_values"]["hour"]
					server_minute=new_var["server_cron"]["cron_server_values"]["minute"]
					
					if server_hour<new_var["cron_values"]["hour"]:
						errorClock=True
					elif server_hour==new_var["cron_values"]["hour"]:
						if server_minute<new_var["cron_values"]["minute"]:
							errorClock=True
					
					server_weekdays=new_var["server_cron"]["cron_server_values"]["weekdays"]

					if server_weekdays!=new_var["cron_values"]["weekdays"]:
						for item in range(0,len(server_weekdays)):
							if server_weekdays[item]:
								if not new_var["cron_values"]["weekdays"][item]:
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
	


	def gather_values_server(self,new_var):

		day_configured=False

		for item in self.weekServerValues:
			if item:
				day_configured=True
				break
		if day_configured:
			new_var["server_cron"]["cron_server_values"]["hour"]=self.clockServerValues[0]
			new_var["server_cron"]["cron_server_values"]["minute"]=self.clockServerValues[1]
			new_var["server_cron"]["cron_server_values"]["weekdays"][0]=self.weekServerValues[0]
			new_var["server_cron"]["cron_server_values"]["weekdays"][1]=self.weekServerValues[1]
			new_var["server_cron"]["cron_server_values"]["weekdays"][2]=self.weekServerValues[2]
			new_var["server_cron"]["cron_server_values"]["weekdays"][3]=self.weekServerValues[3]
			new_var["server_cron"]["cron_server_values"]["weekdays"][4]=self.weekServerValues[4]
			new_var["server_cron"]["custom_shutdown"]=self.customServerShut

			days=""
			count=1
			for day in new_var["server_cron"]["cron_server_values"]["weekdays"]:
				if day:
					days+="%s,"%count
					count+=1
			days=days.rstrip(",")
			new_var["server_cron"]["cron_server_content"]=self.cron_content%(self.clockServerValues[1],self.clockServerValues[0],days,self.custom_shutdown_bin)

		return new_var
	
	#def gather_values_server		


	def gather_values(self):

		getServerValues=False
		new_var=copy.deepcopy(Bridge.n4d_man.shutdowner_var)
		new_var["cron_enabled"]=self.cronSwitch


		if self.cronSwitch:

			day_configured=False

			for item in self.weekClientValues:
				if item:
					day_configured=True
					break
			
			if day_configured:

				new_var["cron_values"]["weekdays"][0]=self.weekClientValues[0]
				new_var["cron_values"]["weekdays"][1]=self.weekClientValues[1]
				new_var["cron_values"]["weekdays"][2]=self.weekClientValues[2]
				new_var["cron_values"]["weekdays"][3]=self.weekClientValues[3]
				new_var["cron_values"]["weekdays"][4]=self.weekClientValues[4]
				new_var["cron_values"]["server_shutdown"]=self.serverShut
				new_var["cron_values"]["hour"]=self.clockClientValues[0]
				new_var["cron_values"]["minute"]=self.clockClientValues[1]

				days=""
				count=1
				for day in new_var["cron_values"]["weekdays"]:
					if day:
						days+="%s,"%count
					count+=1
				days=days.rstrip(",")
				new_var["cron_content"]=self.cron_content%(self.clockClientValues[1],self.clockClientValues[0],days,self.shutdown_bin)
				if not self._isStandAlone and self.serverShut:
					if self.customServerShut:
						new_var=self.gather_values_server(new_var)	
					else:
						new_var["server_cron"]["custom_shutdown"]=False

			else:
				new_var["cron_enabled"]=False
		

		return new_var

	#def gather_values
	
	def saveValues(self):

		new_var=self.gather_values()

		if new_var!=Bridge.n4d_man.shutdowner_var:
			error=self.check_compat_client_server(new_var)
			if not error[0]:
				self.showMessage=[False,""]
				self.previousError=""
				Bridge.n4d_man.shutdowner_var=new_var
				self.countToShowError=0
				print("[LliurexShutdowner] Updating shutdowner variable...")
				t=threading.Thread(target=Bridge.n4d_man.set_shutdowner_values)
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
			self.showMessage=[False,""]	
			self.previousError=""
			self.countToShowError=0
	
			
	#def saveValues

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

	#def getServerShut

	@Slot()
	def shutdownClientsNow(self):
		
		Bridge.n4d_man.shutdown_clients()
	
	#def shutdownClientsNow

	@Slot()
	def openHelp(self):
		lang=os.environ["LANG"]

		if 'valencia' in lang:
			self.help_cmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Lliurex+Shutdowner.'
		else:
			self.help_cmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Lliurex-Shutdowner'
		
		self.open_help_t=threading.Thread(target=self._open_help)
		self.open_help_t.daemon=True
		self.open_help_t.start()

	#def OpenHelp

	def _open_help(self):

		os.system(self.help_cmd)

	#def _open_help

	@Slot(int)
	def manageTransitions(self,stack):

		if self.currentOptionStack!=stack:
			self.currentOptionStack=stack

	#def manageTransitions

	@Slot(bool,result=bool)
	def closeShutdowner(self,state):
		
		acceptedClose=self.check_changes()
		if acceptedClose:
			if not self._isStandAlone:
				self.client_timer.stop()
			self.saveValues_timer.stop()
			return True
		else:
			return False

	#def closed	

	isStandAlone=Property(bool,_getIsStandAlone,constant=True)
	isClient=Property(bool,_getIsClient,constant=True)

	on_isCronEnabled=Signal()
	isCronEnabled=Property(bool,_getIsCronEnabled,_setIsCronEnabled,notify=on_isCronEnabled)
	
	on_initClockClient=Signal()
	initClockClient=Property('QVariantList',_getInitClockClient,_setInitClockClient,notify=on_initClockClient)
	
	on_initWeekDaysClient=Signal()
	initWeekDaysClient=Property('QVariantList',_getInitWeekDaysClient,_setInitWeekDaysClient,notify=on_initWeekDaysClient)
	
	on_initClockServer=Signal()
	initClockServer=Property('QVariantList',_getInitClockServer,_setInitClockServer,notify=on_initClockServer)
	
	on_initWeekDaysServer=Signal()
	initWeekDaysServer=Property('QVariantList',_getInitWeekDaysServer,_setInitWeekDaysServer,notify=on_initWeekDaysServer)

	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)

	on_currentOptionStack=Signal()
	currentOptionStack=Property(int,_getCurrentOptionStack,_setCurrentOptionStack, notify=on_currentOptionStack)

	on_detectedClients=Signal()
	detectedClients=Property(str,_getDetectedClients,_setDetectedClients, notify=on_detectedClients)
	
	on_serverShut=Signal()
	serverShut=Property(bool,_getDetectedServerShut,_setDetectedServerShut,notify=on_serverShut)
	
	on_customServerShut=Signal()
	customServerShut=Property(bool,_getDetectedCustomServerShut,_setDetectedCustomServerShut, notify=on_customServerShut)
	
	on_showMessage=Signal()
	showMessage=Property('QVariantList',_getShowMessage,_setShowMessage, notify=on_showMessage)


if __name__=="__main__":

	pass
