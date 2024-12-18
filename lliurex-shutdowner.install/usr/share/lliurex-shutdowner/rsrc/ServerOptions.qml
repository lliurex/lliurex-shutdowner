import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami


Rectangle{
    color:"transparent"
    Text{ 
        text:i18nd("lliurex-shutdowner","Server shutdown configuration")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout {
        id: mainGridServer
        rows:2
        flow: GridLayout.TopToBottom
        anchors.left:parent.left
        width:parent.width-10
        height:parent.height-90
        
        GroupBox {
            id: clockBoxServer
            Layout.fillWidth: true
            Layout.topMargin: mainStackBridge.showMessage[0]?35:10

            background: Rectangle {
                color:"#ffffff"
                border.color: "#d3d3d3"
            }
            visible:!clientStackBridge.isStandAlone

            GridLayout {
                id: shutGridServer
                rows:5
                flow: GridLayout.TopToBottom
                Layout.topMargin: 10
                Layout.bottomMargin: 10
                rowSpacing:5
                anchors.fill:parent

                RowLayout {
                    id: automaticLayoutServer
                    Layout.topMargin: 5
                    Text {
                        id:textMessageServer
                        text:i18nd("lliurex-shutdowner","Automatic server shutdown")
                        font.family: "Quattrocento Sans Bold"
                        font.pointSize: 10
                        Layout.alignment:Qt.AlignVCenter
                        Layout.leftMargin:5
                    }   
                    Switch {
                        id:toggleswitchServer
                        checked: serverStackBridge.serverShut
                        Layout.alignment:Qt.AlignVCenter
                        Layout.fillWidth: true
                        Layout.rightMargin:5
                        indicator: Rectangle {
                            implicitWidth: 40
                            implicitHeight: 10
                            x: toggleswitchServer.width - width - toggleswitchServer.rightPadding
                            y: parent.height/2 - height/2 
                            radius: 7
                            color: toggleswitchServer.checked ? "#3daee9" : "#d3d3d3"
                            Rectangle {
                                x: toggleswitchServer.checked ? parent.width - width : 0
                                width: 20
                                height: 20
                                y:parent.height/2-height/2
                                radius: 10
                                border.color: "#808080"
                            }
                        }
                        onToggled: enableLayouts()
        			}
      			}

                Rectangle {
                    Layout.leftMargin: 5
                    Layout.rightMargin:5
                    Layout.bottomMargin: 10
                    Layout.preferredWidth: 555
                    height: 1
                    border.color:"#000000"
                    border.width: 5
                    radius: 10
                }
      			RowLayout {
                    id: serverLayoutOp1
                    Layout.fillWidth: true
                    Layout.bottomMargin: 10
                    enabled:toggleswitchServer.checked
                    visible:true
                    spacing:15
                    CheckBox {
                        id:serverShutOp1
                        text:i18nd("lliurex-shutdowner","Shutdown server 2 minutes after clients)")
                        checked:!serverStackBridge.customServerShut
                        font.pointSize: 10
                        focusPolicy: Qt.NoFocus
                        onToggled:enableServerOptions(1)
                    }
                } 

                RowLayout {
                    id: serverLayoutOp2
                    Layout.fillWidth: true
                    Layout.bottomMargin: 10
                    enabled:toggleswitchServer.checked
                    visible:true
                    spacing:15
                    CheckBox {
                        id:serverShutOp2
                        text:i18nd("lliurex-shutdowner","Custom:")
                        font.pointSize: 10
                        focusPolicy: Qt.NoFocus
                        checked:serverStackBridge.customServerShut
                        onToggled:enableServerOptions(2)
                    }
                } 

                RowLayout{
                    Cron{
                        id:cronServer
                        clockLayoutEnabled:enableClock()
                        currentHour:serverStackBridge.initClockServer[0]				
                        currentMinutes:serverStackBridge.initClockServer[1]
                        daysLayoutEnabled:clockLayoutEnabled
                        mondayChecked:serverStackBridge.initWeekDaysServer[0]
                        tuesdayChecked:serverStackBridge.initWeekDaysServer[1]
                        wednesdayChecked:serverStackBridge.initWeekDaysServer[2]
                        thursdayChecked:serverStackBridge.initWeekDaysServer[3]
                        fridayChecked:serverStackBridge.initWeekDaysServer[4]

                        Connections{
                            function onUpdateClock(value){
                                serverStackBridge.getClockServerValues(value);
            		    	}
                            function onUpdateWeekDays(value){
                                serverStackBridge.getWeekServerValues(value);	
            		    	}
          		    	}
                    }
                }
    		 
            }
  	     }
    }

    function enableLayouts(){

        serverStackBridge.getServerShut(toggleswitchServer.checked)
        if (toggleswitchServer.checked){
            if (serverShutOp2.checked){
                cronServer.clockLayoutEnabled=true,
                cronServer.daysLayoutEnabled=true;
            }
            serverLayoutOp1.enabled=true,
            serverLayoutOp2.enabled=true;
        }else{
            serverLayoutOp1.enabled=false,
            serverLayoutOp2.enabled=false,
            cronServer.clockLayoutEnabled=false,
            cronServer.daysLayoutEnabled=false;
        }
    }

    function enableServerOptions(option){

        if (option==1){
            serverStackBridge.getCustomServerShut(!serverShutOp1.checked)
            serverShutOp2.checked=!serverShutOp1.checked,
            cronServer.clockLayoutEnabled=!serverShutOp1.checked,
            cronServer.daysLayoutEnabled=!serverShutOp1.checked;
        }else{
            serverStackBridge.getCustomServerShut(serverShutOp2.checked),
            serverShutOp1.checked=!serverShutOp2.checked,
            cronServer.clockLayoutEnabled=serverShutOp2.checked,
            cronServer.daysLayoutEnabled=serverShutOp2.checked;
        } 
    }

    function enableClock(){

        if (toggleswitchServer.checked){
            if (serverStackBridge.customServerShut){
                return true;
            }else{
                return false;
            }
        }else{
            return false;
        }
    }
}

	
				

			
