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

	def __init__(self,ticket=None):

		QObject.__init__(self)

		self.n4d_man=N4dManager.N4dManager(ticket)
		self.initBridge()

	def initBridge(self):

		self.cron_content="%s %s * * %s root %s >> /var/log/syslog\n"
		self.shutdown_bin="/usr/sbin/shutdown-lliurex"
		self._initFinish=False
		self._detectedClients="0"
		self._isStandAlone=self.n4d_man.is_standalone_mode()
		self._isCronEnabled=self.n4d_man.is_cron_enabled()
		self.cronSwitch=copy.deepcopy(self._isCronEnabled)
		self.getShutInfo()

		if not self._isStandAlone:
			self.client_timer = QTimer(None)
			self.client_timer.timeout.connect(self.getClient)
			self.client_timer.start(2000)
		self.saveValues_timer = QTimer(None)
		self.saveValues_timer.timeout.connect(self.saveValues)
		self.saveValues_timer.start(5000)

	
	#def _init	
	
	def getShutInfo(self):

		t = threading.Thread(target=self._loadInfo)
		t.daemon=True
		t.start()
	#def getShutInfo		
	
	def _loadInfo(self):

		values=self.n4d_man.get_cron_values()	

		self._initClock=[values["hour"],values["minute"]]
		self.clockValues=copy.deepcopy(self._initClock)
		self._initWeekDays=[values["weekdays"][0],values["weekdays"][1],values["weekdays"][2],values["weekdays"][3],values["weekdays"][4]]
		self.weekValues=copy.deepcopy(self._initWeekDays)
		self._initServerShut=values["server_shutdown"]
		self.serverShut=copy.deepcopy(self._initServerShut)
		time.sleep(3)
		self.initFinish=True

	#def _loadInfo	

	@Slot(str)
	def getClient(self):

		self.detectedClients=str(self.n4d_man.detected_clients)

	#def getClient

	def _getIsStandAlone(self):

		return self._isStandAlone

	#def _getIsStandAlone	

	def _getIsCronEnabled(self):

		return self._isCronEnabled

	#def _getIsCronEnabled	

	def _getInitClock(self):

		return self._initClock

	#def _getInitClock	

	def _getInitWeekDays(self):

		return self._initWeekDays

	#def _getInitHour	

	def _getInitServerShut(self):

		return self._initServerShut

	#def _getInitHour	

	def _getInitFinish(self):

		return self._initFinish

	#def _getInitHour	

	def _setInitFinish(self,initFinish):
		
		self._initFinish=initFinish
		self.on_initFinish.emit()	

	#def _setLoadState

	def _getDetectedClients(self):

		return self._detectedClients

	#def _getInitHour	


	def _setDetectedClients(self,detectedClients):

		self._detectedClients=detectedClients
		self.on_detectedClients.emit()	

		
	def check_changes(self):
		
		new_var=self.gather_values()
		if new_var!=self.n4d_man.shutdowner_var:
			self.n4d_man.shutdowner_var=new_var
			print("[LliurexShutdowner] Updating value on close signal...")
			self.n4d_man.set_shutdowner_values()

			day_configured=False
			for item in self.weekValues:
				if item:
					day_configured=True
					break
			
			if self.cronSwitch and not day_configured:
				return True
			
		return True

	def gather_values(self):

		new_var=copy.deepcopy(self.n4d_man.shutdowner_var)
		new_var["cron_enabled"]=self.cronSwitch


		if self.cronSwitch:

			day_configured=False

			for item in self.weekValues:
				if item:
					day_configured=True
					break
			
			if day_configured:
				new_var["cron_values"]["weekdays"][0]=self.weekValues[0]
				new_var["cron_values"]["weekdays"][1]=self.weekValues[1]
				new_var["cron_values"]["weekdays"][2]=self.weekValues[2]
				new_var["cron_values"]["weekdays"][3]=self.weekValues[3]
				new_var["cron_values"]["weekdays"][4]=self.weekValues[4]
				new_var["cron_values"]["server_shutdown"]=self.serverShut
				new_var["cron_values"]["hour"]=self.clockValues[0]
				new_var["cron_values"]["minute"]=self.clockValues[1]

				days=""
				count=1
				for day in new_var["cron_values"]["weekdays"]:
					if day:
						days+="%s,"%count
					count+=1
				days=days.rstrip(",")
				new_var["cron_content"]=self.cron_content%(self.clockValues[1],self.clockValues[0],days,self.shutdown_bin)
			
			else:
				new_var["cron_enabled"]=False
		

		return new_var

	#def gather_values
	
	def saveValues(self):

		new_var=self.gather_values()
		if new_var!=self.n4d_man.shutdowner_var:
			self.n4d_man.shutdowner_var=new_var
			print("[LliurexShutdowner] Updating shutdowner variable...")
			t=threading.Thread(target=self.n4d_man.set_shutdowner_values)
			t.daemon=True
			t.start()

	#def saveValues

	
	@Slot(bool)
	def getCronSwitchValue(self,state):
		self.cronSwitch=state

	#getCronSwitchValue
	
	@Slot('QVariantList')
	def getClokValues(self,values):

		if values[0]=="H":
			self.clockValues[0]=values[1]
		else:
			self.clockValues[1]=values[1]						

	#def getClokValues
	
	@Slot('QVariantList')
	def getWeekValues(self,values):

		if values[0]=="MO":
			self.weekValues[0]=values[1]
		elif values[0]=="TU":
			self.weekValues[1]=values[1]
		elif values[0]=="WE":
			self.weekValues[2]=values[1]	
		elif values[0]=="TH":
			self.weekValues[3]=values[1]
		elif values[0]=="FR":
			self.weekValues[4]=values[1]	


	#def getWeekValues

	@Slot(bool)
	def getServerShut(self,value):

		self.serverShut=value

	#def getServerShut

	@Slot()
	def shutdownClientsNow(self):
		self.n4d_man.shutdown_clients()
	
	#def shutdownClientsNow

	@Slot(bool,result=bool)
	def closed(self,state):
		
		aceptedClose=self.check_changes()

		if aceptedClose:
			if not self._isStandAlone:
				self.client_timer.stop()
			self.saveValues_timer.stop()
			return True
		else:
			return False

	#def closed	

	isStandAlone=Property(bool,_getIsStandAlone,constant=True)
	isCronEnabled=Property(bool,_getIsCronEnabled,constant=True)
	initClock=Property('QVariantList',_getInitClock,constant=True)
	initWeekDays=Property('QVariantList',_getInitWeekDays,constant=True)
	initServerShut=Property(bool,_getInitServerShut,constant=True)

	on_initFinish=Signal()
	initFinish=Property(bool,_getInitFinish,_setInitFinish, notify=on_initFinish)

	on_detectedClients=Signal()
	detectedClients=Property(str,_getDetectedClients,_setDetectedClients, notify=on_detectedClients)


if __name__=="__main__":

	pass