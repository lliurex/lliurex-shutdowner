import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami


GridLayout{
    id: optionsGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    Rectangle{
        width:200
        Layout.minimumHeight:430
        Layout.fillHeight:true
        border.color: "#d3d3d3"

        GridLayout{
            id: menuGrid
            rows:4 
            flow: GridLayout.TopToBottom
            rowSpacing:0

            MenuOptionBtn {
                id:clientOption
                optionText:{
                    if (!clientStackBridge.isStandAlone){
                        i18nd("lliurex-shutdowner","Client configuration")
                    }else{
                        i18nd("lliurex-shutdowner","Desktop configuration")
                    }
                }
                optionIcon:"/usr/share/icons/breeze/devices/22/computer.svg"
                optionEnabled:true
                Connections{
                    function onMenuOptionClicked(){
                        mainStackBridge.manageTransitions(0)
                    }
                }
            }

            MenuOptionBtn {
                id:serverOption
                optionText:i18nd("lliurex-shutdowner","Server configuration")
                optionIcon:"/usr/share/icons/breeze/places/22/network-workgroup.svg"                  
                optionEnabled:clientStackBridge.isCronEnabled
                visible:!clientStackBridge.isStandAlone
                Connections{
                    function onMenuOptionClicked(){
                        mainStackBridge.manageTransitions(1)
                    }
                }
            }

            MenuOptionBtn{
                id:settingsOption
                optionText:i18nd("lliurex-shutdowner","System settings")
                optionIcon:"/usr/share/icons/breeze/actions/22/configure.svg"
                optionEnabled:{
                    if (!serverStackBridge.serverShut){
                        true
                    }else{
                        false
                    }
                }
                visible:clientStackBridge.isClient
                Connections{
                    function onMenuOptionClicked(){
                        mainStackBridge.manageTransitions(2)
                    }
                }
            }

            MenuOptionBtn {
                id:helpOption
                optionText:i18nd("lliurex-shutdowner","Help")
                optionIcon:"/usr/share/icons/breeze/actions/22/help-contents.svg"
                optionEnabled:true
                visible:true
                Connections{
                    function onMenuOptionClicked(){
                        mainStackBridge.openHelp();
                    }
                }
            }
        }
    }
    GridLayout{
        id:mainGrid
        rows:2
        flow:GridLayout.TopToBottom
        Layout.bottomMargin:10

        StackView {
            id: optionsLayout
            property int currentIndex:mainStackBridge.currentOptionStack
            Layout.fillHeight:true
            Layout.fillWidth:true
            Layout.alignment:Qt.AlignHCenter

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
                PropertyAnimation {
                    property: "opacity"
                    from: 0
                    to:1
                    duration: 60
                }
            }
            replaceExit: Transition {
                PropertyAnimation {
                    property: "opacity"
                    from: 1
                    to:0
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
            visible:mainStackBridge.showMessage[0]
            text:getMessageText()
            type: {
                if (mainStackBridge.showMessage[1]==""){
                    Kirigami.MessageType.Positive;
                }else{
                    Kirigami.MessageType.Error;
                }
            }
            Layout.minimumWidth:580
            Layout.topMargin:30
            
        }
        
    }

    function getMessageText(){

        switch(mainStackBridge.showMessage[1]){
            case -10:
                var msg=i18nd("lliurex-shutdowner","The client and server shutdown time are not compatible with each other");
                break;
            case -20:
                var msg=i18nd("lliurex-shutdowner","The client and server shutdown days are not compatible with each other");
                break;
            case -30:
                var msg=i18nd("lliurex-shutdowner","The client and server shutdown time and days are not compatible with each other");
                break;
            case -40:
                var msg=i18nd("lliurex-shutdowner","Disabling automatic shutdown in this computer is only posible if automatic server shutdown is not enabled")
                break;
            default:
                var msg=i18nd("lliurex-shutdowner","Changes saved successfully");
                break
        }
        return msg;
    }

}

