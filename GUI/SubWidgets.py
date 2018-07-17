from PyQt5 import QtWidgets as qtW, QtCore
import pyqtgraph as pg
import pyqtgraph.parametertree as pt
import logging


class OverallView(qtW.QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.spatial_view = pg.ImageView(parent=parent)
        self.scatter = pg.PlotWidget(parent=parent)
        self.addWidget(self.spatial_view, stretch=1)
        self.addWidget(self.scatter, stretch=1)

    def setDisabled(self, a0: bool):
        for widget in (self.itemAt(i).widget() for i in range(self.count())):
            widget.setDisabled(a0)


class FunctionButtons(qtW.QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.logger = parent.logger
        for txt, fun in (('Next', self.log), ('Discard', self.log), ('exit', parent.close)):
            button = qtW.QPushButton(txt, parent=parent)
            button.clicked.connect(fun)
            self.addWidget(button)

    def log(self):
        self.logger.info("Pressed button " + self.sender().text())

    def setDisabled(self, a0: bool):
        for widget in (self.itemAt(i).widget() for i in range(self.count())):
            widget.setDisabled(a0)


class EvaluationArea(qtW.QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__()
        self.splitter_out = qtW.QSplitter(QtCore.Qt.Horizontal, parent=parent)

        self.ROI = pg.ImageView(parent=self.splitter_out)

        self.splitter_in = qtW.QSplitter(QtCore.Qt.Vertical, parent=self.splitter_out)
        self.trace = pg.PlotWidget(parent=self.splitter_in)
        self.cm_tabs = CaImAnControl(parent=self.splitter_in)

        self.splitter_in.setFrameShadow(qtW.QSplitter.Sunken)
        self.splitter_out.setFrameShadow(qtW.QSplitter.Sunken)
        [self.splitter_out.setStretchFactor(*t) for t in ((0, 1), (1, 7))]
        [self.splitter_in.setStretchFactor(*t) for t in ((1, 1), (0, 8))]

        self.addWidget(self.splitter_out)

    def setDisabled(self, a0: bool):
        self.ROI.setDisabled(a0)
        self.trace.setDisabled(a0)
        self.cm_tabs.setDisabled(a0)


class CaImAnControl(qtW.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.textbox = TextBoxHandler(parent=self)
        self.cm_params = pt.ParameterTree(parent=self)

        self.addTab(self.textbox, "Log")
        self.addTab(self.cm_params, "Parameters")

    def setDisabled(self, a0: bool):
        self.setCurrentWidget(self.textbox)
        super().setDisabled(a0)


class TextBoxHandler(qtW.QPlainTextEdit, logging.Handler):
    def __init__(self, parent=None):
        qtW.QPlainTextEdit.__init__(self, parent=parent)
        logging.Handler.__init__(self)
        self.setReadOnly(True)
        self.setLevel(logging.INFO)
        self.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    def emit(self, record):
        self.appendPlainText(self.format(record))
