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

	def __init__(self,wait_time):

		QObject.__init__(self)

		self.indicatorColor="#3daee9"
		self.countdown=int(wait_time)*60
		self.current_counter=0
		self.block_destroy=True
		self.countdown_timer = QTimer(None)
		self.countdown_timer.timeout.connect(self.updateCountDown)

		if wait_time=="2":
			self._timeRemaining=["02:00",self.indicatorColor]
		else:
			self._timeRemaining=["01:00",self.indicatorColor]

		self.initValues()

	#def __init__
	
	def initValues(self):
		
		visibleBtn=self._showCancelBtn()
		warning_msg=_("System will shutdown in a few seconds. Please, save your files")
		cancelBtn_msg=_("Cancel shutdown")

		self._translateMsg=[warning_msg,cancelBtn_msg]
		self._visibleCancelBtn=visibleBtn
		self.countdown_timer.start(1000)
	
	#def init_values

	def _showCancelBtn(self):

		visibleBtn=False
		isDesktop=True
		cmd='lliurex-version -v'
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		result=p.communicate()[0]

		if type(result) is bytes:
			result=result.decode()
		flavours = [ x.strip() for x in result.split(',') ]

		for item in flavours:
			if 'adi' in item:
				visibleBtn=True
				isDesktop=False
				break
				
		if isDesktop:
			if self._checkConnectionWithADI():
				visibleBtn=False
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
			context=ssl._create_unverified_context()
			self.client=n4dclient.ServerProxy('https://localhost:9779',context=context,allow_none=True)
			return False

	#def _checkConnectionWithADI


	def updateCountDown(self):

		self.current_counter+=1

		if self.countdown-self.current_counter >=0:
			count=self.countdown-self.current_counter
			
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
			self.block_destroy=False		
		else:
			self.countdown_timer.stop()
			self.block_destroy=True

		
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
		self.countdown_timer.stop()
		try:
			ret=self.client.cancel_shutdown('','ShutdownerManager')
		except:
			pass
		app.quit()

	#def cancelClicked

	@Slot(bool,result=bool)
	def closed(self,state):
		
		return self.block_destroy	

	#def closed	
		
	on_timeRemaining=Signal()
	timeRemaining=Property('QVariantList',_getTimeRemaining,_setTimeRemaining, notify=on_timeRemaining)
	translateMsg=Property('QVariantList',_getTranslateMsg,constant=True)
	visibleCancelBtn=Property(bool,_getVisibleCancelBtn,constant=True)

	
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

	engine.quit.connect(QApplication.quit)
	app.setWindowIcon(QIcon("/usr/share/icons/hicolor/scalable/apps/lliurex-shutdowner.svg"));
	ret=app.exec()
	del engine
	del app
	sys.exit(ret)
