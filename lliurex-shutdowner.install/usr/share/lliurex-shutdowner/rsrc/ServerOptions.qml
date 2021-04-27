import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2


GridLayout {
  id: mainGridServer
  rows:2
  flow: GridLayout.TopToBottom
  Layout.topMargin: 5
  Layout.bottomMargin:10
  rowSpacing:5

  GroupBox {
    id: clockBoxServer
    Layout.fillWidth: true
    background: Rectangle {
      color:"#ffffff"
      border.color: "#d3d3d3"
    }
    visible:!shutBridge.isStandAlone
    Layout.alignment:Qt.AlignHCenter

    GridLayout {
      id: shutGridServer
      rows:6
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
          checked: shutBridge.serverShut
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
          checked:!shutBridge.customServerShut
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
          checked:shutBridge.customServerShut
          onToggled:enableServerOptions(2)
        }
      } 

      RowLayout{
        Cron{
          id:cronServer
          clockLayoutEnabled:enableClock()
          currentHour:shutBridge.initClockServer[0]				
          currentMinutes:shutBridge.initClockServer[1]
          daysLayoutEnabled:clockLayoutEnabled
          mondayChecked:shutBridge.initWeekDaysServer[0]
          tuesdayChecked:shutBridge.initWeekDaysServer[1]
          wednesdayChecked:shutBridge.initWeekDaysServer[2]
          thursdayChecked:shutBridge.initWeekDaysServer[3]
          fridayChecked:shutBridge.initWeekDaysServer[4]

          Connections{
            function onUpdateClock(value){
              shutBridge.getClockServerValues(value);
		    		}
            function onUpdateWeekDays(value){
              shutBridge.getWeekServerValues(value);	
		    		}
		    	}
        }
      }
			
      RowLayout {
        id: backBtnLayout
        Layout.fillWidth: true
				
        Button {
          id:backBtn
          visible:true
          display:AbstractButton.IconOnly
          icon.name:"arrow-left.svg"
          Layout.preferredHeight: 40
          Layout.topMargin: 5
          Layout.bottomMargin: 5
          Layout.leftMargin:5
          onClicked:{
            stackLayout.currentIndex=1;
          }
        }
      }   
    }
	}

  function enableLayouts(){

    shutBridge.getServerShut(toggleswitchServer.checked)
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
      shutBridge.getCustomServerShut(!serverShutOp1.checked)
      serverShutOp2.checked=!serverShutOp1.checked,
      cronServer.clockLayoutEnabled=!serverShutOp1.checked,
      cronServer.daysLayoutEnabled=!serverShutOp1.checked;
    }else{
      shutBridge.getCustomServerShut(serverShutOp2.checked),
      serverShutOp1.checked=!serverShutOp2.checked,
      cronServer.clockLayoutEnabled=serverShutOp2.checked,
      cronServer.daysLayoutEnabled=serverShutOp2.checked;
    } 
  }

  function enableClock(){

    if (toggleswitchServer.checked){
      if (shutBridge.customServerShut){
        return true;
      }else{
        return false;
      }
    }else{
      return false;
    }
  }

  function removeConnection(){
    clockBoxServer.visible=false,
  	toggleswitchServer.checked=false,
  	serverShutOp1.checked=false,
  	serverShutOp2.checked=false,
    cronServer.clockLayoutEnabled=false,
    cronServer.currentHour=false,
    cronServer.currentMinutes=false,
    cronServer.daysLayoutEnabled=false,
    cronServer.mondayChecked=false,
    cronServer.tuesdayChecked=false,
    cronServer.wednesdayChecked=false,
    cronServer.thursdayChecked=false,
    cronServer.fridayChecked=false;
  }
}		
				

			