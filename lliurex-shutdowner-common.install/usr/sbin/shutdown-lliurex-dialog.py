#! /usr/bin/python3
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl, QObject, Slot, Signal, Property,QTimer
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtGui import QIcon

import os
import sys
import subprocess
import gettext
import xmlrpc.client as n4dclient
import ssl
gettext.textdomain("lliurex-shutdowner-common")
_=gettext.gettext


class Bridge(QObject):

	def __init__(self,waitTime):

		QObject.__init__(self)

		self.adiClient="/usr/bin/natfree-tie"
		self.indicatorColor="#3daee9"
		self.countdown=int(waitTime)*60
		self.currentCounter=0
		self.blockDestroy=True
		self.countdownTimer = QTimer(None)
		self.countdownTimer.timeout.connect(self.updateCountDown)

		if waitTime=="2":
			self._timeRemaining=["02:00",self.indicatorColor]
		else:
			self._timeRemaining=["01:00",self.indicatorColor]

		self.initValues()

	#def __init__
	
	def initValues(self):
		
		visibleBtn=self._showCancelBtn()
		warningMsg=_("System will shutdown in a few seconds. Please, save your files")
		cancelBtnMsg=_("Cancel shutdown")

		self._translateMsg=[warningMsg,cancelBtnMsg]
		self._visibleCancelBtn=visibleBtn
		self.countdownTimer.start(1000)
	
	#def init_values

	def _showCancelBtn(self):

		visibleBtn=False
		isClient=False
		isDesktop=False
		cmd='lliurex-version -v'
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		result=p.communicate()[0]

		if type(result) is bytes:
			result=result.decode()
		flavours = [ x.strip() for x in result.split(',') ]

		for item in flavours:
			if 'server' in item:
				visibleBtn=True
				break
			elif 'client' in item:
				isClient=True
			elif 'desktop' in item:
				isDesktop=True
				visibleBtn=True
				if os.path.exists(self.adiClient):
					isClient=True
					
		if isClient:
			if isDesktop:
				if self._checkConnectionWithServer():
					visibleBtn=False
				else:
					visibleBtn=True
	
		return visibleBtn

	#def _showCancelBtn
	
	def _checkConnectionWithServer(self):

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

	#def updateCountDown

	def _getTranslateMsg(self):

		return self._translateMsg

	#def _getVisibleCancelBtn	
	
	def _getVisibleCancelBtn(self):

		return self._visibleCancelBtn

	#def _getVisibleCancelBtn	

	def _getTimeRemaining(self):

		return self._timeRemaining

	#def _getTimeRemaining	

	def _setTimeRemaining(self,timeRemaining):

		self._timeRemaining=timeRemaining
		self.on_timeRemaining.emit()	

	#def _setTimeRemaining

	@Slot()
	def cancelClicked(self):
		self.countdownTimer.stop()
		command="shutdown -c"
		os.system(command)
		app.quit()

	#def cancelClicked

	@Slot(bool,result=bool)
	def closed(self,state):
		
		return self.blockDestroy	

	#def closed	
		
	on_timeRemaining=Signal()
	timeRemaining=Property('QVariantList',_getTimeRemaining,_setTimeRemaining, notify=on_timeRemaining)
	translateMsg=Property('QVariantList',_getTranslateMsg,constant=True)
	visibleCancelBtn=Property(bool,_getVisibleCancelBtn,constant=True)

#class Bridge

if __name__=="__main__":

	app = QApplication()
	engine = QQmlApplicationEngine()
	engine.clearComponentCache()
	context=engine.rootContext()
	bridge=Bridge(sys.argv[1])
	context.setContextProperty("bridge", bridge)

	url = QUrl("/usr/share/lliurex-shutdowner/rsrc/shutdowner-lliurex-dialog.qml")

	engine.load(url)
	if not engine.rootObjects():
		sys.exit(-1)

	engine.quit.connect(QApplication.quit)
	app.setWindowIcon(QIcon("/usr/share/icons/hicolor/scalable/apps/lliurex-shutdowner.svg"));
	ret=app.exec_()
	del engine
	del app
	sys.exit(ret)
