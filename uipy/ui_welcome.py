from PyQt5 import QtCore, QtWidgets


class Ui_Welcome(object):
    def setupUi(self, Welcome):
        Welcome.setObjectName("Welcome")
        Welcome.resize(460, 390)
        Welcome.setMinimumSize(QtCore.QSize(460, 390))
        Welcome.setMaximumSize(QtCore.QSize(460, 390))

        Welcome.setStyleSheet("#frame{border-image: url(\'./1.png\');}")
        self.frame = QtWidgets.QFrame(Welcome)
        self.frame.setGeometry(QtCore.QRect(-10, -10, 480, 400))
        self.frame.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.agree = QtWidgets.QRadioButton(self.frame)
        self.agree.setGeometry(QtCore.QRect(160, 260, 161, 19))
        self.agree.setObjectName("agree")
        self.start = QtWidgets.QPushButton(self.frame)
        self.start.setGeometry(QtCore.QRect(180, 300, 121, 31))
        self.start.setObjectName("start")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setGeometry(QtCore.QRect(90, 40, 311, 201))
        self.textBrowser.setStyleSheet("background-color: transparent;\n"
                                       "font-family: 微软雅黑;\n"
                                       "font-size: 12pt;\n"
                                       "")
        self.textBrowser.setObjectName("textBrowser")
        self.retranslateUi(Welcome)
        QtCore.QMetaObject.connectSlotsByName(Welcome)

    def retranslateUi(self, Welcome):
        _translate = QtCore.QCoreApplication.translate
        Welcome.setWindowTitle(_translate("Welcome", "Welcome"))
        self.agree.setText(_translate("Welcome", "同意开始使用本平台"))
        self.start.setText(_translate("Welcome", "开始使用"))
        self.textBrowser.setHtml(_translate("Welcome",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'隶书\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-weight:600;\">使用本平台前</span></p>\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-weight:600;\">请先阅读以下注意事项:</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';\">1.平台目前支持的生理信号有：</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';\">心电图（ECG）、肌电图（EMG）、皮肤电活动（EDA）、呼吸描记图（RSP）和光电容积脉搏波（PPG）。</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';\">2.进入平台后，需要先创建信号，然后在窗口中选中信号右键呼出菜单。</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';\">3.对信号进行处理时，请尽量单独处理，建议只使用多选删除信号。</span></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\';\">4.平台正在不断改进和完善，所以目前可能仍存在一些问题。</span></p></body></html>"))


