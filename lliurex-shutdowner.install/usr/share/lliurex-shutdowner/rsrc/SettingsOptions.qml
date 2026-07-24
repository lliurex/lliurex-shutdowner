import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami 2.16 as Kirigami


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
     
     	RowLayout{
         id: settingsGrid
         Layout.fillWidth: true


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
				onToggled: {
					settingsStackBridge.overrideShutdownSwitch(toggleswitch.checked)
				}
			}
		}

	}
}
