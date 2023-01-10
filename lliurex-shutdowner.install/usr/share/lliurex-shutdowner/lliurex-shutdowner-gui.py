from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl
from PySide2.QtGui import QIcon
from PySide2.QtQml import QQmlApplicationEngine

import sys
import LliurexShutdowner

app = QApplication()
engine = QQmlApplicationEngine()
engine.clearComponentCache()
context=engine.rootContext()
shutBridge=LliurexShutdowner.Bridge(sys.argv[1],sys.argv[2])
context.setContextProperty("shutBridge", shutBridge)

url = QUrl("/usr/share/lliurex-shutdowner/rsrc/lliurex-shutdowner.qml")


engine.load(url)
if not engine.rootObjects():
	sys.exit(-1)

engine.quit.connect(QApplication.quit)
app.setWindowIcon(QIcon("/usr/share/icons/hicolor/scalable/apps/lliurex-shutdowner.svg"));
ret=app.exec_()
del engine
del app
sys.exit(ret)
