import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami


Rectangle{
    color:"transparent"

    ColumnLayout{
        id:generalLayout
        anchors.top:parent.top
        anchors.left:parent.left
        anchors.right:parent.right

        anchors.leftMargin:5
        anchors.rightMargin:15
        anchors.bottomMargin:25
        spacing: 10

        Text{ 
            text:i18nd("lliurex-shutdowner","Server shutdown configuration")
            font.pointSize: 16
        }
        
        GroupBox {
            id: clockBoxServer
            Layout.fillWidth: true
            Layout.topMargin:10

            background: Rectangle {
                color:"#ffffff"
                border.color: "#d3d3d3"
                radius:5.0
            }

            visible:!clientStackBridge.isStandAlone

            ColumnLayout {
                id: shutGridServer
                spacing:5
                anchors.fill:parent

                RowLayout {
                    id: automaticLayoutServer
                    Layout.topMargin: 5

                    Text {
                        id:textMessageServer
                        text:i18nd("lliurex-shutdowner","Automatic server shutdown")
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
                        onToggled: enableLayouts()
        			}
      			}

                Rectangle {
                    Layout.leftMargin: 5
                    Layout.rightMargin:5
                    Layout.bottomMargin: 10
                    Layout.fillWidth:true
                    Layout.preferredWidth: 555
                    height: 1
                    color:"#000000"
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
                    Layout.fillWidth:true
                    Cron{
                        id:cronServer
                        Layout.fillWidth:true
                        clockLayoutEnabled:enableClock()
                        currentHour:serverStackBridge.initClockServer.hour				
                        currentMinutes:serverStackBridge.initClockServer.minute
                        daysLayoutEnabled:clockLayoutEnabled
                        weekDays:serverStackBridge.initWeekDaysServer

                        Connections{
                            target: cronServer

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

	
				

			
