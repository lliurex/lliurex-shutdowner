#!/bin/bash

xgettext ../lliurex-shutdowner.install/usr/share/lliurex-shutdowner/LliurexShutdowner.py  ../lliurex-shutdowner.install/usr/share/lliurex-shutdowner/rsrc/lliurex-shutdowner.ui -o lliurex-shutdowner/lliurex-shutdowner.pot

xgettext ../lliurex-shutdowner-common.install/usr/share/lliurex-shutdowner/rsrc/shutdowner-lliurex-dialog.ui -L Python ../lliurex-shutdowner-common.install/usr/sbin/shutdown-lliurex-dialog -o lliurex-shutdowner-common/lliurex-shutdowner-common.pot

