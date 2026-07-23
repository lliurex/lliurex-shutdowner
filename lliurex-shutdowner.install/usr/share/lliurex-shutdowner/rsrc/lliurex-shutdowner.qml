import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import org.kde.plasma.core 2.0 as PlasmaCore

ApplicationWindow {
    id:mainWindow
    property bool closing: false
    property int margin: 1

    visible: true
    title: "LliureX Shutdowner"

    width: mainLayout.implicitWidth + 2 * margin
    height: mainLayout.implicitHeight + 2 * margin

    minimumWidth: 800 + 2 * margin
    minimumHeight: 580 + 2 * margin
    maximumWidth:800 + 2 * margin
    maximumHeight: 580 + 2 * margin

    Component.onCompleted: {
        x = Screen.width / 2 - minimumWidth / 2
        y = Screen.height / 2 - minimumHeight /2
    }

    
    onClosing: (close) => {
        close.accepted = closing;
        if (!closing) {
            mainStackBridge.closeShutdowner();
            closeTimer.start();
        }
    }

    Timer {
        id: closeTimer
        interval: 100
        repeat: true
        onTriggered: {
            if (mainStackBridge.closeGui) {
                stop();
                mainWindow.closing = true;
                mainWindow.close();
            }
        }
    }

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent

        Rectangle{
            color: "#23262f"
            Layout.fillWidth: true
            Layout.preferredHeight: 120

            Image{
                id:banner
                source: "lliurex-shutdowner.png"
                asynchronous:false
                anchors.centerIn: parent
                fillMode: Image.PreserveAspectFit
            }
        }

        StackView {
            id: mainView
            Layout.fillWidth:true
            Layout.fillHeight:true
            Layout.minimumHeight:clientStackBridge.isStandAlone?380:460

            property int currentIndex:mainStackBridge.currentStack
            initialItem:loadingView

            onCurrentIndexChanged:{
                switch (currentIndex){
                    case 0:
                        mainView.replace(loadingView)
                        break;
                    case 1:
                        mainView.replace(applicationOptionsView)
                }
            }

            replaceEnter: Transition {
                NumberAnimation {
                    property: "opacity"
                    from: 0
                    to: 1
                    duration: 60
                }
            }
            replaceExit: Transition {
                NumberAnimation { 
                    property: "opacity"
                    from: 1
                    to: 0
                    duration: 60
                }
            }

            Component{
                id:loadingView
                Loading{
                    id:loading
                }
            }
            Component{
                id:applicationOptionsView
                ApplicationOptions{
                    id:applicationOptions
                }
            }

        }

    }
}

