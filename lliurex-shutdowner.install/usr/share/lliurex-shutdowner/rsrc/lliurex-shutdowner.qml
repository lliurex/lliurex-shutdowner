import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.kirigami 2.4 as Kirigami


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
        y = Screen.height / 2 - height / 2
    }

    onClosing: {
        if (shutBridge.closeShutdowner(true)){
            close.accepted=true,
            console.log("Cleanup done, can close!");
        }else{
            close.accepted=false;	
        }
    }

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: margin
        Layout.minimumWidth:600	
        Layout.maximumWidth:600
        Layout.minimumHeight:shutBridge.isStandAlone? 450:570
        Layout.maximumHeight:shutBridge.isStandAlone? 450:570

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

        StackLayout {
            id: stackLayout
            currentIndex:shutBridge.currentStack
            implicitWidth: 600
            Layout.bottomMargin: 10
            Layout.alignment:Qt.AlignHCenter
            Layout.leftMargin:10
            Layout.rightMargin:10
            Layout.fillHeight: true

            GridLayout {
                id: loginGrid
                rows: 6
                flow: GridLayout.TopToBottom
                Layout.topMargin: 10
                Layout.bottomMargin: 10
                rowSpacing:10

                Item {
                  	Layout.fillWidth: true
                    Layout.topMargin:	(mainLayout.Layout.minimumHeight-bannerBox.Layout.minimumHeight)/2-loginGrid.rows*20
                }
                RowLayout {
                    Layout.fillWidth: true
                    Layout.alignment:Qt.AlignHCenter
                    Image{
                      	id:imgUsername
                      	source: "images/username.svg"
                    }
                    TextField {
                        id:userEntry
                        placeholderText:i18nd("lliurex-shutdowner","User")
                        implicitWidth:280
                        font.family: "Quattrocento Sans Bold"
                  		  font.pointSize: 10
                        Layout.alignment:Qt.AlignCenter
                      }
                  
                }
                RowLayout {
                    Layout.fillWidth: true
                    Layout.alignment:Qt.AlignHCenter
                    Image{
                      	id:imgPassword
                      	source: "images/password.svg"
                	  }
                    TextField {
                        id:passwordEntry
                        placeholderText:i18nd("lliurex-shutdowner","Password")
                        echoMode:TextInput.Password
                        implicitWidth: 280
                        font.family: "Quattrocento Sans Bold"
                  		  font.pointSize: 10
                        Layout.alignment:Qt.AlignCenter
                    }
                }
            		RowLayout {
                    id:serverRow
                    Layout.fillWidth: true
                    Layout.alignment:Qt.AlignHCenter
                    visible:!shutBridge.isStandAlone
              		  Image{
                      	id:imgServer
                      	source: "images/server.svg"
                  	 }
                    TextField {
                        id:serverEntry
                        placeholderText:i18nd("lliurex-shutdowner","Server IP    (Default value : server)")
                        implicitWidth: 280
                        font.family: "Quattrocento Sans Bold"
                  		  font.pointSize: 10
                        Layout.alignment:Qt.AlignCenter
                    }
                }
              	RowLayout {
                    Layout.fillWidth: true
                    Layout.alignment:Qt.AlignHCenter
                    
                    Button {
                        id:loginButton
                        text: i18nd("lliurex-shutdowner","Login")
                        onClicked: {
                            loginLabel.text=i18nd("lliurex-shutdowner","Validating user...")
                            loginLabel.color="black"
                            loginGrid.enabled=false
                            delay(1000, function() {
                                if (!shutBridge.running){
                                    loginGrid.enabled=true
                                    loginLabel.text=""
                                    timer.stop();
                                }
                            })
                            shutBridge.validate([userEntry.text,passwordEntry.text,serverEntry.text])
                        }
                    }
              
                }
                RowLayout{
                    Layout.fillWidth: true
                    Layout.alignment:Qt.AlignHCenter

                    Text {
                        id:loginLabel
                        text: ""
                        visible:true
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        color:"black"
                    }
                }

            }

            ClientOptions{
                id:clientOptions
            }

            ServerOptions{
                id:serverOptions
            }
        }

        RowLayout {
            id: footBox
            Layout.fillWidth: true
            Layout.minimumHeight:50
            Layout.maximumHeight:50
            Layout.leftMargin:10
            Layout.rightMargin:10
            Layout.bottomMargin: 10
            Button {
                id:helpBtn
                visible:{
                    if (shutBridge.currentStack!=0){
                        true
                    }else{
                        false
                    }
                }
                display:AbstractButton.TextBesideIcon
                icon.name:"help-whatsthis.svg"
                text:i18nd("lliurex-shutdowner","Help")
                Layout.preferredHeight: 40
                Layout.rightMargin:5
                onClicked:{
                    shutBridge.openHelp()
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
                Layout.fillWidth: true
                Layout.minimumHeight:40
            }
     
      }

  }
  Timer{
      id:timer
  }

  function delay(delayTime,cb){
      timer.interval=delayTime;
      timer.repeat=true;
      timer.triggered.connect(cb);
      timer.start()
  }


  function getMessageText(){

      switch (shutBridge.showMessage[1]){
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
              var msg=i18nd("lliurex-shutdowner","Invalid user");
              break;
          default:
              var msg=i18nd("lliurex-shutdowner","Changes saved successfully");
              break;
      }
      return msg
  }
}	    
