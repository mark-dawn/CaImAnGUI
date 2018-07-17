from PyQt5 import QtWidgets as qtW, QtCore, QtGui
from GUI import MainWidget
import logging


class MainWindow(qtW.QMainWindow):
    logger = logging.getLogger('GUI_sys')

    def __init__(self):
        super().__init__()
        self.file = ""
        self.setGeometry(300, 300, 1280, 720)
        self.statusBar()
        setattr(self.statusBar(), 'showMessage', self.start_time_deco(self.statusBar().showMessage))

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
        if self.file:
            self.statusBar().showMessage('Opening ' + self.file)
            self.logger.info("Opening file" + self.file)
            # TODO: actually load data
        else:
            self.statusBar().showMessage('No file selected')
        self.setDisabled(False)

    def saveFile(self):
        self.setDisabled(True)
        if self.file:
            self.statusBar().showMessage('Saving ' + self.file)
            # TODO: save
        else:
            self.statusBar().showMessage('No file loaded!')
            self.logger.warning("Cannot save when file is not open")
        self.setDisabled(False)

    def setDisabled(self, a0: bool):
        self.toolbar.setDisabled(a0)
        self.centralWidget().setDisabled(a0)

    def start_time_deco(self, fun):
        def timer_wrapper(*args, **kwargs):
            QtCore.QTimer(parent=self).singleShot(6000, self.statusBar().clearMessage)
            fun(*args, **kwargs)
        return timer_wrapper
