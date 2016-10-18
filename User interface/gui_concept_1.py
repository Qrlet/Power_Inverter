from PyQt4 import QtCore, QtGui
from Modbus import RTU
import sys
from serial.tools.list_ports_windows import comports

# TODO: Set frequency from text box.
# TODO: Why can't move ui methods functionality to ModbusGui methods, i.e. clicking button would do few things at once
# TODO: Destroying object
# TODO: Turning OFF should notify slider
# TODO: Different types programs for start working
# TODO: Hz format 500 -> 50.0
# TODO: Move some methods to __init__ so lambda won't be needed
# TODO: Need to refresh port list

# List of active com ports
HITACHI_PORT = [port[0] for port in comports()]
print HITACHI_PORT
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


def main():
    # QApplication object which is an application definition
    app = QtGui.QApplication(sys.argv)
    window = ModbusGui()
    window.show()
    sys.exit(app.exec_())


class UiClass(object):

    def setup_ui(self, Form):
        # Main window object, layout
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(600, 300)

        # Combo box
        self.comboBox = QtGui.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(10, 30, 69, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItems(HITACHI_PORT)

        # Labels
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 160, 61, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        # Push buttons
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(110, 20, 71, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 20, 75, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(300, 20, 75, 31))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))

        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 70, 81, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))

        self.pushButton_5 = QtGui.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(200, 70, 81, 23))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))

        # LCD
        self.lcdNumberGetFrq = QtGui.QLCDNumber(Form)
        self.lcdNumberGetFrq.setGeometry(QtCore.QRect(300, 70, 71, 23))
        self.lcdNumberGetFrq.setObjectName(_fromUtf8("lcdNumber"))
        self.lcdNumberSetFrq = QtGui.QLCDNumber(Form)
        self.lcdNumberSetFrq.setGeometry(QtCore.QRect(110, 70, 71, 23))
        self.lcdNumberSetFrq.setObjectName(_fromUtf8("lcdNumber_2"))

        # Sliders
        self.horizontalSlider = QtGui.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(10, 120, 450, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.horizontalSlider.setMinimum(RTU.HITACHI_FRQUENCY_MIN)
        self.horizontalSlider.setMaximum(RTU.HITACHI_FRQUENCY_MAX)

        # Log window
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setReadOnly(True)
        self.textEdit.setGeometry(QtCore.QRect(20, 180, 500, 111))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Select device port", None))
        self.pushButton.setText(_translate("Form", "Initialize", None))
        self.pushButton_2.setText(_translate("Form", "Turn On/Off", None))
        self.pushButton_3.setText(_translate("Form", "Test modbus", None))
        self.pushButton_4.setText(_translate("Form", "Set frequency (0)", None))
        self.pushButton_5.setText(_translate("Form", "Get frequency", None))
        self.label_2.setText(_translate("Form", "Log", None))


class ModbusGui(QtGui.QWidget, UiClass):

    def __init__(self, debug=True, debug_modbus=True):
        QtGui.QWidget.__init__(self)
        self.setParent(None)
        self.ui = UiClass()
        self.ui.setup_ui(self)
        self.setup_signals()
        # Attribute checking if device is turned ON or OFF
        self.status = None

    def __del__(self):
        self.modbus.__del__()

    def setup_signals(self):
        self.ui.pushButton.clicked.connect(lambda: self.create_modbus_handler())
        # Change what should emit signal
        self.ui.horizontalSlider.valueChanged.connect(self.ui.lcdNumberSetFrq.display)
        self.ui.horizontalSlider.valueChanged.connect(lambda: self.set_frequency(self.ui.horizontalSlider.value()))
        self.ui.pushButton_4.clicked.connect(lambda: self.set_frequency(0))
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.horizontalSlider.setValue(self.get_frequency()))
        self.ui.pushButton_2.clicked.connect(lambda: self.turn_on_off_device())
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.lcdNumberSetFrq.display(self.get_frequency()))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.horizontalSlider.setValue(self.get_frequency()))
        self.ui.pushButton_5.clicked.connect(lambda: self.get_frequency())
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.lcdNumberGetFrq.display(self.get_frequency()))
        self.ui.pushButton_3.clicked.connect(lambda: self.test_modbus())

    def create_modbus_handler(self):
        port_selected = str(self.ui.comboBox.currentText())
        try:
            self.modbus = RTU.HitachiSlave(1, port_selected, debug_class=False, debug_modbus=False)
            self.get_status()
        except Exception as e:
            print str(e)
            print "[Modbus] Hitachi slave handler object not created."
        else:
            if self.status == 0:
                print "[Modbus] Device status: OFF"
            elif self.status == 1:
                print "[Modbus] Device status: ON"
            else:
                print "[Modbus] Warning! Device status: UNKNOWN."

    def get_status(self):
        self.status = self.modbus.get_status()

    def turn_on_off_device(self):
        # Need to call this method for updated
        self.get_status()
        if self.status == 0:
            try:
                # Set frequency to 0 before turn ON.
                self.modbus.set_frequency(0)
                self.modbus.turn_on_device()
            except Exception as e:
                print str(e)
                print "[Modbus] Power inverter not started."
            else:
                print "[Hitachi] Device turned ON."
        elif self.status == 1:
            try:
                # Set frequency to 0 before turn OFF.
                self.modbus.set_frequency(0)
                self.modbus.turn_off_device()
            except Exception as e:
                print str(e)
                print "[Modbus] Power inverter not stopped."
            else:
                print "[Hitachi] Device turned OFF."
        else:
            print "[Modbus] Status of device unknown."

    # Need to return value in order to pass it to QLCDNumber object
    def get_frequency(self):
        return self.modbus.get_frequency()

    def set_frequency(self, frequency):
        self.modbus.set_frequency(frequency)

    def test_modbus(self, test_cycles=100):
        test_passed = 0
        for i in xrange(test_cycles):
            test_passed += self.modbus.modbus_test()
        print("[Modbus] Percentage value of tests passed: " + str(100*test_passed/test_cycles) + " [%].")


if __name__ == "__main__":
    main()
