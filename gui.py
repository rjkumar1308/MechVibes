import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout,QHBoxLayout, QWidget, QSlider, QSystemTrayIcon, QAction, QMenu, qApp
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from resource_path import resource_path

class GUI():
    def __init__(self, volume):
        super().__init__()
        app = QApplication(sys.argv)
        self.widget = QWidget()
        self.volume = volume
        self.widget.changeEvent = self.changeEvent
        self.initUI()
        os._exit(app.exec_())

    
    def initUI(self):
        self.widget.setStyleSheet("background-color:white")
        self.setTitle()
        self.setIcon()
        self.setHeading()
        self.setVolume()
        self.setTrayIcon()
        self.widget.hide()

    def setIcon(self):
        self.pathOfIcon = resource_path("icon.png")
        self.widget.setWindowIcon(QIcon(self.pathOfIcon))
    
    def setTitle(self):
        self.widget.setGeometry(300, 300, 380, 550)
        self.widget.setWindowTitle('MechVibes')

    def setHeading(self):
        l1 = QLabel("MechVibes")
        l1.setStyleSheet("border: 2px solid #333;"
                            "border-radius: 5px;"
                            "font-size: 25px;"
                            "font-weight: bold;"
                            "color:#333;"
                            "margin: 25px 25px 25px 25px;"
                            "text-align: center;"
                            )
        l1.setAlignment(QtCore.Qt.AlignCenter)
        l1.setFixedSize(250, 130)
        hbox = QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        hbox.addWidget(l1)
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(hbox)
        self.vbox.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.widget.setLayout(self.vbox)
    
    def setVolume(self):
        l1 = QLabel("Volume")
        l1.setStyleSheet("font-size: 16px;"
                            "color:grey;"
                            "margin: 25px 0px 25px 30px;"
                            )
        hbox = QHBoxLayout()
        hbox.addWidget(l1)

        sld = QSlider(QtCore.Qt.Horizontal, self.widget)
        sld.setRange(0, 100)
        sld.setFocusPolicy(QtCore.Qt.NoFocus)
        sld.setPageStep(5)
        sld.setValue(self.volume.get())
        sld.setStyleSheet("""QSlider::groove:horizontal { 
                            background-color: #d3d3d3;
                            border: 0px solid #424242; 
                            height: 5px; 
                            border-radius: 2px;
                            margin-right:30px;
                            margin-left:20px;
                        }

                        QSlider::handle:horizontal { 
                            background-color: #FF5433; 
                            border: 2px solid #FF5433; 
                            width: 16px; 
                            height: 20px; 
                            line-height: 20px; 
                            margin-top: -8px; 
                            margin-bottom: -8px; 
                            border-radius: 10px; 
                        }

                        QSlider::handle:horizontal:hover { 
                            border-radius: 10px;
                            background-color: #FF3333; 
                            border: 2px solid #FF3333;
                        }""")

        sld.valueChanged.connect(self.updateLabel)

        self.label = QLabel(str(self.volume.get()))
        self.label.setStyleSheet("font-size: 16px;"
                            "color:grey;"
                            "margin: 25px 0px 25px 0px;"
                            )
        self.label.setMinimumWidth(40)

        hbox.addWidget(self.label)
        hbox.addWidget(sld)

        self.vbox.addLayout(hbox)
    
    def updateLabel(self, value):
        self.label.setText(str(value))
        self.volume.changeVolume(int(value))
        fo = open(resource_path("initial_data.txt"), "w")
        fo.write(str(value))
        fo.close()
    
    def setTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(self.widget)
        self.tray_icon.setIcon(QIcon(self.pathOfIcon))
        show_action = QAction("Show", self.widget)
        quit_action = QAction("Exit", self.widget)
        show_action.triggered.connect(self.widget.show)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.activated.connect(self.focus)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def focus(self, event):
        self.widget.showNormal()
        self.widget.raise_()
        self.widget.activateWindow()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.widget.windowState() & QtCore.Qt.WindowMinimized:
                self.widget.hide()