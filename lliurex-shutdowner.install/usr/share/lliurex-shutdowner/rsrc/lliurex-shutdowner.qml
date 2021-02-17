import QtQuick 2.6
import QtQuick.Controls 2.6
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2

ApplicationWindow {
	visible: true
	title: "LliureX Shutdowner"
	property int margin: 1
	width: mainLayout.implicitWidth + 2 * margin
	height: mainLayout.implicitHeight + 2 * margin
	minimumWidth: mainLayout.Layout.minimumWidth + 2 * margin
	minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin
	maximumWidth: mainLayout.Layout.maximumWidth + 2 * margin
	maximumHeight: mainLayout.Layout.maximumHeight + 2 * margin
	Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }
     onClosing: {
     	if (shutBridge.closed(true))
     		removeConnection(),
      		close.accepted=true,
        	console.log("Cleanup done, can close!");
        else
        	close.accepted=false;	
    }


    ColumnLayout {
    	id: mainLayout
    	anchors.fill: parent
    	anchors.margins: margin
    	Layout.minimumWidth:600	
    	Layout.maximumWidth:600
    	Layout.minimumHeight:shutBridge.isStandAlone? 370:485
    	Layout.maximumHeight:shutBridge.isStandAlone? 370:485

    	RowLayout {
    		id: bannerBox
        	Layout.alignment:Qt.AlignTop
        	Layout.minimumHeight:120
        	Layout.maximumHeight:120
        	Image{
        		id:banner
        		source: "/usr/share/lliurex-shutdowner/rsrc/lliurex-shutdowner.png"
       		}
       	}
        
       

	    StackLayout {
	      	id: stackLayout
	        currentIndex:1
	        implicitWidth: 600
	        Layout.bottomMargin: 10
	       	Layout.alignment:Qt.AlignHCenter
	       	Layout.leftMargin:10
	       	Layout.rightMargin:10
	       	Layout.fillHeight: true

	       	GridLayout{
	       		id: loadGrid
	       		rows: 4
	       		flow: GridLayout.TopToBottom
	       		Layout.topMargin: 10
	       		Layout.bottomMargin: 10

	       		Item {
	       			Layout.fillWidth: true
	       			Layout.topMargin: (mainLayout.Layout.minimumHeight-bannerBox.Layout.minimumHeight)/2-2*loadGrid.Layout.topMargin
    			}

    			RowLayout {
    				Layout.fillWidth: true
	               	Layout.alignment:Qt.AlignHCenter
           			Text{
           				id:loadtext
           				text:i18nd("lliurex-shutdowner", "Loading information. Wait a moment...")
           				font.family: "Quattrocento Sans Bold"
           				font.pointSize: 10
           				color:"black"
           				Layout.alignment:Qt.AlignCenter
           			}
           		}
           		RowLayout {
    				Layout.fillWidth: true
	               	Layout.alignment:Qt.AlignHCenter
    				Text {
    					id:timer
						text:shutBridge.initFinish
						visible:false
	               		Layout.alignment:Qt.AlignHCenter
						font.family: "Quattrocento Sans Bold"
			   			font.pointSize: 10
			   			onTextChanged:{
			   				stackLayout.currentIndex=shutBridge.initFinish? 1:0
						} 
					} 
				}
			}			  

          	GridLayout {
           		id: mainGrid
		        rows:2
		        flow: GridLayout.TopToBottom
		        Layout.topMargin: 10
		        Layout.bottomMargin: 10
		        rowSpacing:5

		        GroupBox {
		        	id: clockBox
		            Layout.fillWidth: true
		            background: Rectangle {
		            	color:"white"
		            	border.color: "lightGray"
         			}
         			Layout.alignment:Qt.AlignHCenter


		           	GridLayout {
		           		id: shutGrid
			            rows:5
			            flow: GridLayout.TopToBottom
			            Layout.topMargin: 10
			            Layout.bottomMargin: 10
			            rowSpacing:5
			            anchors.fill:parent

			            RowLayout {
			            	id: automaticLayout
			            	Layout.topMargin: 5

			                Text {
			                	id:textMessage
			                	text:!shutBridge.isStandAlone? i18nd("lliurex-shutdowner","Automatic client shutdown"):i18nd("lliurex-shutdowner","Automatic shutdown")
					    		font.family: "Quattrocento Sans Bold"
					   			font.pointSize: 10
					    		color: "black"
					    		Layout.alignment:Qt.AlignVCenter
					    		Layout.leftMargin:5

							}   

				        	Switch {
				        		id:toggleswitch
				        		checked: shutBridge.isCronEnabled
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
					        		shutBridge.getCronSwitchValue(toggleswitch.checked);
					        		if (toggleswitch.checked)
						        		clockLayout.enabled=true,
						        		daysLayout.enabled=true,
						        		serverLayout.enabled=true,
						        		clientBox.enabled=true;
						        	else
						        		clockLayout.enabled=false,
						        		daysLayout.enabled=false,
						        		serverLayout.enabled=false,
						        		clientBox.enabled=false;
					        		
						       	}
										
							}
						}
				               	
				        Rectangle {
				           	Layout.leftMargin: 5
				            Layout.rightMargin:5
				            Layout.bottomMargin: 10
						  	Layout.preferredWidth: 555
							height: 1
							border.color: "black"
							border.width: 5
							radius: 10
						}

						RowLayout {
				        	id:clockLayout
				        	enabled:shutBridge.isCronEnabled
				           	Layout.leftMargin: 5
				            Layout.rightMargin:5
				            Layout.bottomMargin: 10
				           	Layout.fillWidth: true
				           	Layout.alignment:Qt.AlignHCenter
				               	
				          	Item {
				        		Layout.fillWidth: true
				        		width:200
			    			}
				               	
				            Rectangle {
				             	anchors.topMargin: 4
							    Layout.fillWidth: true
					           	Layout.alignment:Qt.AlignVCenter
							    height: 100
							    width: 80
							    color:"transparent"
								       
							    ListView {
							    	id: hour
							        highlightFollowsCurrentItem:true
							        maximumFlickVelocity:1000
							        anchors.fill: parent
							        highlightRangeMode: ListView.StrictlyEnforceRange
							        preferredHighlightBegin: height/10
							        preferredHighlightEnd: height/10
							        clip: true
							        model: 24
							        focus:true
							     	currentIndex:shutBridge.initClock[0]
							      
							       onCurrentIndexChanged:{
								    	shutBridge.getClokValues(["H",hour.currentIndex]);
								       
								    }
								          
								    delegate: Text {
								    	font.pixelSize: 60;
								        color: clockLayout.enabled? "#3daee9":"#87cefa"
								        text: index<10?"0"+index:index
										anchors.horizontalCenter: parent ? parent.horizontalCenter : undefined
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
								        }
								    }
								}
							}
				                	
					        Text{
					          	Layout.fillWidth: true
					          	Layout.alignment:Qt.AlignVCenter
						        font.pixelSize:60;
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
								ListView {
									id: minute
								    highlightFollowsCurrentItem:true
								    maximumFlickVelocity:1000
								    anchors.fill: parent
								    highlightRangeMode: ListView.StrictlyEnforceRange
								    preferredHighlightBegin: height/10
								    preferredHighlightEnd: height/10
								    clip: true
								    model: 60
								    focus:true
								  	currentIndex:shutBridge.initClock[1]

								    onCurrentIndexChanged: {
								    	shutBridge.getClokValues(["M",minute.currentIndex]);
								     }
								            
								     delegate: Text {
								     	font.pixelSize: 60
								        color: clockLayout.enabled? "#3daee9":"#87cefa"
								        text: index<10?"0"+index:index	
										anchors.horizontalCenter: parent ? parent.horizontalCenter : undefined
					                    MouseArea {
					                      	id: mouseAreaMinute
								             anchors.fill: parent
								             hoverEnabled: true
								             onEntered: {
								        	   	parent.color="#add8e6"
								             }
								             onExited: {
								               	parent.color="#3daee9"
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
							enabled:shutBridge.isCronEnabled
					        Layout.alignment:Qt.AlignHCenter
				            Layout.fillWidth: true
				            Layout.bottomMargin: 10
				            spacing:8
				                
				            Button {
				              	id:mondaybtn
								checkable: true
								checked:shutBridge.initWeekDays[0]
								text:i18nd("lliurex-shutdowner","Monday")
								Layout.preferredWidth: 100
								Layout.preferredHeight: 40
								palette.button:{
									if (daysLayout.enabled)
										mondaybtn.checked? "#3daee9": "#f0f1f2";
									else
										mondaybtn.checked? "#87cefa":"#e4e5e7";		
								}	
								palette.buttonText:{
									if (daysLayout.enabled)
										mondaybtn.checked? "white": "black";
									else
										mondaybtn.checked? "white": "#b9babc";
									
								}	
								focusPolicy: Qt.NoFocus
								onClicked: {
									shutBridge.getWeekValues(["MO",mondaybtn.checked]);
								}
							}
									
							Button {
				               	id:tuesdaybtn
								checkable: true
								checked:shutBridge.initWeekDays[1]
								text:i18nd("lliurex-shutdowner","Tuesday")
								Layout.preferredWidth: 100
								Layout.preferredHeight: 40
								palette.button:{
									if (daysLayout.enabled)
										tuesdaybtn.checked? "#3daee9": "#f0f1f2";
									else
										tuesdaybtn.checked? "#87cefa":"#e4e5e7";		
								}	
								palette.buttonText:{
									if (daysLayout.enabled)
										tuesdaybtn.checked? "white": "black";
									else
										tuesdaybtn.checked? "white": "#b9babc";
									
								}	
								focusPolicy: Qt.NoFocus
								onClicked: {
									shutBridge.getWeekValues(["TU",tuesdaybtn.checked]);
								}

							}
							
							Button {
								id:wednesdaybtn
								checkable: true
								checked:shutBridge.initWeekDays[2]
								text:i18nd("lliurex-shutdowner","Wednesday")
								Layout.preferredWidth: 100
								Layout.preferredHeight: 40
								palette.button:{
									if (daysLayout.enabled)
										wednesdaybtn.checked? "#3daee9": "#f0f1f2";
									else
										wednesdaybtn.checked? "#87cefa":"#e4e5e7";		
								}	
								palette.buttonText:{
									if (daysLayout.enabled)
										wednesdaybtn.checked? "white": "black";
									else
										wednesdaybtn.checked? "white": "#b9babc";
									
								}	
								focusPolicy: Qt.NoFocus
								onClicked: {
									shutBridge.getWeekValues(["WE",wednesdaybtn.checked]);
								}

							}
									
							Button {
								id:thursdaybtn
								checkable: true
								checked:shutBridge.initWeekDays[3]
								text:i18nd("lliurex-shutdowner","Thursday")
								Layout.preferredWidth: 100
								Layout.preferredHeight: 40
								palette.button:{
									if (daysLayout.enabled)
										thursdaybtn.checked? "#3daee9": "#f0f1f2";
									else
										thursdaybtn.checked? "#87cefa":"#e4e5e7";		
								}	
								palette.buttonText:{
									if (daysLayout.enabled)
										thursdaybtn.checked? "white": "black";
									else
										thursdaybtn.checked? "white": "#b9babc";
									
								}	
								focusPolicy: Qt.NoFocus
								onClicked: {
									shutBridge.getWeekValues(["TH",thursdaybtn.checked]);
								}
							}
								
							Button {
								id:fridaybtn
								checkable: true
								checked:shutBridge.initWeekDays[4]
								text:i18nd("lliurex-shutdowner","Friday")
								Layout.preferredWidth: 100
								Layout.preferredHeight: 40
								palette.button:{
									if (daysLayout.enabled)
										fridaybtn.checked? "#3daee9": "#f0f1f2";
									else
										fridaybtn.checked? "#87cefa":"#e4e5e7";		
								}	
								palette.buttonText:{
									if (daysLayout.enabled)
										fridaybtn.checked? "white": "black";
									else
										fridaybtn.checked? "white": "#b9babc";
									
								}	
								focusPolicy: Qt.NoFocus
								onClicked: {
									shutBridge.getWeekValues(["FR",fridaybtn.checked]);
								}
							}		
						}
							
						RowLayout {
							id: serverLayout
					        Layout.alignment:Qt.AlignHCenter
				            Layout.fillWidth: true
				           	Layout.bottomMargin: 10
				           	enabled:shutBridge.isCronEnabled
				           	visible:!shutBridge.isStandAlone
				           	spacing:15
				            CheckBox {
				            	id:serverShut
				             	checked:shutBridge.initServerShut
				               	text:i18nd("lliurex-shutdowner","Shutdown server as well (2 minutes later)")
				               	font.pointSize: 10
				               	focusPolicy: Qt.NoFocus
				               	onToggled:{
				               		shutBridge.getServerShut(serverShut.checked)
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
			      	visible:!shutBridge.isStandAlone
			      	enabled:shutBridge.isCronEnabled
		            background: Rectangle {
		            	color:"white"
		            	border.color: "lightGray"
         			}


					RowLayout {
						id: clientLayout
					    Layout.topMargin: 10
		           		Layout.bottomMargin: 10
						anchors.fill:parent

					    Text {
					       	id:clientText
					       	text:i18nd("lliurex-shutdowner","Currently detected clients: ")
					        font.family: "Quattrocento Sans Bold"
					  		font.pointSize: 10
						   	color: "black"
						  	Layout.alignment:Qt.AlignVCenter
        					Layout.minimumWidth:10
        					Layout.leftMargin:5

				        }

				        Text {
					       	id:numberclientText
					       	text:shutBridge.detectedClients
					        font.family: "Quattrocento Sans Bold"
							font.pointSize: 10
						  	color: "black"
        					Layout.maximumWidth:240
        					Layout.fillWidth: true
	  	
				        }

				        Button {
				        	id:shutnowbtn
				      		display:AbstractButton.TextBesideIcon
							icon.name:"system-shutdown.svg"
				            text:i18nd("lliurex-shutdowner","Shutdown clients now")
				        	Layout.preferredHeight: 40
				    		Layout.topMargin: 5
		           			Layout.bottomMargin: 5
		           			Layout.rightMargin:5
		           			onClicked:{
		           				shutBridge.shutdownClientsNow()
		           			}

		              	}
		             }      	
				}
			}
		}
	}

	function removeConnection() {
			timer.text="",
     		textMessage.text="",
			toggleswitch.checked=false,
			mainLayout.Layout.minimumHeight=485,			
			mainLayout.Layout.maximumHeight=485,
			clockLayout.enabled=false,
			hour.currentIndex="0",
			minute.currentIndex="0",
			daysLayout.enabled=false,
			mondaybtn.checked=false,
			tuesdaybtn.checked=false,
			wednesdaybtn.checked=false,
			thursdaybtn.checked=false,
			fridaybtn.checked=false,
			serverLayout.visible=false,
			serverLayout.enabled=false,
			serverShut.checked=false,
			clientBox.visible=true,
			clientBox.enabled=false,
			numberclientText.text="0";
        
    }
	
}	    
