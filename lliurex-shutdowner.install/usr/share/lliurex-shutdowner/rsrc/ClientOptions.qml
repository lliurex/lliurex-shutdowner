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
	      	text:!clientStackBridge.isStandAlone?i18nd("lliurex-shutdowner","Client shutdown configuration"):i18nd("lliurex-shutdowner","Desktop shutdown configuration")
	      	font.pointSize: 16
	    }

    
		GroupBox {
			id: clockBoxClient
			Layout.fillWidth: true
			Layout.topMargin:10
			
			background: Rectangle {
				color:"#ffffff"
				border.color: "#d3d3d3"
				radius:5.0
        	}

        	ColumnLayout {
        		id: shutGridClient
        		spacing:5
        		anchors.fill:parent

        		RowLayout {
        			id: automaticLayoutClient
        			Layout.topMargin: 5
        			Text {
        				id:textMessageClient
        				text:!clientStackBridge.isStandAlone? i18nd("lliurex-shutdowner","Automatic client shutdown"):i18nd("lliurex-shutdowner","Automatic shutdown")
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
						onToggled: {
							clientStackBridge.getCronSwitchValue(toggleswitch.checked)
							cronClient.clockLayoutEnabled=toggleswitch.checked
							cronClient.daysLayoutEnabled=toggleswitch.checked
							serverOptionsLayout.enabled=toggleswitch.checked
						}
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

				RowLayout{
					Layout.fillWidth:true

					Cron{
						id:cronClient
						Layout.fillWidth:true
						clockLayoutEnabled:clientStackBridge.isCronEnabled
						currentHour:clientStackBridge.initClockClient.hour
						currentMinutes:clientStackBridge.initClockClient.minute
						daysLayoutEnabled:clientStackBridge.isCronEnabled
						weekDays:clientStackBridge.initWeekDaysClient

						Connections{
							target:cronClient

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
						font.pointSize: 10
						Layout.alignment:Qt.AlignVCenter
						Layout.minimumWidth:10
						Layout.leftMargin:5
					}

					Text {
						id:serverConfiguredOpText
						text:getTextOption()
						font.pointSize: 10
						Layout.maximumWidth:240
					}

					Button {
						id:serverConfigBtn
						display:AbstractButton.IconOnly
						icon.name:"configure"
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
			Layout.alignment:Qt.AlignHCenter
			visible:!clientStackBridge.isStandAlone
			
			background: Rectangle {
				color:"#ffffff"
				border.color: "#d3d3d3"
				radius:5.0
			}

			RowLayout {
				id: clientLayout
				anchors.fill:parent

				Text {
					id:clientText
					text:i18nd("lliurex-shutdowner","Currently detected clients:")
					font.pointSize: 10
					Layout.alignment:Qt.AlignVCenter
					Layout.minimumWidth:10
					Layout.leftMargin:5
				}

				Text {
					id:numberclientTex
					text:clientStackBridge.detectedClients
					font.pointSize: 10
					Layout.maximumWidth:240
					Layout.fillWidth: true
				}

				Button {
					id:shutnowBtn
					display:AbstractButton.TextBesideIcon
					icon.name:"system-shutdown"
					text:i18nd("lliurex-shutdowner","Shutdown clients now")
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
