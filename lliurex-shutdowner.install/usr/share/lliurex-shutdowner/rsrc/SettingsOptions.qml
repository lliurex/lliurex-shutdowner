import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.16 as Kirigami


Rectangle{
    color:"transparent"
    Text{ 
       text:i18nd("lliurex-shutdowner","System settings")
        font.family: "Quattrocento Sans Bold"
        font.pointSize: 16
    }

    GridLayout {
		id: mainGridSettings
		rows:1
		flow: GridLayout.TopToBottom
		Layout.fillWidth: true
		anchors.horizontalCenter:parent.horizontalCenter
		       
     	GridLayout {
     		id: settingsGrid
     		columns:2
     		flow: GridLayout.LeftToRight
     		Layout.bottomMargin: 10
     		columnSpacing:10
     		Layout.alignment:Qt.AlignHCenter
     		Layout.topMargin:55

     		Text {
     			id:textMessageSettings
     			text:i18nd("lliurex-shutdowner","Disable automatic shutdown on this computer:")
				font.family: "Quattrocento Sans Bold"
				font.pointSize: 10
				Layout.alignment:Qt.AlignRight
			}   

			Switch {
				id:toggleswitch
				checked: settingsStackBridge.isClientShutDownOverride
				Layout.alignment:Qt.AlignLeft
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
					settingsStackBridge.overrideShutdownSwitch(toggleswitch.checked);
				}
			}
		}

	}
}