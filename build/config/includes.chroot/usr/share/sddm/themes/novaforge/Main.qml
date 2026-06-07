// ============================================================
// NovaForge Linux — SDDM Login Theme
// ============================================================
// Modern glassmorphism login screen with:
//   - Blurred background image
//   - Frosted glass login card
//   - Cyan neon accent border glow
//   - Circular user avatar
//   - Clock display
//   - Session and power controls
// ============================================================

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15
import SddmComponents 2.0

Rectangle {
    id: root
    width: Screen.width
    height: Screen.height
    color: "#0a0a1a"

    // ── Properties ────────────────────────────────────────
    property color accentColor: "#00e5ff"
    property color bgDark: "#11111b"
    property color bgCard: "#1e1e2e"
    property color textPrimary: "#cdd6f4"
    property color textSecondary: "#7f849c"
    property color borderColor: "#313244"

    // ── Background Image ──────────────────────────────────
    Image {
        id: backgroundImage
        source: "background.jpg"
        anchors.fill: parent
        fillMode: Image.PreserveAspectCrop
        smooth: true
        visible: false
    }

    // Blur effect on background
    FastBlur {
        id: blurredBg
        anchors.fill: parent
        source: backgroundImage
        radius: 48
    }

    // Dark overlay
    Rectangle {
        anchors.fill: parent
        color: "#000000"
        opacity: 0.45
    }

    // ── Clock (Top Center) ────────────────────────────────
    ColumnLayout {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: parent.height * 0.08
        spacing: 4

        Text {
            id: timeLabel
            Layout.alignment: Qt.AlignHCenter
            font.family: "Inter"
            font.pixelSize: 64
            font.weight: Font.Light
            color: textPrimary
            text: Qt.formatTime(new Date(), "HH:mm")
        }

        Text {
            id: dateLabel
            Layout.alignment: Qt.AlignHCenter
            font.family: "Inter"
            font.pixelSize: 16
            font.weight: Font.Normal
            color: textSecondary
            text: Qt.formatDate(new Date(), "dddd, MMMM d, yyyy")
        }
    }

    // Clock timer
    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: {
            timeLabel.text = Qt.formatTime(new Date(), "HH:mm")
            dateLabel.text = Qt.formatDate(new Date(), "dddd, MMMM d, yyyy")
        }
    }

    // ── Login Card (Center) ───────────────────────────────
    Rectangle {
        id: loginCard
        anchors.centerIn: parent
        width: 380
        height: 460
        radius: 20
        color: Qt.rgba(bgCard.r, bgCard.g, bgCard.b, 0.75)
        border.color: Qt.rgba(accentColor.r, accentColor.g, accentColor.b, 0.3)
        border.width: 1

        // Subtle glow effect
        layer.enabled: true
        layer.effect: DropShadow {
            transparentBorder: true
            horizontalOffset: 0
            verticalOffset: 0
            radius: 30
            samples: 61
            color: Qt.rgba(accentColor.r, accentColor.g, accentColor.b, 0.15)
        }

        // Card entrance animation
        scale: 0.95
        opacity: 0

        Component.onCompleted: {
            cardEntrance.start()
        }

        ParallelAnimation {
            id: cardEntrance
            NumberAnimation {
                target: loginCard
                property: "scale"
                from: 0.95
                to: 1.0
                duration: 400
                easing.type: Easing.OutCubic
            }
            NumberAnimation {
                target: loginCard
                property: "opacity"
                from: 0
                to: 1
                duration: 400
                easing.type: Easing.OutCubic
            }
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 36
            spacing: 16

            // ── User Avatar ───────────────────────────────
            Item {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 96
                Layout.preferredHeight: 96

                Rectangle {
                    anchors.fill: parent
                    radius: 48
                    color: bgDark
                    border.color: accentColor
                    border.width: 2

                    Text {
                        anchors.centerIn: parent
                        text: "👤"
                        font.pixelSize: 40
                    }
                }
            }

            // ── Username Label ────────────────────────────
            Text {
                Layout.alignment: Qt.AlignHCenter
                text: userModel.lastUser || "User"
                font.family: "Inter"
                font.pixelSize: 18
                font.weight: Font.DemiBold
                color: textPrimary
            }

            // Spacer
            Item { Layout.preferredHeight: 8 }

            // ── Username Field ────────────────────────────
            TextField {
                id: userField
                Layout.fillWidth: true
                Layout.preferredHeight: 44
                placeholderText: "Username"
                text: userModel.lastUser
                font.family: "Inter"
                font.pixelSize: 14
                color: textPrimary
                selectionColor: accentColor
                selectedTextColor: bgDark

                background: Rectangle {
                    radius: 10
                    color: bgDark
                    border.color: userField.activeFocus ? accentColor : borderColor
                    border.width: userField.activeFocus ? 2 : 1

                    Behavior on border.color {
                        ColorAnimation { duration: 200 }
                    }
                }

                Keys.onReturnPressed: passwordField.forceActiveFocus()
            }

            // ── Password Field ────────────────────────────
            TextField {
                id: passwordField
                Layout.fillWidth: true
                Layout.preferredHeight: 44
                placeholderText: "Password"
                echoMode: TextInput.Password
                font.family: "Inter"
                font.pixelSize: 14
                color: textPrimary
                selectionColor: accentColor
                selectedTextColor: bgDark

                background: Rectangle {
                    radius: 10
                    color: bgDark
                    border.color: passwordField.activeFocus ? accentColor : borderColor
                    border.width: passwordField.activeFocus ? 2 : 1

                    Behavior on border.color {
                        ColorAnimation { duration: 200 }
                    }
                }

                Keys.onReturnPressed: sddm.login(userField.text, passwordField.text, sessionModel.lastIndex)
            }

            // ── Error Message ─────────────────────────────
            Text {
                id: errorMessage
                Layout.alignment: Qt.AlignHCenter
                font.family: "Inter"
                font.pixelSize: 12
                color: "#f38ba8"
                text: ""
                visible: text !== ""
            }

            // ── Login Button ──────────────────────────────
            Button {
                id: loginButton
                Layout.fillWidth: true
                Layout.preferredHeight: 44
                text: "Login"
                font.family: "Inter"
                font.pixelSize: 15
                font.weight: Font.DemiBold

                contentItem: Text {
                    text: loginButton.text
                    font: loginButton.font
                    color: bgDark
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    radius: 10
                    color: loginButton.hovered ? Qt.lighter(accentColor, 1.1) : accentColor

                    Behavior on color {
                        ColorAnimation { duration: 150 }
                    }
                }

                onClicked: sddm.login(userField.text, passwordField.text, sessionModel.lastIndex)
            }

            // ── Session Selector ──────────────────────────
            ComboBox {
                id: sessionSelector
                Layout.fillWidth: true
                Layout.preferredHeight: 36
                model: sessionModel
                currentIndex: sessionModel.lastIndex
                textRole: "name"
                font.family: "Inter"
                font.pixelSize: 12

                background: Rectangle {
                    radius: 8
                    color: bgDark
                    border.color: borderColor
                    border.width: 1
                }

                contentItem: Text {
                    text: sessionSelector.displayText
                    font: sessionSelector.font
                    color: textSecondary
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: 12
                }
            }
        }
    }

    // ── Power Buttons (Bottom Right) ──────────────────────
    Row {
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 24
        spacing: 12

        // Suspend
        Rectangle {
            width: 40
            height: 40
            radius: 20
            color: mouseAreaSuspend.containsMouse ? Qt.rgba(1, 1, 1, 0.1) : "transparent"
            Text {
                anchors.centerIn: parent
                text: "⏸"
                font.pixelSize: 18
                color: textSecondary
            }
            MouseArea {
                id: mouseAreaSuspend
                anchors.fill: parent
                hoverEnabled: true
                onClicked: sddm.suspend()
            }
        }

        // Restart
        Rectangle {
            width: 40
            height: 40
            radius: 20
            color: mouseAreaRestart.containsMouse ? Qt.rgba(1, 1, 1, 0.1) : "transparent"
            Text {
                anchors.centerIn: parent
                text: "🔄"
                font.pixelSize: 18
                color: textSecondary
            }
            MouseArea {
                id: mouseAreaRestart
                anchors.fill: parent
                hoverEnabled: true
                onClicked: sddm.reboot()
            }
        }

        // Power Off
        Rectangle {
            width: 40
            height: 40
            radius: 20
            color: mouseAreaPower.containsMouse ? Qt.rgba(1, 1, 1, 0.1) : "transparent"
            Text {
                anchors.centerIn: parent
                text: "⏻"
                font.pixelSize: 20
                color: "#f38ba8"
            }
            MouseArea {
                id: mouseAreaPower
                anchors.fill: parent
                hoverEnabled: true
                onClicked: sddm.powerOff()
            }
        }
    }

    // ── Login Failure Handler ─────────────────────────────
    Connections {
        target: sddm
        function onLoginFailed() {
            errorMessage.text = "Login failed. Please try again."
            passwordField.text = ""
            passwordField.forceActiveFocus()

            // Shake animation
            shakeAnimation.start()
        }
    }

    SequentialAnimation {
        id: shakeAnimation
        NumberAnimation { target: loginCard; property: "x"; to: loginCard.x - 10; duration: 50 }
        NumberAnimation { target: loginCard; property: "x"; to: loginCard.x + 10; duration: 50 }
        NumberAnimation { target: loginCard; property: "x"; to: loginCard.x - 5; duration: 50 }
        NumberAnimation { target: loginCard; property: "x"; to: loginCard.x + 5; duration: 50 }
        NumberAnimation { target: loginCard; property: "x"; to: loginCard.x; duration: 50 }
    }

    // ── Focus on load ─────────────────────────────────────
    Component.onCompleted: {
        if (userField.text !== "") {
            passwordField.forceActiveFocus()
        } else {
            userField.forceActiveFocus()
        }
    }
}
