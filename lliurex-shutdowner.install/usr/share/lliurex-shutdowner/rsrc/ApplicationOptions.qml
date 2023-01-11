import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.16 as Kirigami


GridLayout{
    id: optionsGrid
    columns: 2
    flow: GridLayout.LeftToRight
    columnSpacing:10

    Rectangle{
        width:170
        Layout.minimumHeight:430
        Layout.preferredHeight:shutBridge.isStandAlone? 440:580
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
                    if (!shutBridge.isStandAlone){
                        i18nd("lliurex-shutdowner","Client configuration")
                    }else{
                        i18nd("lliurex-shutdowner","Desktop configuration")
                    }
                }
                optionIcon:"/usr/share/icons/breeze/devices/16/computer.svg"
                optionEnabled:true
                optionVisible:true
                Connections{
                    function onMenuOptionClicked(){
                        shutBridge.manageTransitions(0)
                    }
                }
            }

            MenuOptionBtn {
                id:serverOption
                optionText:{
                    if (!shutBridge.isStandAlone){
                        i18nd("lliurex-shutdowner","Server configuration")
                    }else{
                        i18nd("lliurex-shutdowner","Help")
                    }
                }
                optionIcon:{
                    if (!shutBridge.isStandAlone){
                        "/usr/share/icons/breeze/places/16/network-workgroup.svg"
                    }else{
                        "/usr/share/icons/breeze/actions/16/help-contents.svg"
                    }
                }
                  
                optionEnabled:{
                    if (!shutBridge.isStandAlone){
                        shutBridge.isCronEnabled
                    }else{
                        true
                    }
                }
                optionVisible:true
                Connections{
                    function onMenuOptionClicked(){
                        if (!shutBridge.isStandAlon){
                            shutBridge.manageTransitions(1)
                        }else{
                            shutBridge.openHelp()  
                        }
                    }
                }
            }

            MenuOptionBtn{
                id:settingsOption
                optionText:{
                    if (shutBridge.isClient){
                        i18nd("lliurex-shutdowner","System settings")
                    }else{
                        i18nd("lliurex-shutdowner","Help")
                    }
                }
                optionIcon:{
                    if (shutBridge.isClient){
                        "/usr/share/icons/breeze/actions/16/configure.svg"
                    }else{
                        "/usr/share/icons/breeze/actions/16/help-contents.svg"
                    }
                }
                optionEnabled:{
                    if (shutBridge.isClient){
                        shutBridge.isCronEnabled
                    }else{
                        true
                    }
                }
                optionVisible:{
                    if (!shutBridge.isStandAlone){
                          true
                     }else{
                         false
                     }
                }
                Connections{
                    function onMenuOptionClicked(){
                        if (shutBridge.isClient){
                            shutBridge.manageTransitions(2)
                        }else{
                            shutBridge.openHelp()  
                        }
                    }
                }
            }

            MenuOptionBtn {
                id:helpOption
                optionText:i18nd("lliurex-shutdowner","Help")
                optionIcon:"/usr/share/icons/breeze/actions/16/help-contents.svg"
                optionEnabled:true
                optionVisible:{
                    if (!shutBridge.isStandAlone){
                        if (shutBridge.isClient){
                            true
                        }else{
                            false
                        }
                    }else{
                        false
                    }

                }
                Connections{
                    function onMenuOptionClicked(){
                        shutBridge.openHelp();
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
            property int currentIndex:shutBridge.currentOptionStack
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
                    duration: 600
                }
            }
            replaceExit: Transition {
                PropertyAnimation {
                    property: "opacity"
                    from: 1
                    to:0
                    duration: 600
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
            visible:shutBridge.showMessage[0]
            text:getMessageText()
            type: {
                if (shutBridge.showMessage[1]==""){
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

        switch(shutBridge.showMessage[1]){
            case -10:
                var msg=i18nd("lliurex-shutdowner","The client and server shutdown time are not compatible with each other");
                break;
            case -20:
                var msg=i18nd("lliurex-shutdowner","The client and server shutdown days are not compatible with each other");
                break;
            case -30:
                var msg=i18nd("lliurex-shutdowner","The client and server shutdown time and days are not compatible with each other");
                break;
            default:
                var msg=i18nd("lliurex-shutdowner","Changes saved successfully");
                break
        }
        return msg;
    }

}

