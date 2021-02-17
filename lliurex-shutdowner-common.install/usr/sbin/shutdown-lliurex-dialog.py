#! /usr/bin/python3
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl, QObject, Slot, Signal, Property,QTimer
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtGui import QIcon

import os
import sys
import subprocess
import gettext
gettext.textdomain("lliurex-shutdowner-common")
_=gettext.gettext


class Bridge(QObject):


	def __init__(self,wait_time):


		QObject.__init__(self)

		self.countdown=int(wait_time)*60
		self.current_counter=0
		self.block_destroy=True
		self.countdown_timer = QTimer(None)
		self.countdown_timer.timeout.connect(self.updateCountDown)
		self.initValues()

	#def __init__
	
	def initValues(self):
		
		visibleBtn=True
		server=os.system("lliurex-version -t server 2>/dev/null")
		server_lite=os.system("lliurex-version -t server-lite 2>/dev/null")

		if server==0 or server_lite==0:
			ret=0
		else:
			ret=1

		is_thin=os.system("lliurex-version -x thin")
		is_desktop=os.system("lliurex-version -x desktop")

		if ret!=0 or is_thin==0:
			if is_desktop!=0:
				visibleBtn=False

		warning_msg=_("System will shutdown in a few seconds. Please, save your files")
		cancelBtn_msg=_("Cancel shutdown")

		self._translateMsg=[warning_msg,cancelBtn_msg]
		self._visibleCancelBtn=True
		self.countdown_timer.start(1000)
	
	#def init_values


	def updateCountDown(self):

		if self.countdown-self.current_counter >=0:
			count=self.countdown-self.current_counter
			
			if count==120:
				self.timeRemaining.emit("02:00") 
			elif count>69:
				self.timeRemaining.emit("01:"+str(count-60))
			elif count>60:
				self.timeRemaining.emit("01:0"+str(count-60))
			elif count==60:
				self.timeRemaining.emit("01:00")
			elif count<10:
				self.timeRemaining.emit("00:0"+str(count))
			else:
				self.timeRemaining.emit("00:"+str(count))
	
			self.block_destroy=False		
		else:
			self.countdown_timer.stop()
			self.block_destroy=True

		self.current_counter+=1

		
	#def updateCountDown

	def _getTranslateMsg(self):

		return self._translateMsg

	#def _getVisibleCancelBtn	
	
	def _getVisibleCancelBtn(self):

		return self._visibleCancelBtn

	#def _getVisibleCancelBtn	


	@Slot()
	def cancelClicked(self):
		self.countdown_timer.stop()
		command="shutdown -c"
		os.system(command)
		app.quit()

	#def cancelClicked

	@Slot(bool,result=bool)
	def closed(self,state):
		
		return self.block_destroy	

	#def closed	
		
	timeRemaining=Signal(str,arguments=['timeRemaining'])
	translateMsg=Property('QVariantList',_getTranslateMsg,constant=True)
	visibleCancelBtn=Property(bool,_getVisibleCancelBtn,constant=True)

	
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
	sys.exit(app.exec_())
