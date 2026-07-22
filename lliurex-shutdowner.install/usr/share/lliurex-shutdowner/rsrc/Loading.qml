import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami


Rectangle{
    id:loadRoot
    visible: true

    color:"transparent"

    ColumnLayout {
        id: mainLoaderLayout
        anchors.centerIn: parent
        width: parent.width * 0.9
        spacing: 15

        ColumnLayout{
            Layout.alignment: Qt.AlignHCenter
            spacing:10

            Image{
                id:spinnerImage
                source: "loading.png"
                visible:!mainStackBridge.isThereAnError.show
                Layout.preferredWidth: 24
                Layout.preferredHeight: 24
                Layout.alignment: Qt.AlignHCenter
                fillMode: Image.PreserveAspectFit
                smooth:false
                antialiasing:false

                rotation:0
            }
            
            Timer{
                id:rotationTimer
                running:(spinnerImage!==null && loadRoot!==null) && loadRoot.visible
                repeat:true
                interval:100

                onTriggered:{

                    if (spinnerImage && typeof spinnerImage.rotation!="undefined"){
                        var nextRotation= spinnerImage.rotation-30
                        if (nextRotation<0){
                            nextRotation=330
                        }
                        spinnerImage.rotation=nextRotation
                     }else{
                        stop()
                     }   

                }
            }

            Kirigami.InlineMessage{
                id:errorLabel
                visible:mainStackBridge.isThereAnError.show
                text:getMsgError()
                type:Kirigami.MessageType.Error
                Layout.fillWidth:true
            }

            Text {
                id: loadText
                text:i18nd("lliurex-access-control", "Loading. Wait a moment...")
                visible:!mainStackBridge.isThereAnError.show
                font.pointSize: 10
                color: palette.windowText
                Layout.alignment: Qt.AlignHCenter
            }

        }

    }

    function getMsgError(){

         switch(mainStackBridge.isThereAnError.msgCode){
            case -50:
                return i18nd("lliurex-shutdowner","Unable to connect with localhost")
            case -60:
                return i18nd("lliurex-shutdowner","An error ocurred when loading data. Restart your computer and try again")
            default:
                return ""
         }

    }
}
