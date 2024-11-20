import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami


ApplicationWindow {
    visible: true
    title: "LliureX Shutdowner"
    property int margin: 1
    width: mainLayout.implicitWidth + 2 * margin
    height: mainLayout.implicitHeight + 2 * margin
    minimumWidth: mainLayout.Layout.minimumWidth + 2 * margin
    minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
    maximumWidth: mainLayout.Layout.maximumWidth + 2 * margin
    maximumHeight: mainLayout.Layout.maximumHeight + 2 * margin
    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 0.5
    }

    onClosing:(close)=> {
        if (mainStackBridge.closeShutdowner(true)){
            close.accepted=true;
        }else{
            close.accepted=false;   
        }
    }

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: margin
        Layout.minimumWidth:795
        Layout.maximumWidth:795

        RowLayout {
            id: bannerBox
            Layout.alignment:Qt.AlignTop
            Layout.minimumHeight:120
            Layout.maximumHeight:120
            Image{
                id:banner
                source: "/usr/share/lliurex-shutdowner/rsrc/lliurex-shutdowner.png"
            }
        }

        StackView {
            id: mainWiew
            property int currentIndex:mainStackBridge.currentStack
            implicitWidth: 795
            Layout.alignment:Qt.AlignVCenter
            Layout.leftMargin:0
	    Layout.minimumHeight:clientStackBridge.isStandAlone? 430:480
	    Layout.maximumHeight:clientStackBridge.isStandAlone? 430:480

            initialItem:loadingView

            onCurrentIndexChanged:{
                switch(currentIndex){
                    case 0:
                        mainView.replace(loadingView)
                        break
                    case 1:
                        mainWiew.replace(applicationOptionView)
                        break
                }
            }
        }

        Component{
            id:loadingView
            Loading{
                id:loading
            }

        }

        Component{
            id:applicationOptionView
            ApplicationOptions{
                id:applicationOption
            }

        }
    }


}       
