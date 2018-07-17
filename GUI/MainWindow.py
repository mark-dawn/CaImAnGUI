from PyQt5 import QtWidgets as qtW, QtCore, QtGui
from GUI import MainWidget
import logging


class MainWindow(qtW.QMainWindow):
    log_freq = 100
    logger = logging.getLogger('GUI_sys')

    def __init__(self):
        super().__init__()
        self.file = None
        self.setGeometry(300, 300, 1280, 720)
        self.statusBar()
        # self.timerLog = QtCore.QTimer(parent=self)
        # self.timerLog.timeout.connect(self.updateLog)

        act_load = qtW.QAction(QtGui.QIcon.fromTheme('document-open'), 'Open', parent=self)
        act_save = qtW.QAction(QtGui.QIcon.fromTheme('document-save'), 'Save', parent=self)
        act_load.triggered.connect(self.openFile)
        act_save.triggered.connect(self.saveFile)

        self.toolbar = self.addToolBar('Load/Save')
        self.toolbar.addAction(act_load)
        self.toolbar.addAction(act_save)

        self.setCentralWidget(MainWidget(parent=self))

        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler('log.txt', mode='w')
        fh.setFormatter(logging.Formatter('%(asctime)s - [%(name)s]%(levelname)s: %(message)s'))
        self.logger.addHandler(fh)
        self.logger.addHandler(self.centralWidget().sublayouts['work_area'].cm_tabs.textbox)
        self.setWindowTitle('CaImAn ValidationGUI')

    def openFile(self):
        self.setDisabled(True)
        self.file, filt = qtW.QFileDialog.getOpenFileName(parent=self, caption='Open File...')
        self.statusBar().showMessage('Opening ' + self.file)
        self.logger.info("test")
        # TODO: actually load data
        self.setDisabled(False)
        self.statusBar().clearMessage()

    def saveFile(self):
        self.lock()
        self.statusBar().showMessage('Saving ' + self.file)
        # TODO: save
        self.statusBar().clearMessage()

    # def updateLog(self):
    #     for logger in self.loggers:
    #         logger.print(self.log)

    def show(self):
        super().show()
        # self.timerLog.start(self.log_freq)

    def setDisabled(self, a0: bool):
        self.toolbar.setDisabled(a0)
        self.centralWidget().setDisabled(a0)