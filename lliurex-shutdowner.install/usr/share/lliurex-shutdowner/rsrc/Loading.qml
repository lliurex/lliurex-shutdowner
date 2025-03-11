import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.16 as Kirigami


Rectangle{
    visible: true

    GridLayout{
        id: loadGrid
        rows: 3
        flow: GridLayout.TopToBottom
        anchors.centerIn:parent

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            visible:!mainStackBridge.isThereAreError

            Rectangle{
                color:"transparent"
                width:30
                height:30
                
                AnimatedImage{
                    source: "/usr/share/lliurex-shutdowner/rsrc/loading.gif"
                    transform: Scale {xScale:0.45;yScale:0.45}
                }
            }
        }

        RowLayout{
            Layout.fillWidth: true
            Layout.alignment:Qt.AlignHCenter
            visible:!mainStackBridge.isThereAreError

            Text{
                id:loadtext
                text:i18nd("lliurex-shutdowner", "Loading. Wait a moment...")
                font.family: "Quattrocento Sans Bold"
                font.pointSize: 10
                Layout.alignment:Qt.AlignHCenter
            }
        }

        Kirigami.InlineMessage{
            id:errorLabel
            visible:mainStackBridge.isThereAreError
            text:i18nd("lliurex-shutdowner","An error ocurred while loading data. Restart your computer and try again")
            type:Kirigami.MessageType.Error
            Layout.minimumWidth:750
            Layout.rightMargin:15
            Layout.leftMargin:15

        }
    }
}
