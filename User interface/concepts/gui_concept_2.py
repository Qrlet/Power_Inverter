# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_concept_2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(708, 389)
        self.comboBox = QtGui.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(30, 30, 69, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 10, 91, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 91, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.comboBox_2 = QtGui.QComboBox(Form)
        self.comboBox_2.setGeometry(QtCore.QRect(30, 80, 69, 22))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.pushButton_6 = QtGui.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(30, 120, 75, 31))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 170, 75, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_7 = QtGui.QPushButton(Form)
        self.pushButton_7.setGeometry(QtCore.QRect(30, 220, 75, 21))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.pushButton_8 = QtGui.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(140, 30, 91, 31))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.pushButton_9 = QtGui.QPushButton(Form)
        self.pushButton_9.setGeometry(QtCore.QRect(140, 100, 91, 31))
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.horizontalSlider_2 = QtGui.QSlider(Form)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(140, 70, 191, 21))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName(_fromUtf8("horizontalSlider_2"))
        self.lcdNumber_2 = QtGui.QLCDNumber(Form)
        self.lcdNumber_2.setGeometry(QtCore.QRect(260, 100, 71, 31))
        self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(260, 30, 71, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton_10 = QtGui.QPushButton(Form)
        self.pushButton_10.setGeometry(QtCore.QRect(140, 150, 91, 31))
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(260, 150, 71, 31))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.pushButton_11 = QtGui.QPushButton(Form)
        self.pushButton_11.setGeometry(QtCore.QRect(140, 200, 101, 41))
        self.pushButton_11.setObjectName(_fromUtf8("pushButton_11"))
        self.comboBox_3 = QtGui.QComboBox(Form)
        self.comboBox_3.setGeometry(QtCore.QRect(30, 280, 69, 22))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 260, 91, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton_12 = QtGui.QPushButton(Form)
        self.pushButton_12.setGeometry(QtCore.QRect(30, 310, 75, 31))
        self.pushButton_12.setObjectName(_fromUtf8("pushButton_12"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(350, 30, 91, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(350, 50, 351, 301))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Modbus port", None))
        self.label_2.setText(_translate("Form", "Device", None))
        self.pushButton_6.setText(_translate("Form", "Turn On", None))
        self.pushButton_2.setText(_translate("Form", "Turn Off", None))
        self.pushButton_7.setText(_translate("Form", "Test modbus", None))
        self.pushButton_8.setText(_translate("Form", "Set Frequency", None))
        self.pushButton_9.setText(_translate("Form", "Get Frequency", None))
        self.pushButton_10.setText(_translate("Form", "Set Width", None))
        self.pushButton_11.setText(_translate("Form", "Autorun", None))
        self.label_3.setText(_translate("Form", "Sensor port", None))
        self.pushButton_12.setText(_translate("Form", "Initialize", None))
        self.label_4.setText(_translate("Form", "LOGS", None))


class ModbusGui(QtGui.QWidget, Ui_Form):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setParent(None)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = ModbusGui()
    window.show()
    sys.exit(app.exec_())