import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


ColumnLayout{
	id:scheduler
    spacing: 10
    focus: true

	property alias clockLayoutEnabled:clockLayout.enabled
	property alias currentHour:hoursSelector.currentIndex
	property alias currentMinutes: minutesSelector.currentIndex
	signal updateClock(variant value)
	property alias daysLayoutEnabled:daysLayout.enabled

	property var weekDays
	signal updateWeekDays(variant value)


	RowLayout {
        id: clockLayout
        Layout.alignment: Qt.AlignHCenter
        spacing: 5

        property int hoursWheelAccumulator:0
        property int minutesWheelAccumulator:59
        readonly property int wheelThreshold:360

        Component {
            id: numberDelegate
            Item {
                width: 80
                height: 80

                HoverHandler{
                    id:itemHoverHandler
                }

                Text {
                    text: modelData.toString().padStart(2, "0")
                    font.pointSize: 50
                    color: paletteText(itemHoverHandler.hovered)
                    anchors.centerIn: parent
                }

                ToolTip.delay:1000
                ToolTip.timeout:1000
                ToolTip.visible:itemHoverHandler.hovered
                ToolTip.text:i18nd("lliurex-shutdowner","You can use the mouse wheel to change the value")
            }
        }

        Rectangle {
            width: 80
            height: 80
            color: "transparent"
            clip: true

            PathView {
                id: hoursSelector
                anchors.fill: parent
                focus: true
                model: 24
                delegate: numberDelegate

                pathItemCount: 3
                preferredHighlightBegin: 0.5
                preferredHighlightEnd: 0.5
                highlightRangeMode: PathView.StrictlyEnforceRange


                onCurrentIndexChanged: {
                	updateClock({"hour": hoursSelector.currentIndex});
                }

                WheelHandler {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad

                    onWheel: (event) => {

                        let delta=event.angleDelta.y;

                        if ((delta >0 && clockLayout.hoursWheelAccumulator < 0) || ( delta <0 && clockLayout.hoursWheelAccumulator > 0)){
                            clockLayout.hoursWheelAccumulator = 0;
                        }

                        clockLayout.hoursWheelAccumulator+=delta;

                        if (clockLayout.hoursWheelAccumulator >= clockLayout.wheelThreshold){
                            hoursSelector.decrementCurrentIndex();
                            clockLayout.hoursWheelAccumulator=0;
                        } 
                        else if (clockLayout.hoursWheelAccumulator <= -clockLayout.wheelThreshold) {
                            hoursSelector.incrementCurrentIndex();
                            clockLayout.hoursWheelAccumulator=0;
                        }
                            
                    }
                }

                path: Path {
                    startX: 40; startY: -80
                    PathPercent {value:0.0}

                    PathLine { x: 40; y: 40 }
                    PathPercent {value:0.5}

                    PathLine { x: 40; y: 160 }
                    PathPercent {value:1.0}

                }
            }
        }

        Text {
            text: ":"
            font.pointSize: 40
            color: "#3daee9"
            Layout.alignment: Qt.AlignCenter
        }

        Rectangle {
            width: 80
            height: 80
            color: "transparent"
            clip: true

            PathView {
                id: minutesSelector
                anchors.fill: parent
                focus: true
                model: 60
                delegate: numberDelegate

                pathItemCount: 3
                preferredHighlightBegin: 0.5
                preferredHighlightEnd: 0.5
                highlightRangeMode: PathView.StrictlyEnforceRange


                onCurrentIndexChanged: {
                    updateClock({"minute": minutesSelector.currentIndex});
                }

                WheelHandler {
                    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
                    onWheel: (event) => {

                        let delta=event.angleDelta.y;

                        if ((delta >0 && clockLayout.minutesWheelAccumulator < 0) || ( delta <0 && clockLayout.minutesWheelAccumulator > 0)){
                            clockLayout.minutesWheelAccumulator = 0;
                        }

                        clockLayout.minutesWheelAccumulator+=delta;

                        if (clockLayout.minutesWheelAccumulator >= clockLayout.wheelThreshold){ 
                            minutesSelector.decrementCurrentIndex();
                            clockLayout.minutesWheelAccumulator = 0;
                        } else if (clockLayout.minutesWheelAccumulator <= -clockLayout.wheelThreshold) {
                            minutesSelector.incrementCurrentIndex();
                            clockLayout.minutesWheelAccumulator = 0;
                        }
                    }
                }

                path: Path {
                    startX: 40; startY: -80
                    PathPercent {value:0.0}

                    PathLine { x: 40; y: 40 }
                    PathPercent {value:0.5}

                    PathLine { x: 40; y: 160 }
                    PathPercent {value:1.0}
                }
            }
        }
 
		Button {
			id:editHourBtn
			display:AbstractButton.IconOnly
			icon.name:"edit-entry"
			Layout.alignment:Qt.AlignCenter
            Layout.topMargin: 10
            Layout.leftMargin: 10
            hoverEnabled: true

			ToolTip.delay: 1000
			ToolTip.timeout: 3000
			ToolTip.visible: hovered
			ToolTip.text:i18nd("lliurex-shutdowner","Click to edit shutdown time with keyboard ")
			
			onClicked:{
				timeSelector.open()
			}
			
		}
		
	}	

	RowLayout {
		id: daysLayout
		enabled:daysLayoutEnabled
		Layout.alignment:Qt.AlignHCenter
		Layout.bottomMargin: 10
		spacing:8

        Item{
            Layout.fillWidth:true
        }


        Repeater {

        	model:[
               { key: "0", name: i18nd("lliurex-shutdowner","Monday")},
               { key: "1", name: i18nd("lliurex-shutdowner","Tuesday") },
               { key: "2", name: i18nd("lliurex-shutdowner","Wednesday") },
               { key: "3", name: i18nd("lliurex-shutdowner","Thursday") },
               { key: "4", name: i18nd("lliurex-shutdowner","Friday") } 
            ]

        	DayButton{
        		dayBtnChecked:weekDays[modelData.key]
        		dayBtnText: modelData.name
                dayBtnEnabled:daysLayout.enabled
        		onDayBtnClicked: (value) => {
                    updateWeekDays({[modelData.key]: value});
                }

        	}

        }

        Item{
            Layout.fillWidth:true
        }
	    
	}


	TimeSelector {
        id: timeSelector
        
        Binding{
            target:timeSelector
            property:"hourValue"
            value:hoursSelector.currentIndex.toString().padStart(2, "0")

        }

        Binding{
            target:timeSelector
            property:"minuteValue"
            value:minutesSelector.currentIndex.toString().padStart(2, "0")

        }

        Connections {
            target: timeSelector
            function onTimeApplyClicked(hourValue, minuteValue){
                hoursSelector.currentIndex = hourValue
                minutesSelector.currentIndex = minuteValue
            }
        }
    }

    Timer {
        id: safetyTimer
        property var callback: null
        onTriggered: {
            if (callback) {
                callback();
                callback = null;
            }
        }
    }

    function delay(delayTime, cb) {
        safetyTimer.stop();
        safetyTimer.interval = delayTime;
        safetyTimer.callback = cb;
        safetyTimer.start();
    }

    function validateEntry(hour, minute) {
        return hour !== "" && minute !== "";
    }

    function paletteText(isHovered=false) {

        if (clockLayout.enabled) { 
            return isHovered ? "#add8e6":"#3daee9"
        }else {
            return "#87cefa"
        }
    }
}				
