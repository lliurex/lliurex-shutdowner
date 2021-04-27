import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2

ApplicationWindow {
	visible: true
	title: "LliureX Shutdowner"
	property int margin: 1
	color:"#eff0f1"
	width: 610
	height: mainLayout.implicitHeight + 2 * margin
	minimumWidth: 610
	minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
	maximumWidth: 610
	maximumHeight: mainLayout.Layout.maximumHeight + 2 * margin
	Component.onCompleted: {
	    x = Screen.width/2 - width/2 
        y = Screen.height/2 - height/2

    }

    onClosing: {
     	if (bridge.closed(true))
     		removePropertiesConnect(),
     		close.accepted=true;
        else
        	close.accepted=false;	
              
    }

    ColumnLayout {
    	id: mainLayout
    	anchors.fill: parent
    	anchors.margins: margin
    	Layout.minimumWidth:610	
    	Layout.maximumWidth:610
    	Layout.minimumHeight:btnBox.visible?205:160
    	Layout.maximumHeight:btnBox.visible?205:160
    	
	   	GridLayout {
	   		id: grid
	   		Layout.topMargin: 5
	   		Layout.bottomMargin: 0
	   		rows: 3
	   		columns: 2
	   		Rectangle {
	   			color:"transparent"
	   			Layout.rowSpan: 1
	   			Layout.columnSpan: 1
	   			Layout.leftMargin:10
	   			width:60
	   			height:60
	   			Image{
	   				source:"/usr/share/icons/breeze/status/64/dialog-warning.svg"
	   				anchors.centerIn:parent
	   			}
	   		}
	   		Rectangle {
	   			color:"transparent"
	   			Layout.rowSpan: 1
	   			Layout.columnSpan: 1
	   			height:60
	   			Layout.fillWidth: true
	   			Layout.leftMargin:10
	   			Text{
	   				id:warningText
	   				text:bridge.translateMsg[0]
	   				font.family: "Quattrocento Sans Bold"
	   				font.pointSize: 11
	   				anchors.left: parent.left
	   				anchors.verticalCenter:parent.verticalCenter
	   			}
	   		}
	   		Rectangle {
	   			color:"transparent"
	   			Layout.rowSpan: 1
	   			Layout.columnSpan: 2
	   			Layout.fillWidth: true
	   			height:70
	   			Text {
	   				id:countDown
	   				visible:true
	   				font.family: "Quattrocento Sans Bold"
	   				font.pointSize: 50
	   				anchors.centerIn:parent
	   				text:bridge.timeRemaining[0]
	   				color:bridge.timeRemaining[1]
	   			}
	   		}
	   		Rectangle {
	   			id:btnBox
	   			color:"transparent"
	   			visible:bridge.visibleCancelBtn
	   			Layout.rowSpan: 1
	   			Layout.columnSpan: 2
	   			Layout.fillWidth: true
	   			Layout.rightMargin:10
	   			height:60
	   			Button {
	   				id:cancelBtn
	   				height: 35
	   				anchors.right: parent.right
	   				anchors.verticalCenter:parent.verticalCenter
	   				display:AbstractButton.TextBesideIcon
	   				icon.source:"/usr/share/icons/breeze/actions/16/dialog-cancel.svg"
	   				icon.width:16
	   				icon.height:16
	   				text:bridge.translateMsg[1]
	   				background: Rectangle{ 
	   					color:"#f0f1f2"
	   					border.color: "#b3b5b6"
	   					radius:2
					}
					MouseArea {
						id: mouseArea
						anchors.fill: parent
						hoverEnabled: true
						onEntered: {
							parent.background.border.color="#3daee9"
						}
						onExited: {
							parent.background.border.color="#b3b5b6"
						}
						onPressed:{
							parent.background.color="#94cfeb"
						}
						onClicked:{
							bridge.cancelClicked(),
							removePropertiesConnect()
						} 
					}	 
				}	
		    }
		}
	
	 }

	 function removePropertiesConnect(){
	 	warningText.text="",
	 	countDown.text="",
	 	countDown.color="#3daee9",
	 	cancelBtn.text="",
	 	btnBox.visible=false;
	 }
}  		