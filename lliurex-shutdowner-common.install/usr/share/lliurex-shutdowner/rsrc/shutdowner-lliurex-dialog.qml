import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    title: "LliureX Shutdowner"
    color: "#eff0f1"

    width: 610
    height: btnBox.visible ? 205 : 160
    minimumWidth: 610
    maximumWidth: 610
    minimumHeight: height
    maximumHeight: height

    Component.onCompleted: {
        window.x = (screen.width - window.width) / 2
        window.y = (screen.height - window.height) / 2
    }

    onClosing: (close) => {
        if (bridge.closed(true)) {
            close.accepted = true;
        } else {
            close.accepted = false;
        }
    }

    GridLayout {
        id: grid
        anchors.fill: parent
        anchors.margins: 10
        rows: 3
        columns: 2
        rowSpacing: 10
        columnSpacing: 10

        Item {
            Layout.preferredWidth: 60
            Layout.preferredHeight: 60
            Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter

            Image {
                source: "file:///usr/share/icons/breeze/status/64/dialog-warning.svg"
                anchors.centerIn: parent
                fillMode: Image.PreserveAspectFit
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: 60

            Text {
                id: warningText
                text: bridge.translateMsg.msg
                font.pointSize: 11
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        Item {
            Layout.columnSpan: 2
            Layout.fillWidth: true
            Layout.preferredHeight: 70

            Text {
                id: countDown
                font.pointSize: 50
                anchors.centerIn: parent
                text: bridge.timeRemaining.time
                color: bridge.timeRemaining.color
            }
        }

        Item {
            id: btnBox
            visible: bridge.visibleCancelBtn
            Layout.columnSpan: 2
            Layout.fillWidth: true
            Layout.preferredHeight: 40

            Button {
                id: cancelBtn
                height: 35
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                display: AbstractButton.TextBesideIcon
                icon.source: "file:///usr/share/icons/breeze/actions/16/dialog-cancel.svg"
                icon.width: 16
                icon.height: 16
                text: bridge.translateMsg.btnMsg

                onClicked: {
                    bridge.cancelClicked();
                    removePropertiesConnect();
                }

                background: Rectangle {
                    implicitWidth: 100
                    implicitHeight: 35
                    color: cancelBtn.pressed ? "#94cfeb" : "#f0f1f2"
                    border.color: cancelBtn.hovered ? "#3daee9" : "#b3b5b6"
                    border.width: 1
                    radius: 2
                }
            }
        }
    }
}
