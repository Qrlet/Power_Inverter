from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
import sys
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
from multiprocessing import Queue
import logging


logger = logging.getLogger(__name__)


N_POINTS_ON_PLOT = 100


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.setup_signals()
    window.show()
    sys.exit(app.exec_())

class SensorWidget():
    def __init__(self, parent=None):
        self.figure, self.axes = plt.subplots()
        self.x_axis = []
        self.y_values = []
        self.sensor_plot_queue = Queue(maxsize=N_POINTS_ON_PLOT)

        self.compute_initial_figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(parent)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(5)

    def compute_initial_figure(self):
        self.axes.plot(self.y_values)

    def feed_value(self, value):
        self.sensor_plot_queue.put(value)

    def update_figure(self):
        self.axes.cla()
        # ToDo: Need to add lock here and iterate through all elements
        if not self.sensor_plot_queue.empty():
            self.y_values.append(self.sensor_plot_queue.get())
        if len(self.y_values) > N_POINTS_ON_PLOT:
            self.y_values.pop(0)
            self.x_axis = [x + 1 for x in self.x_axis]
        else:
            self.axes.set_xlim(0, N_POINTS_ON_PLOT)
            while len(self.x_axis) < len(self.y_values):
                self.x_axis.append(len(self.y_values))
        self.axes.plot(self.x_axis, self.y_values)
        logging.debug("Drawing new plot")
        self.canvas.draw()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(627, 347)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lcdNumber_freq = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_freq.setGeometry(QtCore.QRect(110, 130, 71, 23))
        self.lcdNumber_freq.setObjectName("lcdNumber_freq")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 60, 85, 27))
        self.pushButton.setObjectName("pushButton")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(120, 60, 81, 27))
        self.lineEdit.setObjectName("lineEdit")

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(20, 100, 160, 18))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.label_freq = QtWidgets.QLabel(self.centralwidget)
        self.label_freq.setGeometry(QtCore.QRect(30, 130, 71, 17))
        self.label_freq.setObjectName("label_freq")


        self.lcdNumber_width = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_width.setGeometry(QtCore.QRect(110, 170, 71, 23))
        self.lcdNumber_width.setObjectName("lcdNumber_width")

        self.sensor_widget = SensorWidget(self.centralwidget)
        self.sensor_widget.canvas.setGeometry(QtCore.QRect(220, 60, 400, 300))


        self.label_width = QtWidgets.QLabel(self.centralwidget)
        self.label_width.setGeometry(QtCore.QRect(30, 170, 71, 17))
        self.label_width.setObjectName("label_width")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 627, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Falownik"))
        self.pushButton.setText(_translate("MainWindow", "Set freq"))
        self.label_freq.setText(_translate("MainWindow", "Freq"))
        self.label_width.setText(_translate("MainWindow", "Width"))


    def setup_signals(self):
        self.horizontalSlider.valueChanged.connect(self.lcdNumber_freq.display)
        self.pushButton.clicked.connect(lambda: self.lcdNumber_freq.display(float(self.lineEdit.text())))



if __name__ == "__main__":
    main()