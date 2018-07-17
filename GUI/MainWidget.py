from PyQt5 import QtWidgets as qtW, QtCore
from GUI import OverallView, FunctionButtons, EvaluationArea


class MainWidget(qtW.QWidget):
    """
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.status = parent.statusBar()
        self.logger = parent.logger
        line = qtW.QFrame(parent=self)
        line.setFrameShadow(qtW.QFrame.Sunken)
        line.setFrameShape(qtW.QFrame.HLine)

        self.sublayouts = {'over': OverallView(parent=self), 'btns': FunctionButtons(parent=self), 'work_area': EvaluationArea(parent=self)}

        layout = qtW.QVBoxLayout(self)
        layout.addLayout(self.sublayouts['over'], stretch=4)
        layout.addWidget(line)
        layout.addLayout(self.sublayouts['work_area'], stretch=5)
        layout.addLayout(self.sublayouts['btns'], stretch=1)

        self.setLayout(layout)

    def close(self):
        super().close()
        self.parent().close()

    def setDisabled(self, a0: bool):
        for _, child in self.sublayouts.items():
            child.setDisabled(a0)