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

class Bridge(QObject):


	def __init__(self):

		QObject.__init__(self)

		self.n4d_man=N4dManager.N4dManager()
		self.initBridge()

	def printd(self,message):

		debug=True

		if debug:
			print('[Bridge_python] %s'%message)

	# def_printd

	def initBridge(self):

		self.cron_content="%s %s * * %s root %s >> /var/log/syslog\n"
		self.shutdown_bin="/usr/sbin/shutdown-lliurex"
		self.custom_shutdown_bin="/usr/sbin/shutdown-lliurex-server"
		self._initFinish=False
		self._running=False
		self._detectedClients=0
		self._showMessage=[False,""]
		self.previousError=""
		self._isStandAlone=self.n4d_man.is_standalone_mode()
		#self._isCronEnabled=self.n4d_man.is_cron_enabled()
		self._initClockClient=[0,0]
		self._initWeekDaysClient=[True,True,True,True,True]
		self._initClockServer=[0,0]
		self._initWeekDaysServer=[True,True,True,True,True]
		self._isCronEnabled=False

		self.cronSwitch=copy.deepcopy(self._isCronEnabled)
		
		#server_info=self.n4d_man.is_server_shut()
		#self._serverShut=server_info[0]
		self._serverShut=False
		self.serverShut=copy.deepcopy(self._serverShut)
		#self._customServerShut=server_info[1]
		self._customServerShut=False
		self.customServerShut=copy.deepcopy(self._customServerShut)


		self.clockClientValues=copy.deepcopy(self._initClockClient)
		self.weekClientValues=copy.deepcopy(self._initWeekDaysClient)
		self.clockServerValues=copy.deepcopy(self._initClockServer)
		self.weekServerValues=copy.deepcopy(self._initWeekDaysServer)
		
		#self.getShutInfo()

		if not self._isStandAlone:
			self.client_timer = QTimer(None)
			self.client_timer.timeout.connect(self.getClient)
			self.client_timer.start(2000)
		self.saveValues_timer = QTimer(None)
		self.saveValues_timer.timeout.connect(self.saveValues)
		self.saveValues_timer.start(5000)

	
	#def _init	
	
	'''def getShutInfo(self):

		t = threading.Thread(target=self._loadInfo)
		t.daemon=True
		t.start()
	#def getShutInfo'''

	@Slot('QVariantList')
	def validate(self,value):

		self.showMessage=[False,""]
		self.user=value[0]
		self.password=value[1]
		server=value[2]
		
		if server=='':
			server='server'
		
		self.n4d_man.set_server(server)

		if not self.running:
			self.running = True
			thread = threading.Thread(target=self._validate)
			thread.start()

	#def validate


	def _validate(self):

		LOGIN_FAILED=-40
		ret=self.n4d_man.validate_user(self.user,self.password)

		if ret:
			group_found=False
			for g in ["sudo","admins","teachers","admin"]:
				if g in self.n4d_man.user_groups:
					group_found=True
					break
					
			if group_found:
				self._loadInfo()
				#self._getState()
			else:
				self.showMessage=[True,LOGIN_FAILED]
				self.initFinish=False
				self.running=False
		else:
			self.showMessage=[True,LOGIN_FAILED]
			self.initFinish=False
			self.running=False

	#def _Validate	


	
	def _loadInfo(self):

		client_values=self.n4d_man.get_cron_values()	
		server_values=self.n4d_man.get_server_cron_values()
		self.printd('---loadInfo---')
		self.printd('client_values: %s'%client_values)
		self.printd('server_values: %s'%server_values)
		
		self.initClockClient=[client_values["hour"],client_values["minute"]]
		self.clockClientValues=copy.deepcopy(self._initClockClient)
		self.initWeekDaysClient=[client_values["weekdays"][0],client_values["weekdays"][1],client_values["weekdays"][2],client_values["weekdays"][3],client_values["weekdays"][4]]
		self.weekClientValues=copy.deepcopy(self._initWeekDaysClient)
		
		self.initClockServer=[server_values["hour"],server_values["minute"]]
		self.clockServerValues=copy.deepcopy(self._initClockServer)
		self.initWeekDaysServer=[server_values["weekdays"][0],server_values["weekdays"][1],server_values["weekdays"][2],server_values["weekdays"][3],server_values["weekdays"][4]]
		self.weekServerValues=copy.deepcopy(self._initWeekDaysServer)

		self.isCronEnabled=self.n4d_man.is_cron_enabled()
		self.cronSwitch=self.isCronEnabled
		server_info=self.n4d_man.is_server_shut()
		self.printd('server_info: %s'%server_info)
		self.serverShut=server_info[0]
		self.customServerShut=server_info[1]


		time.sleep(3)

		self.running=False

		self.initFinish=True

	#def _loadInfo	

	@Slot(str)
	def getClient(self):
		if self.initFinish:
			self.detectedClients=str(self.n4d_man.detected_clients)

	#def getClient

	def _getIsStandAlone(self):

		return self._isStandAlone

	#def _getIsStandAlone	

	def _getIsCronEnabled(self):

		return self._isCronEnabled

	#def _getIsCronEnabled	

	def _setIsCronEnabled(self,isCronEnabled):

		self._isCronEnabled=isCronEnabled
		self.on_isCronEnabled.emit()

	#def _getIsCronEnabled	

	def _getInitClockClient(self):

		return self._initClockClient

	#def _getinitClockClient	

	def _setInitClockClient(self,initClockClient):

		self._initClockClient=initClockClient
		self.on_initClockClient.emit()

	#def _setinitClockClient


	def _getInitWeekDaysClient(self):

		return self._initWeekDaysClient

	#def _getInitWeekDaysClient	



	def _setInitWeekDaysClient(self,initWeekDaysClient):

		self._initWeekDaysClient=initWeekDaysClient
		self.on_initWeekDaysClient.emit()

	#def _setInitWeekDaysClient	


	def _getInitClockServer(self):

		return self._initClockServer

	#def _getinitClockServer


	def _setInitClockServer(self,initClockServer):

		self._initClockServer=initClockServer
		self.on_initClockServer.emit()

	#def _setinitClockServer


	def _getInitWeekDaysServer(self):

		return self._initWeekDaysServer

	#def _getInitWeekDaysServer


	def _setInitWeekDaysServer(self,initWeekDaysServer):

		self._initWeekDaysServer=initWeekDaysServer
		self.on_initWeekDaysServer.emit()

	#def _setInitWeekDaysServer


	def _getInitFinish(self):

		return self._initFinish

	#def _getInitFinish	

	def _setInitFinish(self,initFinish):
		
		self._initFinish=initFinish
		self.on_initFinish.emit()	

	#def _setInitFinish

	def _getRunning(self):

		return self._running

	#def _getInitFinish	

	def _setRunning(self,running):
		
		self._running=running
		self.on_running.emit()	

	#def _setInitFinish

	def _getDetectedClients(self):

		return self._detectedClients

	#def _getDetectedClients	


	def _setDetectedClients(self,detectedClients):

		self._detectedClients=detectedClients
		self.on_detectedClients.emit()	

	#def _setDetectedClients

	def _getDetectedServerShut(self):

		return self._serverShut

	#def _getServerShut
	
	def _setDetectedServerShut(self,serverShut):

		self._serverShut=serverShut
		self.on_serverShut.emit()

	#def _setServerShut

	def _getDetectedCustomServerShut(self):

		return self._customServerShut

	#def getCustomServerShut
	
	def _setDetectedCustomServerShut(self,customServerShut):

		self._customServerShut=customServerShut
		self.on_customServerShut.emit()

	#def _setCustomServerShut

	def _getShowMessage(self):

		return self._showMessage

	#def _getShowMessage
	
	def _setShowMessage(self,showMessage):

		self._showMessage=showMessage
		self.on_showMessage.emit()

	#def _setShowMessage


	def check_changes(self):

		new_var=self.gather_values()
		if new_var!=self.n4d_man.shutdowner_var:
			self.printd('---check_changes---')
			self.printd('self.n4d_man.shutdowner_var is different, update it...')
			error=self.check_compat_client_server(new_var)
			if not error[0]:
				self.n4d_man.shutdowner_var=new_var
				self.previousError=""
				self.printd("[LliurexShutdowner] Updating value on close signal...")
				self.n4d_man.set_shutdowner_values()
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
						if (server_minute-new_var["cron_values"]["minute"])<2:
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
		self.printd('---gather_values_server---')
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

		self.printd('---gather_values---')
		getServerValues=False
		new_var=copy.deepcopy(self.n4d_man.shutdowner_var)

		new_var["cron_enabled"]=self.cronSwitch
		self.printd('new_var["cron_enabled"]: %s'%new_var["cron_enabled"])

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
				self.printd('new_var["cron_content"]: %s'%new_var["cron_content"])
				if not self._isStandAlone and self.serverShut:
					if self.customServerShut:
						new_var=self.gather_values_server(new_var)	
					else:
						self.printd('SERVER CUSTOM CRON: FALSE')
						new_var["server_cron"]["custom_shutdown"]=False

			else:
				new_var["cron_enabled"]=False
		

		return new_var

	#def gather_values
	
	def saveValues(self):
		if self.initFinish :
			new_var=self.gather_values()
			self.printd('---saveValues execute---')
			if new_var!=self.n4d_man.shutdowner_var:
				self.printd('Variables are different update it...')
				error=self.check_compat_client_server(new_var)
				if not error[0]:
					self.showMessage=[False,""]
					self.previousError=""
					self.n4d_man.shutdowner_var=new_var
					self.printd("[LliurexShutdowner] Updating shutdowner variable...")
					t=threading.Thread(target=self.n4d_man.set_shutdowner_values)
					t.daemon=True
					t.start()
				else:
					if self.previousError!=error[1]:
						self.showMessage=error
						self.previousError=error[1]
			else:
				self.showMessage=[False,""]	
				self.previousError=""
	
			
	#def saveValues

	
	@Slot(bool)
	def getCronSwitchValue(self,state):
		self.cronSwitch=state

	#getCronSwitchValue
	
	@Slot('QVariantList')
	def getClockClientValues(self,values):

		if values[0]=="H":
			self.clockClientValues[0]=values[1]
		
		else:
			self.clockClientValues[1]=values[1]

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


	#def getWeekServerValues

	@Slot('QVariantList')
	def getClockServerValues(self,values):

		if values[0]=="H":
			self.clockServerValues[0]=values[1]
		
		else:
			self.clockServerValues[1]=values[1]
								
	#def getClokClientValues
	
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
		self.n4d_man.shutdown_clients()
	
	#def shutdownClientsNow

	@Slot()
	def openHelp(self):
		lang=os.environ["LANG"]

		if 'valencia' in lang:
			self.help_cmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Lliurex+Shutdowner_V2.'
		else:
			self.help_cmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Lliurex-Shutdowner_V2'
		
		self.open_help_t=threading.Thread(target=self._open_help)
		self.open_help_t.daemon=True
		self.open_help_t.start()

	#def OpenHelp

	def _open_help(self):

		os.system(self.help_cmd)

	#def _open_help

	@Slot(bool,result=bool)


	def closeShutdowner(self,state):
		self.printd('---closeShutdowner---')
		self.printd(self.gather_values())
		if self.initFinish:
			acceptedClose=self.check_changes()
			if acceptedClose:
				self.printd('AcceptedClose....')
				if not self._isStandAlone:
					self.client_timer.stop()
				self.saveValues_timer.stop()
				return True
			else:
				return False
		else:
			return True

	#def closed




	isStandAlone=Property(bool,_getIsStandAlone,constant=True)
	#isCronEnabled=Property(bool,_getIsCronEnabled,constant=True)
	#initClockClient=Property('QVariantList',_getInitClockClient,constant=True)
	#initWeekDaysClient=Property('QVariantList',_getInitWeekDaysClient,constant=True)
	#initClockServer=Property('QVariantList',_getInitClockServer,constant=True)
	#initWeekDaysServer=Property('QVariantList',_getInitWeekDaysServer,constant=True)

	on_isCronEnabled=Signal()
	isCronEnabled=Property(bool,_getIsCronEnabled,_setIsCronEnabled, notify=on_isCronEnabled)

	on_initClockClient=Signal()
	initClockClient=Property('QVariantList',_getInitClockClient,_setInitClockClient, notify=on_initClockClient)

	on_initWeekDaysClient=Signal()
	initWeekDaysClient=Property('QVariantList',_getInitWeekDaysClient,_setInitWeekDaysClient, notify=on_initWeekDaysClient)

	on_initClockServer=Signal()
	initClockServer=Property('QVariantList',_getInitClockServer,_setInitClockServer, notify=on_initClockServer)

	on_initWeekDaysServer=Signal()
	initWeekDaysServer=Property('QVariantList',_getInitWeekDaysServer,_setInitWeekDaysServer, notify=on_initWeekDaysServer)


	on_initFinish=Signal()
	initFinish=Property(bool,_getInitFinish,_setInitFinish, notify=on_initFinish)

	on_running=Signal()
	running=Property(bool,_getRunning,_setRunning, notify=on_running)

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