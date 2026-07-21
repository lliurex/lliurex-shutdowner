import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami


RowLayout{
    id: optionsGrid
    spacing: 10

    Rectangle{
        width:215
        Layout.fillHeight:true
        border.color: palette.mid

        ColumnLayout{
            id: menuGrid
            Layout.fillWidth:true
            Layout.fillHeight: true
            spacing: 0

            MenuOptionBtn { 
                id: clientOption 
                optionText: clientStackBridge.isStandAlone
                    ?i18nd("lliurex-shutdowner", "Desktop configuration")
                    :i18nd("lliurex-shutdowner", "Client configuration")
                optionIcon: "computer" 
                optionEnabled: true 
                onMenuOptionClicked: mainStackBridge.manageTransitions(0)
            }

            MenuOptionBtn {
                id:serverOption
                optionText:i18nd("lliurex-shutdowner","Server configuration")
                optionIcon:"network-workgroup"                  
                optionEnabled:clientStackBridge.isCronEnabled
                visible:!clientStackBridge.isStandAlone
                onMenuOptionClicked:mainStackBridge.manageTransitions(1)
            }

            MenuOptionBtn{
                id:settingsOption
                optionText:i18nd("lliurex-shutdowner","System settings")
                optionIcon:"configure"
                optionEnabled:serverStackBridge.serverShut?false:true
                visible:clientStackBridge.isClient
                onMenuOptionClicked:nainStackBridge.manageTransitions(2)

            }
            
            MenuOptionBtn {
                id:helpOption
                optionText:i18nd("lliurex-shutdowner","Help")
                optionIcon:"help-contents"
                optionEnabled:true
                visible:true
                onMenuOptionClicked:mainStackBridge.openHelp()
             }

            Item {
                    Layout.fillHeight:true

            }
        }
    }

    ColumnLayout{
        Layout.fillWidth:true
        Layout.fillHeight:true
        spacing:0

        StackView {
            id: optionsLayout
            Layout.fillHeight:true
            Layout.fillWidth:true

            property int currentIndex:mainStackBridge.currentOptionStack
            initialItem:clientView

            onCurrentIndexChanged:{

                switch (currentIndex){
                    case 0:
                        optionsLayout.replace(clientView)
                        break;
                    case 1:
                        optionsLayout.replace(serverView)
                        break;
                    case 2:
                        optionsLayout.replace(settingsView)
                        break;
                       
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
                id:clientView
                ClientOptions{
                    id:clientOptions
                }
            }

            Component{
                id:serverView
                ServerOptions{
                    id:serverOptions
                }
            }
            Component{
                id:settingsView
                SettingsOptions{
                    id:settingsOptions
                }
            }

                
        }

        Kirigami.InlineMessage {
            id: messageLabel
            visible:mainStackBridge.showMessage.show
            text:getMessageText()
            type: getMessageType(mainStackBridge.showMessage.type)
            Layout.fillWidth:true
            Layout.bottomMargin:15
            Layout.leftMargin:5
            Layout.rightMargin:15
            
        }

    }

    function getMessageText(){

        switch(mainStackBridge.showMessage.msgCode){
            case -10:
                return i18nd("lliurex-shutdowner","The client and server shutdown time are not compatible with each other")
            case -20:
                return i18nd("lliurex-shutdowner","The client and server shutdown days are not compatible with each other")
            case -30:
                return i18nd("lliurex-shutdowner","The client and server shutdown time and days are not compatible with each other")
            case -40:
                return i18nd("lliurex-shutdowner","Disabling automatic shutdown in this computer is only posible if automatic server shutdown is not enabled")
            case -50:
                return i18nd("lliurex-shutdowner","No days has been set to schedule the shutdown")
            default:
                return i18nd("lliurex-shutdowner","Changes saved successfully");
        }
        return ""
    }

    function getMessageType(type){

        switch (type) {
            case 0:
                return Kirigami.MessageType.Positive
            case 1:
                return Kirigami.MessageType.Error
            case 2:
                return Kirigami.MessageType.Warning
            case 3:
                return Kirigami.MessageType.Information
           default:
                return Kirigami.MessageType.Information
        }

    } 

}

