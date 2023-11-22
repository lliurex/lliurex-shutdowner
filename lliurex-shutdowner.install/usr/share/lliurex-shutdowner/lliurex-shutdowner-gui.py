from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl
from PySide2.QtGui import QIcon
from PySide2.QtQml import QQmlApplicationEngine

import sys
import Core
c=Core.Core.get_core()

app = QApplication()
engine = QQmlApplicationEngine()
engine.clearComponentCache()
context=engine.rootContext()
mainStackBridge=c.mainStack
clientStackBridge=c.clientStack
serverStackBridge=c.serverStack
settingsStackBridge=c.settingsStack
context.setContextProperty("mainStackBridge", mainStackBridge)
context.setContextProperty("clientStackBridge", clientStackBridge)
context.setContextProperty("serverStackBridge", serverStackBridge)
context.setContextProperty("settingsStackBridge", settingsStackBridge)

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
