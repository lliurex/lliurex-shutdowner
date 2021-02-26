#!/bin/bash
xgettext -kde -ki18nd:2 ../lliurex-shutdowner.install/usr/share/lliurex-shutdowner/rsrc/lliurex-shutdowner.qml -o lliurex-shutdowner/lliurex-shutdowner.pot
xgettext --join-existing -kde -ki18nd:2 ../lliurex-shutdowner.install/usr/share/lliurex-shutdowner/rsrc/Cron.qml -o lliurex-shutdowner/lliurex-shutdowner.pot
xgettext --join-existing -kde -ki18nd:2 ../lliurex-shutdowner.install/usr/share/lliurex-shutdowner/rsrc/ClientOptions.qml -o lliurex-shutdowner/lliurex-shutdowner.pot
xgettext --join-existing -kde -ki18nd:2 ../lliurex-shutdowner.install/usr/share/lliurex-shutdowner/rsrc/ServerOptions.qml -o lliurex-shutdowner/lliurex-shutdowner.pot
xgettext ../lliurex-shutdowner-common.install/usr/sbin/shutdown-lliurex-dialog.py -o lliurex-shutdowner-common/lliurex-shutdowner-common.pot

