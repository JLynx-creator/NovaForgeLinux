// ============================================================
// NovaForge Linux — KDE Splash Screen
// ============================================================

import QtQuick 2.15

Rectangle {
    id: root
    color: "#0a0a1a"

    property int stage: 0

    onStageChanged: {
        if (stage === 1) {
            logoFadeIn.start();
        }
        if (stage === 5) {
            fadeOut.start();
        }
    }

    // Logo
    Image {
        id: logo
        source: "images/novaforge-logo.png"
        anchors.centerIn: parent
        sourceSize.width: 200
        sourceSize.height: 200
        opacity: 0

        NumberAnimation on opacity {
            id: logoFadeIn
            from: 0
            to: 1
            duration: 600
            easing.type: Easing.OutCubic
            running: false
        }
    }

    // Branding text
    Text {
        id: brandText
        text: "NovaForge Linux"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: logo.bottom
        anchors.topMargin: 20
        font.family: "Inter"
        font.pixelSize: 24
        font.weight: Font.Light
        color: "#cdd6f4"
        opacity: logo.opacity
    }

    // Loading bar
    Rectangle {
        id: progressBg
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: parent.height * 0.15
        width: 200
        height: 3
        radius: 2
        color: "#1e1e2e"
        opacity: logo.opacity

        Rectangle {
            id: progressBar
            anchors.left: parent.left
            height: parent.height
            radius: 2
            color: "#00e5ff"
            width: parent.width * (root.stage / 6.0)

            Behavior on width {
                NumberAnimation { duration: 300; easing.type: Easing.OutCubic }
            }
        }
    }

    // Fade out
    NumberAnimation {
        id: fadeOut
        target: root
        property: "opacity"
        from: 1
        to: 0
        duration: 400
        easing.type: Easing.InCubic
    }
}
