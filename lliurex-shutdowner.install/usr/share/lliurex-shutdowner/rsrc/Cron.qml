import QtQml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


GridLayout{
	id:calendar
	rows:2
	flow: GridLayout.TopToBottom

	property alias clockLayoutEnabled:clockLayout.enabled
	property alias currentHour:hoursTumbler.currentIndex
	property alias currentMinutes: minutesTumbler.currentIndex
	signal updateClock(variant value)
	property alias daysLayoutEnabled:daysLayout.enabled
	property alias mondayChecked:mondaybtn.dayBtnChecked
	property alias tuesdayChecked:tuesdaybtn.dayBtnChecked
	property alias wednesdayChecked:wednesdaybtn.dayBtnChecked
	property alias thursdayChecked:thursdaybtn.dayBtnChecked
	property alias fridayChecked:fridaybtn.dayBtnChecked
	signal updateWeekDays(variant value)


	RowLayout {
		id:clockLayout
		enabled:shutBridge.isCronEnabled
		Layout.leftMargin: 5
		Layout.rightMargin:5
		Layout.bottomMargin: 10
		Layout.alignment:Qt.AlignHCenter
		spacing:10   	
		Item {
			Layout.fillWidth: true
			width:200
		}
		

		Component {
			id: delegateComponent
			Label {
				font.pointSize: 55
				color: clockLayout.enabled? "#3daee9":"#87cefa"
				text: formatText(Tumbler.tumbler.count, modelData)
				horizontalAlignment: Text.AlignHCenter
				verticalAlignment: Text.AlignVCenter
				MouseArea {
					id: mouseAreaHour
					anchors.fill: parent
					hoverEnabled: true
					onEntered: {
						if (clockLayout.enabled){
							parent.color="#add8e6"
						}else{
							parent.color="#87cefa"
						}
					}
					onExited: {
						if (clockLayout.enabled){
							parent.color="#3daee9"
						}else{
							parent.color="#87cefa"
						}
					}
					onWheel:(wheel)=>{
						var index=modelData
						wheel.accepted=false
						if (wheel.angleDelta.y>0){
							if (modelData==0){
								if (Tumbler.tumbler.count==24){
									Tumbler.tumbler.currentIndex=23;
								}else{
									Tumbler.tumbler.currentIndex=59;
								}
							}else{
								Tumbler.tumbler.currentIndex=modelData-1;
							}
						}else{
							if (modelData==23){
								if (Tumbler.tumbler.count==24){
									Tumbler.tumbler.currentIndex=0;
								}else{
									Tumbler.tumbler.currentIndex=modelData+1;
								}
							}else{ 
								if (modelData==59){
									if (Tumbler.tumbler.count==60){
										Tumbler.tumbler.currentIndex=0;
									}else{
										Tumbler.tumbler.currentIndex=modelData+1;
									}
								}else{
									Tumbler.tumbler.currentIndex=modelData+1;
								}
							}
						}
					}
				}
			}
		}
			 
		Rectangle {
			anchors.topMargin: 4
			Layout.fillWidth: true
			Layout.alignment:Qt.AlignCenter
			height: 100
			width: 80
			color:"transparent"
			Tumbler {
				id: hoursTumbler
				width:80
				height:100
				model: 24
				currentIndex:currentHour
				delegate:delegateComponent 
				visibleItemCount:1
				hoverEnabled:true
				ToolTip.delay: 1000
				ToolTip.timeout: 3000
				ToolTip.visible: hovered
				ToolTip.text:i18nd("lliurex-shutdowner","You can use the mouse wheel to change the hour")
				onCurrentIndexChanged: {
					updateClock(["H",hoursTumbler.currentIndex]);
				} 
			}       
		}
		Text{
			id:clockSeparator
			Layout.fillWidth: true
			Layout.alignment:Qt.AlignCenter
			Layout.leftMargin:10
			font.pointSize:55
			color: clockLayout.enabled? "#3daee9":"#87cefa"
			text:":"
	    }
	    Rectangle {
			anchors.topMargin: 4
			Layout.fillWidth: true
			Layout.alignment:Qt.AlignCenter
			height: 100
			width: 80
			color:"transparent"

			Tumbler {
				id: minutesTumbler
				height:100
				width:80
				model: 60
				currentIndex:currentMinutes
				delegate: delegateComponent
				visibleItemCount:1
				hoverEnabled:true
				ToolTip.delay: 1000
				ToolTip.timeout: 3000
				ToolTip.visible: hovered
				ToolTip.text:i18nd("lliurex-shutdowner","You can use the mouse wheel to change the minutes")
				onCurrentIndexChanged: {
					updateClock(["M",minutesTumbler.currentIndex]);
				}
			}
		} 
		Button {
			id:editHourBtn
			display:AbstractButton.IconOnly
			icon.name:"edit-entry.svg"
			Layout.preferredHeight: 40
			Layout.alignment:Qt.AlignCenter
			Layout.topMargin:20
			Layout.leftMargin:10
			hoverEnabled:true
			ToolTip.delay: 1000
			ToolTip.timeout: 3000
			ToolTip.visible: hovered
			ToolTip.text:i18nd("lliurex-shutdowner","Click to edit shutdown time with keyboard ")
			onClicked:{
				hourEntry.text=formatEditText(hoursTumbler.currentIndex),
				minuteEntry.text=formatEditText(minutesTumbler.currentIndex),
				popupEditHour.open();
			}
			Popup {
				id: popupEditHour
				x: Math.round(parent.width/ 2)
				y: Math.round(parent.height)
				rightMargin:popupEditHour.width
				width: 205
				height: 170
				modal: true
				focus: true
				closePolicy: Popup.NoAutoClose
				enter: Transition {
				        NumberAnimation { property: "opacity"; from: 0.0; to: 1.0 }
				}
				exit: Transition {
					NumberAnimation { property: "opacity"; from: 1.0; to: 0.0 }
				}
				GridLayout{
					id:popupGrid
					rows:3
					flow: GridLayout.TopToBottom
					RowLayout {
						id: popupHourLayout
						Layout.alignment:Qt.AlignHCenter
						Layout.fillWidth: true
						Layout.bottomMargin: 10
						spacing:4
						TextField{
							id: hourEntry
							validator: RegularExpressionValidator { regularExpression: /([0-1][0-9]|2[0-3])/ }
							implicitWidth: 70
							horizontalAlignment: TextInput.AlignHCenter
							color:"#3daee9"
							font.pointSize: 40
						}

						Text{
							font.pointSize:40
							color:"#3daee9"
							text:":"
						}
				    	
						TextField{
							id: minuteEntry
							validator: RegularExpressionValidator { regularExpression: /[0-5][0-9]/ }
							implicitWidth: 70
							horizontalAlignment: TextInput.AlignHCenter
							color:"#3daee9"
							font.pointSize: 40
						}
					}

					RowLayout {
						id: footPopup
						Layout.fillWidth: true
						Layout.bottomMargin: 10

						Layout.alignment:Qt.AlignHCenter
						spacing:8

						Button {
							id:cancelEditBtn
							display:AbstractButton.TextBesideIcon
							icon.name:"dialog-cancel.svg"
							text:i18nd("lliurex-shutdowner","Cancel")
							Layout.preferredHeight: 40
							onClicked:{
								popupEditHour.close();
							}
					 	}
					 	Button {
							id:applyEditBtn
						   	display:AbstractButton.TextBesideIcon
						   	icon.name:"dialog-ok-apply.svg"
						   	text:i18nd("lliurex-shutdowner","Apply")
						   	Layout.preferredHeight: 40
						   	onClicked:{
						   		if (validateEntry(hourEntry.text,minuteEntry.text)){
						   			hoursTumbler.currentIndex=hourEntry.text,
						   			minutesTumbler.currentIndex=minuteEntry.text,
									delay(1000, function() {
										popupEditHour.close();
							        })
							    }else{
							    	popupEditHour.close();
							    }
						   		
					   		}
					 	}
					}      

			    }
			}
		}       
		Item {
			Layout.fillWidth: true
			width:200
		}
	}	

	RowLayout {
		id: daysLayout
		enabled:daysLayoutEnabled
		Layout.alignment:Qt.AlignHCenter
		Layout.fillWidth: true
		Layout.bottomMargin: 10
		spacing:8

	    DayButton {
	      	id:mondaybtn
			dayBtnChecked:mondayChecked
			dayBtnText:i18nd("lliurex-shutdowner","Monday")
			Connections{
				function onDayBtnClicked(value){
					updateWeekDays(["MO",value]);	
				}
			}
					
		}
				
		DayButton {
	       	id:tuesdaybtn
			dayBtnChecked:tuesdayChecked
			dayBtnText:i18nd("lliurex-shutdowner","Tuesday")
			Connections{
				function onDayBtnClicked(value){
					updateWeekDays(["TU",value]);
				}
			}
		}
		
		DayButton {
			id:wednesdaybtn
			dayBtnChecked:wednesdayChecked
			dayBtnText:i18nd("lliurex-shutdowner","Wednesday")
			Connections{
				function onDayBtnClicked(value){
					updateWeekDays(["WE",value]);
				}
			}
			
		}
				
		DayButton {
			id:thursdaybtn
			dayBtnChecked:thursdayChecked
			dayBtnText:i18nd("lliurex-shutdowner","Thursday")
			Connections{
				function onDayBtnClicked(value){
					updateWeekDays(["TH",value]);
				}
			}
		}
			
		DayButton {
			id:fridaybtn
			dayBtnChecked:fridayChecked
			dayBtnText:i18nd("lliurex-shutdowner","Friday")
			Connections{
				function onDayBtnClicked(value){
					updateWeekDays(["FR",value]);
				}
			}
		}
	}


	function formatText(count, modelData) {
		var data = count === 12 ? modelData + 1 : modelData;
		return data.toString().length < 2 ? "0" + data : data;
    }	

    function formatEditText(value){
		if (value<10){
			return "0"+value.toString();
		}else{
			return value.toString();
		}

    }

    function validateEntry(hour,minute){

		if ((hour =="") || (minute=="")){
			console.log("Vacio");
			return false;
		}else{
			return true;
		}

    }
    Timer {
	id: timer
    }

    function delay(delayTime, cb) {
        timer.interval = delayTime;
        timer.repeat = false;
        timer.triggered.connect(cb);
        timer.start();
    }
}				
