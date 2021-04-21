import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2

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
		Layout.fillWidth: true
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
						parent.color="#add8e6"
					}
					onExited: {
						parent.color="#3daee9"
					}
					onWheel:{
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
	       	Layout.alignment:Qt.AlignVCenter
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
			Layout.fillWidth: true
			Layout.alignment:Qt.AlignVCenter
			font.pointSize:55
			color: clockLayout.enabled? "#3daee9":"#87cefa"
			text:":"
	    }
	    Rectangle {
	    	anchors.topMargin: 4
	    	Layout.fillWidth: true
	    	Layout.alignment:Qt.AlignHCenter
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
}				
