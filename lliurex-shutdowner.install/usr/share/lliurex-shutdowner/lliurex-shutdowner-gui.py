from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon,QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

import sys
import Core
c=Core.Core.get_core()

app = QGuiApplication()
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

engine.quit.connect(QQuiApplication.quit)
app.setWindowIcon(QIcon("/usr/share/icons/hicolor/scalable/apps/lliurex-shutdowner.svg"));
ret=app.exec()
del engine
del app
sys.exit(ret)
