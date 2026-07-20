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
	      text:i18nd("lliurex-shutdowner","System settings")
	      font.pointSize: 16
	   }
     
     	ColumnLayout{
         id: settingsGrid
         spacing:5


     		Text {
     			id:textMessageSettings
     			text:i18nd("lliurex-shutdowner","Disable automatic shutdown on this computer:")
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
					settingsStackBridge.overrideShutdownSwitch(toggleswitch.checked)
				}
			}
		}

	}
}
