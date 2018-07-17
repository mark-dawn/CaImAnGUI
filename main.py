from PyQt5 import QtWidgets as qtW
from GUI import MainWindow
import sys


if __name__ == '__main__':
    try:
        import qdarkstyle as qd
    except ModuleNotFoundError:
        qd = None

    app = qtW.QApplication(sys.argv)
    if qd is not None:
        app.setStyleSheet(qd.load_stylesheet_pyqt5())

    ex = MainWindow()

    ex.show()
    sys.exit(app.exec_())
