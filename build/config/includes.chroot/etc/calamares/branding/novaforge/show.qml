import QtQuick 2.15
import QtQuick.Controls 2.15
import calamares.slideshow 1.0

Presentation {
    id: presentation
    width: 600
    height: 400

    Timer {
        id: slideTimer
        interval: 10000
        running: presentation.activatedInCalamares
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }

    Slide {
        id: slide1
        anchors.fill: parent
        
        Rectangle {
            anchors.fill: parent
            color: "#0a0a1a"
            
            Rectangle {
                width: parent.width - 20
                height: parent.height - 20
                anchors.centerIn: parent
                color: "#11111b"
                border.color: "#7c3aed"
                border.width: 1
                radius: 12
                
                Column {
                    anchors.centerIn: parent
                    spacing: 16
                    width: parent.width - 60
                    
                    Text {
                        text: "🔥  NovaForge Linux"
                        color: "#00e5ff"
                        font.family: "Inter"
                        font.pixelSize: 28
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        width: parent.width
                    }
                    
                    Text {
                        text: "Forge Your Universe"
                        color: "#7f849c"
                        font.family: "Inter"
                        font.pixelSize: 16
                        horizontalAlignment: Text.AlignHCenter
                        width: parent.width
                    }
                    
                    Text {
                        text: "Welcome to a premium operating system crafted for developers, creators, gamers, and AI engineers. Thank you for choosing NovaForge Linux!"
                        color: "#cdd6f4"
                        font.family: "Inter"
                        font.pixelSize: 13
                        wrapMode: Text.WordWrap
                        horizontalAlignment: Text.AlignHCenter
                        width: parent.width
                    }
                }
            }
        }
    }

    Slide {
        id: slide2
        anchors.fill: parent
        
        Rectangle {
            anchors.fill: parent
            color: "#0a0a1a"
            
            Rectangle {
                width: parent.width - 20
                height: parent.height - 20
                anchors.centerIn: parent
                color: "#11111b"
                border.color: "#00e5ff"
                border.width: 1
                radius: 12
                
                Column {
                    anchors.centerIn: parent
                    spacing: 16
                    width: parent.width - 60
                    
                    Text {
                        text: "⚡  Optimal Gaming Mode"
                        color: "#00e5ff"
                        font.family: "Inter"
                        font.pixelSize: 22
                        font.bold: true
                        width: parent.width
                    }
                    
                    Text {
                        text: "• GameMode & MangoHud pre-configured for instant overlay metrics.\n• Wine, Proton, Lutris, and Steam ready out of the box.\n• Performance Governor automatically tunes CPU for high frame rates.\n• Low-latency kernel scheduler tweaks for smooth gaming."
                        color: "#cdd6f4"
                        font.family: "Inter"
                        font.pixelSize: 13
                        lineHeight: 1.4
                        wrapMode: Text.WordWrap
                        width: parent.width
                    }
                }
            }
        }
    }

    Slide {
        id: slide3
        anchors.fill: parent
        
        Rectangle {
            anchors.fill: parent
            color: "#0a0a1a"
            
            Rectangle {
                width: parent.width - 20
                height: parent.height - 20
                anchors.centerIn: parent
                color: "#11111b"
                border.color: "#7c3aed"
                border.width: 1
                radius: 12
                
                Column {
                    anchors.centerIn: parent
                    spacing: 16
                    width: parent.width - 60
                    
                    Text {
                        text: "💻  Professional Developer Stack"
                        color: "#7c3aed"
                        font.family: "Inter"
                        font.pixelSize: 22
                        font.bold: true
                        width: parent.width
                    }
                    
                    Text {
                        text: "• Visual Studio Code and Git preloaded with premium settings.\n• Docker Engine, Node.js, and Python 3 preconfigured.\n• Custom terminal profile in Konsole with JetBrains Mono font.\n• Advanced profile governor swaps system limits for heavy coding."
                        color: "#cdd6f4"
                        font.family: "Inter"
                        font.pixelSize: 13
                        lineHeight: 1.4
                        wrapMode: Text.WordWrap
                        width: parent.width
                    }
                }
            }
        }
    }

    Slide {
        id: slide4
        anchors.fill: parent
        
        Rectangle {
            anchors.fill: parent
            color: "#0a0a1a"
            
            Rectangle {
                width: parent.width - 20
                height: parent.height - 20
                anchors.centerIn: parent
                color: "#11111b"
                border.color: "#00e5ff"
                border.width: 1
                radius: 12
                
                Column {
                    anchors.centerIn: parent
                    spacing: 16
                    width: parent.width - 60
                    
                    Text {
                        text: "🤖  Offline AI Workspace"
                        color: "#00e5ff"
                        font.family: "Inter"
                        font.pixelSize: 22
                        font.bold: true
                        width: parent.width
                    }
                    
                    Text {
                        text: "• Integrated with Ollama for hosting local models.\n• Download LLMs (Llama 3, Mistral, Phi-3) using the Control Center.\n• Interactive terminal tool 'novaforge-chat' for instant offline chats.\n• Full CUDA stack guides and AI development dependencies included."
                        color: "#cdd6f4"
                        font.family: "Inter"
                        font.pixelSize: 13
                        lineHeight: 1.4
                        wrapMode: Text.WordWrap
                        width: parent.width
                    }
                }
            }
        }
    }
}
