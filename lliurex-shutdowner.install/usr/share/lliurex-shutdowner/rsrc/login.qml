import QtQuick 2.6

import Edupals.N4D.Agent 1.0 as N4DAgent


Rectangle {
    width: 400
    height: 250
    anchors.centerIn: parent
    color: "#e9e9e9"


    N4DAgent.Login
    {
        showAddress:!tunnel.standAlone
        address:!showAddress?'localhost':'server'
        showCancel: false
        inGroups:["sudo","admins","teachers"]
        
        anchors.centerIn: parent
        
        onLogged: {
            tunnel.on_ticket(ticket),
            showAdress=false;


        }
    }
}
