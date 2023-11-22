import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.16 as Kirigami


Rectangle{
    color:"transparent"
    Text{ 
       text:!clientStackBridge.isStandAlone?i18nd("lliurex-shutdowner","Client shutdown configuration"):i18nd("lliurex-shutdowner","Desktop shutdown configuration")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout {
		id: mainGridClient
		rows:2
		flow: GridLayout.TopToBottom
		anchors.left:parent.left
		width:parent.width-10
		height:parent.height-90
       
		GroupBox {
			id: clockBoxClient
			Layout.fillWidth: true
			Layout.topMargin: {
				if (mainStackBridge.showMessage[0]){
					35
				}else{
					if (!clientStackBridge.isStandAlone){
						45
					}
				}
			}

			background: Rectangle {
				color:"#ffffff"
				border.color: "#d3d3d3"
        	}

        	GridLayout {
        		id: shutGridClient
        		rows:5
        		flow: GridLayout.TopToBottom
        		Layout.topMargin: 10
        		Layout.bottomMargin: 10
        		rowSpacing:5
        		anchors.fill:parent

        		RowLayout {
        			id: automaticLayoutClient
        			Layout.topMargin: 5
        			Text {
        				id:textMessageClient
        				text:!clientStackBridge.isStandAlone? i18nd("lliurex-shutdowner","Automatic client shutdown"):i18nd("lliurex-shutdowner","Automatic shutdown")
						font.family: "Quattrocento Sans Bold"
						font.pointSize: 10
						Layout.alignment:Qt.AlignVCenter
						Layout.leftMargin:5
					}   

					Switch {
						id:toggleswitch
						checked: clientStackBridge.isCronEnabled
						Layout.alignment:Qt.AlignVCenter
						Layout.fillWidth: true
						Layout.rightMargin:5
						indicator: Rectangle {
							implicitWidth: 40
							implicitHeight: 10
							x: toggleswitch.width - width - toggleswitch.rightPadding
							y: parent.height/2 - height/2 
							radius: 7
							color: toggleswitch.checked ? "#3daee9" : "#d3d3d3"

							Rectangle {
								x: toggleswitch.checked ? parent.width - width : 0
								width: 20
								height: 20
								y:parent.height/2-height/2
								radius: 10
								border.color: "#808080"
					    	}
						}	

						onToggled: {
							clientStackBridge.getCronSwitchValue(toggleswitch.checked);
							cronClient.clockLayoutEnabled=toggleswitch.checked,
							cronClient.daysLayoutEnabled=toggleswitch.checked,
							serverOptionsLayout.enabled=toggleswitch.checked;
						}
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

				RowLayout{
					Cron{
						id:cronClient
						clockLayoutEnabled:clientStackBridge.isCronEnabled
						currentHour:clientStackBridge.initClockClient[0]
						currentMinutes:clientStackBridge.initClockClient[1]
						daysLayoutEnabled:clientStackBridge.isCronEnabled
						mondayChecked:clientStackBridge.initWeekDaysClient[0]
						tuesdayChecked:clientStackBridge.initWeekDaysClient[1]
						wednesdayChecked:clientStackBridge.initWeekDaysClient[2]
						thursdayChecked:clientStackBridge.initWeekDaysClient[3]
						fridayChecked:clientStackBridge.initWeekDaysClient[4]

						Connections{
							function onUpdateClock(value){
								clientStackBridge.getClockClientValues(value);
							}
							function onUpdateWeekDays(value){
								clientStackBridge.getWeekClientValues(value);	
							}
						}
					}
				}

				RowLayout {
					id: serverOptionsLayout
					Layout.alignment:Qt.AlignHCenter
					Layout.fillWidth: true
					Layout.bottomMargin: 10
					enabled:clientStackBridge.isCronEnabled
					visible:!clientStackBridge.isStandAlone
					spacing:15
					Text{
						id:serverOptionsText
						text:i18nd("lliurex-shutdowner","Shutdown server as well:")
						font.family: "Quattrocento Sans Bold"
						font.pointSize: 10
						Layout.alignment:Qt.AlignVCenter
						Layout.minimumWidth:10
						Layout.leftMargin:5
					}
					Text {
						id:serverConfiguredOpText
						text:getTextOption()
						font.family: "Quattrocento Sans Bold"
						font.pointSize: 10
						Layout.maximumWidth:240
					}
					Button {
						id:serverConfigBtn
						display:AbstractButton.IconOnly
						icon.name:"configure.svg"
						Layout.preferredHeight: 40
						Layout.topMargin: 5
						Layout.bottomMargin: 5
						Layout.rightMargin:5
						hoverEnabled:true
						ToolTip.delay: 1000
						ToolTip.timeout: 3000
						ToolTip.visible: hovered
						ToolTip.text:i18nd("lliurex-shutdowner","Click to change server shutdown settings")
						
						onClicked:{
							mainStackBridge.manageTransitions(1)
						}
					}
				} 
			}
		}

		GroupBox {
			id: clientBox
			Layout.fillWidth: true
			Layout.maximumHeight:80
			Layout.alignment:Qt.AlignHCenter
			visible:!clientStackBridge.isStandAlone
			background: Rectangle {
				color:"#ffffff"
				border.color: "#d3d3d3"
			}

			RowLayout {
				id: clientLayout
				Layout.topMargin: 0
				Layout.bottomMargin: 10
				anchors.fill:parent

				Text {
					id:clientText
					text:i18nd("lliurex-shutdowner","Currently detected clients:")
					font.family: "Quattrocento Sans Bold"
					font.pointSize: 10
					Layout.alignment:Qt.AlignVCenter
					Layout.minimumWidth:10
					Layout.leftMargin:5
				}

				Text {
					id:numberclientTex
					text:clientStackBridge.detectedClients
					font.family: "Quattrocento Sans Bold"
					font.pointSize: 10
					Layout.maximumWidth:240
					Layout.fillWidth: true
				}

				Button {
					id:shutnowBtn
					display:AbstractButton.TextBesideIcon
					icon.name:"system-shutdown.svg"
					text:i18nd("lliurex-shutdowner","Shutdown clients now")
					Layout.preferredHeight: 40
					Layout.topMargin: 5
					Layout.bottomMargin: 5
					Layout.rightMargin:5
					onClicked:{
						clientStackBridge.shutdownClientsNow()
					}
		      }
	    	}      	
	
	    }
	}
	function getTextOption(){
		if (serverStackBridge.serverShut){
			if (serverStackBridge.customServerShut){
				return i18nd("lliurex-shutdowner","Custom shutdown");
			}else{
				return i18nd("lliurex-shutdowner","2 minutes after clients");
			}
		}else{
			return i18nd("lliurex-shutdowner","Not configured")
		}
					
	}
}