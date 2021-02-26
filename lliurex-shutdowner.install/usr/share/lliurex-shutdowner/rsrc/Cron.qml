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
	property alias mondayChecked:mondaybtn.checked
	property alias tuesdayChecked:tuesdaybtn.checked
	property alias wednesdayChecked:wednesdaybtn.checked
	property alias thursdayChecked:thursdaybtn.checked
	property alias fridayChecked:fridaybtn.checked
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
			font.pointSize:55;
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
	        
	    Button {
	      	id:mondaybtn
			checkable: true
			checked:mondayChecked
			text:i18nd("lliurex-shutdowner","Monday")
			Layout.preferredWidth: 100
			Layout.preferredHeight: 40
			palette.button:paletteBtn(mondaybtn.checked)
			palette.buttonText:paletteBtnText(mondaybtn.checked)
			focusPolicy: Qt.NoFocus
			onClicked: {
				updateWeekDays(["MO",mondaybtn.checked]);
			}
		}
				
		Button {
	       	id:tuesdaybtn
			checkable: true
			checked:tuesdayChecked
			text:i18nd("lliurex-shutdowner","Tuesday")
			Layout.preferredWidth: 100
			Layout.preferredHeight: 40
			palette.button:paletteBtn(tuesdaybtn.checked)
			palette.buttonText:paletteBtnText(tuesdaybtn.checked)
			focusPolicy: Qt.NoFocus
			onClicked: {
				updateWeekDays(["TU",tuesdaybtn.checked]);
			}
		}
		
		Button {
			id:wednesdaybtn
			checkable: true
			checked:wednesdayChecked
			text:i18nd("lliurex-shutdowner","Wednesday")
			Layout.preferredWidth: 100
			Layout.preferredHeight: 40
			palette.button:paletteBtn(wednesdaybtn.checked)
			palette.buttonText:paletteBtnText(wednesdaybtn.checked)
			focusPolicy: Qt.NoFocus
			onClicked: {
				updateWeekDays(["WE",wednesdaybtn.checked]);
			}
		}
				
		Button {
			id:thursdaybtn
			checkable: true
			checked:thursdayChecked
			text:i18nd("lliurex-shutdowner","Thursday")
			Layout.preferredWidth: 100
			Layout.preferredHeight: 40
			palette.button:paletteBtn(thursdaybtn.checked)
			palette.buttonText:paletteBtnText(thursdaybtn.checked)
			focusPolicy: Qt.NoFocus
			onClicked: {
				updateWeekDays(["TH",thursdaybtn.checked]);
			}
		}
			
		Button {
			id:fridaybtn
			checkable: true
			checked:fridayChecked
			text:i18nd("lliurex-shutdowner","Friday")
			Layout.preferredWidth: 100
			Layout.preferredHeight: 40
			palette.button:paletteBtn(fridaybtn.checked)
			palette.buttonText:paletteBtnText(fridaybtn.checked)
			focusPolicy: Qt.NoFocus
			onClicked: {
				updateWeekDays(["FR",fridaybtn.checked]);
			}
		}
	}

	function paletteBtn(status){
		if (daysLayout.enabled){
			if (status){
				return "#3daee9";
			}else{ 
				return "#f0f1f2";
			}
		}else{
			if (status){
				return "#87cefa";
			}else{
				return "#e4e5e7";
			}
		}	

	}

	function paletteBtnText(status){
		if (daysLayout.enabled){
			if (status){
				return "#ffffff";
			}else{ 
				return "#000000";
			}	
		}else{
			if (status){
				return "#ffffff";
			}else{
				return "#b9babc";
			}
		}	

	}

	function formatText(count, modelData) {
        var data = count === 12 ? modelData + 1 : modelData;
        return data.toString().length < 2 ? "0" + data : data;
    }	
}				
