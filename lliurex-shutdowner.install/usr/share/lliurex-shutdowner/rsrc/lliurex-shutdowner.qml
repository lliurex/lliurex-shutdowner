import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.15
import QtQuick.Window 2.2
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.6 as Kirigami


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

    onClosing: {
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
        Layout.minimumWidth:800 
        Layout.maximumWidth:800
        Layout.minimumHeight:clientStackBridge.isStandAlone? 500:580
        Layout.maximumHeight:clientStackBridge.isStandAlone? 500:580

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
            implicitWidth: 800
            Layout.alignment:Qt.AlignVCenter
            Layout.leftMargin:0
            Layout.fillHeight: true

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
