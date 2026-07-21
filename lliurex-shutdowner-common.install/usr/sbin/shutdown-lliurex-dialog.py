#! /usr/bin/python3
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl, QObject, Slot, Signal, Property,QTimer
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QIcon

import os
import sys
import subprocess
import gettext
import xmlrpc.client as n4dclient
import ssl
gettext.textdomain("lliurex-shutdowner-common")
_=gettext.gettext


class Bridge(QObject):

	timeRemainingChanged=Signal()

	def __init__(self,wait_time):

		QObject.__init__(self)

		self.adiClient="/usr/bin/natfree-tie"
		self.adiServer="/usr/bin/natfree-adi"
		self.indicatorColor="#3daee9"
		self.countdown=int(wait_time)*60
		self.currentCounter=0
		self.blockDestroy=True
		self.versionReference=["adi","desktop"]
		self.countdownTimer = QTimer(None)
		self.countdownTimer.timeout.connect(self.updateCountDown)

		if wait_time=="2":
			self._timeRemaining={"time":"02:00","color":self.indicatorColor}
		else:
			self._timeRemaining={"time":"01:00","color":self.indicatorColor}

		self.initValues()

	#def __init__

	@Property(dict,notify=timeRemainingChanged)
	def timeRemaining(self):

		return self._timeRemaining

	#def timeRemaining	

	@timeRemaining.setter
	def timeRemaining(self,timeRemaining):

		self._timeRemaining=timeRemaining
		self.timeRemainingChanged.emit()	

	#def timeRemaining

	@Property(dict,constant=True)
	def translateMsg(self):

		return self._translateMsg

	#def translateMsg

	@Property(bool,constant=True)
	def visibleCancelBtn(self):

		return self._visibleCancelBtn

	#def visibleCancelBtn	
	
	def initValues(self):
		
		visibleBtn=self._showCancelBtn()

		if visibleBtn:
			try:
				context=ssl._create_unverified_context()
				self.client=n4dclient.ServerProxy('https://localhost:9779',context=context,allow_none=True)
			except:
				pass

		warningMsg=_("System will shutdown in a few seconds. Please, save your files")
		cancelBtnMsg=_("Cancel shutdown")

		self._translateMsg={"msg":warningMsg,"btnMsg":cancelBtnMsg}
		self._visibleCancelBtn=visibleBtn
		self.countdownTimer.start(1000)
	
	#def init_values

	def _showCancelBtn(self):

		visibleBtn=False
		
		if os.path.exists(self.adiServer):
			visibleBtn=True
		else:
			if os.path.exists(self.adiClient):
				if self._checkConnectionWithADI():
					visibleBtn=False
				else:
					visibleBtn=True
			else:
				visibleBtn=True

		return visibleBtn	
	
	#def _showCancelBtn
	
	def _checkConnectionWithADI(self):

		try:
			context=ssl._create_unverified_context()
			client=n4dclient.ServerProxy('https://server:9779',context=context,allow_none=True)
			test=client.is_cron_enabled('','ShutdownerManager')
			return True
		except Exception as e:
				return False

	#def _checkConnectionWithServer

	def updateCountDown(self):

		self.currentCounter+=1
		count=self.countdown-self.currentCounter

		if count>=0:
			mins,secs=divmod(count,60)

			if count<=10:
				self.indicatorColor="#ff0000"

			self.timeRemaining={"time":f"{mins:02d}:{secs:02d}","color":self.indicatorColor}

			self.blockDestroy=False
		else:
			self.countdownTimer.stop()
			self.blockDestroy=True

		'''
		if self.countdown-self.currentCounter >=0:
			count=self.countdown-self.currentCounter
			
			if count==120:
				self.timeRemaining=["02:00",self.indicatorColor]
			elif count>69:
				self.timeRemaining=["01:"+str(count-60),self.indicatorColor]
			elif count>60:
				self.timeRemaining=["01:0"+str(count-60),self.indicatorColor]
			elif count==60:
				self.timeRemaining=["01:00",self.indicatorColor]
			elif count<10:
				self.indicatorColor="#ff0000"
				self.timeRemaining=["00:0"+str(count),self.indicatorColor]
			else:
				if count==10:
					self.indicatorColor="#ff0000"
				self.timeRemaining=["00:"+str(count),self.indicatorColor]
			self.blockDestroy=False		
		else:
			self.countdownTimer.stop()
			self.blockDestroy=True
		'''

		
	#def updateCountDown

	@Slot()
	def cancelClicked(self):
		self.countdownTimer.stop()
		try:
			ret=self.client.cancel_shutdown('','ShutdownerManager')
		except:
			pass
		app.quit()

	#def cancelClicked

	@Slot(bool,result=bool)
	def closed(self,state):
		
		return self.blockDestroy	

	#def closed	
	
if __name__=="__main__":

	app = QApplication()
	app.setDesktopFileName("lliurex-shutdowner")
	engine = QQmlApplicationEngine()
	engine.clearComponentCache()
	context=engine.rootContext()
	bridge=Bridge(sys.argv[1])
	context.setContextProperty("bridge", bridge)

	url = QUrl("/usr/share/lliurex-shutdowner/rsrc/shutdowner-lliurex-dialog.qml")


	engine.load(url)
	if not engine.rootObjects():
		sys.exit(-1)

	engine.quit.connect(app.quit)
	ret=app.exec()
	del engine
	del app
	sys.exit(ret)
