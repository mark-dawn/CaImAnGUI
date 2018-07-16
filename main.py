from PyQt5 import QtWidgets as qtW, QtCore
import pyqtgraph as pg
import pyqtgraph.parametertree as pt
import sys


class MainWindow(qtW.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 1280, 720)
        self.statusBar()
        self.setCentralWidget(MainWidget(parent=self))
        self.setWindowTitle('CaImAn ValidationGUI')


class MainWidget(qtW.QWidget):
    """
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.overall = OverallView(parent=self)
        self.status = parent.statusBar()
        line = qtW.QFrame(parent=self)
        line.setFrameShadow(qtW.QFrame.Sunken)
        line.setFrameShape(qtW.QFrame.HLine)

        self.sublayouts = (FunctionButtons(self.status, parent=self), EvaluationArea(parent=self))

        layout = qtW.QVBoxLayout(self)
        layout.addLayout(self.overall, stretch=4)
        layout.addWidget(line)
        layout.addLayout(self.sublayouts[1], stretch=5)
        layout.addLayout(self.sublayouts[0], stretch=1)

        self.setLayout(layout)

    def close(self):
        super().close()
        self.parent().close()


class OverallView(qtW.QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.spatial_view = pg.ImageView(parent=parent)
        self.scatter = pg.PlotWidget(parent=parent)
        self.addWidget(self.spatial_view, stretch=1)
        self.addWidget(self.scatter, stretch=1)


class FunctionButtons(qtW.QHBoxLayout):
    def __init__(self, logger, parent=None):
        super().__init__()
        self.logger = logger
        for txt, fun in (('Next', self.log), ('Discard', self.log), ('exit', parent.close)):
            button = qtW.QPushButton(txt, parent=parent)
            # to connect the signal we just find the signal we want and call connect
            button.clicked.connect(fun)
            self.addWidget(button)

    def log(self):
        pressed_button = self.sender()  # recover our button
        self.logger.showMessage(pressed_button.text())


class EvaluationArea(qtW.QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.splitter_out = qtW.QSplitter(QtCore.Qt.Horizontal, parent=parent)

        self.ROI = pg.ImageView(parent=self.splitter_out)

        self.splitter_in = qtW.QSplitter(QtCore.Qt.Vertical, parent=self.splitter_out)
        self.trace = pg.PlotWidget(parent=self.splitter_in)
        self.cm_tabs = CaimanControl(parent=self.splitter_in)

        self.splitter_in.setFrameShadow(qtW.QSplitter.Sunken)
        self.splitter_out.setFrameShadow(qtW.QSplitter.Sunken)
        [self.splitter_out.setStretchFactor(*t) for t in ((0, 1), (1, 7))]
        [self.splitter_in.setStretchFactor(*t) for t in ((1, 1), (0, 8))]

        self.addWidget(self.splitter_out)


class CaimanControl(qtW.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.textbox = qtW.QPlainTextEdit(parent=self)
        self.textbox.setReadOnly(True)

        self.cm_params = pt.ParameterTree(parent=self)

        self.addTab(self.textbox, "Log")
        self.addTab(self.cm_params, "Parameters")



if __name__ == '__main__':
    import numpy as np
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
