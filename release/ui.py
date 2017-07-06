import sys, time
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget,\
    QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, \
    QProgressBar, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont

from browser import Browser, NetworkError, AuthError

class Worker(QThread):
    """Worker thread that should do all the network work"""
    DO_NOTHING = 0
    LOG_IN = 1
    COUNT_WORK = 2
    DO_WORK = 3
    
    # Signal emited after each page is processed
    onProgress = pyqtSignal(int)

    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        
        self.shouldExit = False
        self.success = False
        self.workCount = 0
        self.type = Worker.DO_NOTHING

    def logIn(self, user, password):
        """Attempts to log in the Allims website."""
        self.type = Worker.LOG_IN
        self.success = False
        self.start()

    def countWork(self):
        """Counts how many pages need to be processed in the Allims website"""
        self.type = Worker.COUNT_WORK
        self.workCount = 0
        self.success = False
        self.start()

    def processPages(self, path):
        """Processes all pages that were gotten in the countWork() method"""
        self.type = Worker.DO_WORK
        self.path = path
        self.success = False
        self.start()

    def getState(self):
        """Gets the current state of the thread. (DO_NOTHING, LOG_IN, COUNT_WORK, DO_WORK).
        The state represents the last task performed."""
        return self.type

    def getSuccess(self):
        """Returns whether the last task performed was successful or not"""
        return self.success

    def getWorkCount(self):
        """Returns the number of pages that need to be processed.
        It's the same values returned by the call to countWork() method"""
        return self.workCount

    def run(self):
        """Do some work, based on the current state (type) of the thread"""
        if self.type == Worker.DO_NOTHING:
            time.sleep(1)
        elif self.type == Worker.LOG_IN:
            time.sleep(1)
            self.success = True
        elif self.type == Worker.COUNT_WORK:
            time.sleep(1)
            self.workCount = 5
            self.success = True
        elif self.type == Worker.DO_WORK:
            for i in range(self.workCount):
                time.sleep(1)
                self.onProgress.emit(i+1)
            self.success = True
        else:
            pass

    def __del__(self):
        self.shouldExit = True
        self.wait()

class ElfWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.center()
        self.setWindowTitle('PAQLF Scraper')

        # Set form header text
        headerlbl = QLabel('Digite as informações de <i>log in</i> para o <i>website</i> da Allims')
        font = QFont()
        font.setPointSize(12)
        font.setStyleHint(QFont.TypeWriter)
        headerlbl.setFont(font)
        headerlbl.setAlignment(Qt.AlignCenter)

        # Set button
        btn = QPushButton("Iniciar")
        btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        btn.clicked.connect( self.onClick )

        # Set form box
        ulbl = QLabel('Usuário')
        ulbl.setAlignment(Qt.AlignCenter)
        ulbl.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        utxt = QLineEdit()
        utxt.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        utxt.setMaxLength(25)
        utxt.returnPressed.connect(btn.click)

        plbl = QLabel('Senha')
        plbl.setAlignment(Qt.AlignCenter)
        plbl.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        ptxt = QLineEdit()
        ptxt.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        ptxt.setMaxLength(25)
        ptxt.setEchoMode(QLineEdit.Password)
        ptxt.returnPressed.connect(btn.click)

        lblbox = QVBoxLayout()
        lblbox.addWidget(ulbl)
        lblbox.addWidget(plbl)

        txtbox = QVBoxLayout()
        txtbox.addWidget(utxt)
        txtbox.addWidget(ptxt)

        formbox = QHBoxLayout()
        formbox.addStretch(1)
        formbox.addLayout(lblbox)
        formbox.addLayout(txtbox)
        formbox.addStretch(1)
        formbox.setContentsMargins(0, 20, 0, 10)

        # Set info box
        login_lbl = QLabel("")
        login_lbl.setAlignment(Qt.AlignCenter)

        count_lbl = QLabel("")
        count_lbl.setAlignment(Qt.AlignCenter)

        work_lbl = QLabel("")
        work_lbl.setAlignment(Qt.AlignCenter)

        progress = QProgressBar()
        progress.setAlignment(Qt.AlignCenter)

        infobox = QVBoxLayout()
        infobox.setAlignment(Qt.AlignCenter)
        infobox.addWidget(login_lbl)
        infobox.addWidget(count_lbl)
        infobox.addWidget(work_lbl)
        infobox.addWidget(progress)

        # Fill main box
        main_box = QVBoxLayout(self)
        main_box.setAlignment(Qt.AlignCenter)
        main_box.addWidget(headerlbl)
        main_box.addLayout(formbox)
        main_box.addLayout(infobox)
        main_box.addWidget(btn)
        main_box.setAlignment(btn, Qt.AlignCenter)

        # Create alert widget
        self.alert = QMessageBox()

        # Get the due instance variables. I hate typing 'self' all the time.
        self.plbl = plbl
        self.ulbl = ulbl
        self.ptxt = ptxt
        self.utxt = utxt
        self.btn = btn
        self.headerlbl = headerlbl
        self.login_lbl = login_lbl
        self.count_lbl = count_lbl
        self.work_lbl = work_lbl
        self.progress = progress

        # Set up worker thread
        self.thread = Worker()
        self.thread.finished.connect(self.joinThread)
        self.thread.onProgress.connect(self.updateWorkLabel)

        self.show()
        self.showInfoBox(False)

    def center(self):
        """Centers the window on the user's computer's screen"""
        frame = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(cp)
        self.move(frame.topLeft())

    def showLogBox(self, show):
        """Shows the log in box if 'show' is True.
        Hides it, if 'show' is False."""
        QWidget.setFocus(self.utxt)
        self.plbl.setVisible(show)
        self.ulbl.setVisible(show)
        self.ptxt.setVisible(show)
        self.utxt.setVisible(show)
        self.headerlbl.setVisible(show)
        self.btn.setVisible(show)

    def showInfoBox(self, show):
        """Shows the information box if 'show' is True.
        Hides it, if 'show' is False."""
        self.login_lbl.setVisible(show)
        self.count_lbl.setVisible(show)
        self.work_lbl.setVisible(show)
        self.progress.setVisible(show)

    def alertUser(self, string):
        """Opens an alert dialog with message 'string'"""
        self.alert.setText(string)
        self.alert.exec()

    def onClick(self):
        """Method called when the 'Iniciar' button is clicked."""
        self.showLogBox(False)
        
        self.login_lbl.setText("Realizando <i>log in</i>...")
        self.login_lbl.show()
        
        # Log in procedure in another thread
        self.thread.logIn(self.utxt.text(), self.ptxt.text())

    def joinThread(self):
        """Method called whenever the worked thread has finished its work"""

        # Check thread state
        state = self.thread.getState()

        # Decide next work based on the state
        if state == Worker.LOG_IN:
            self.finishLogIn()
        elif state == Worker.COUNT_WORK:
            self.finishCountWork()
        elif state == Worker.DO_WORK:
            self.finishProcessing()
            pass
        else:
            pass

    def finishLogIn(self):
        """Method to call when the worker thread has finished the logIn() procedure"""
        self.utxt.clear()
        self.ptxt.clear()

        if self.thread.getSuccess():
            self.login_lbl.setText("<i>Log in</i> realizado com sucesso.")
            self.count_lbl.setText("Contando a quantidade de trabalho a ser realizada...")
            self.count_lbl.show()
            # Launch thread for counting work
            self.thread.countWork()
        else:
            self.showInfoBox(False)
            self.showLogBox(True)
            self.alertUser("<h3>Falha ao realizar o <i>log in</i></h3>"
                    + "<p>Verifique seu usuário e senha.</p>"
                    + "<p>Verifique também a sua conexão.</p>")

    @pyqtSlot(int)
    def updateWorkLabel(self, num):
        """There will be a label showing the current progress of how many pages have been processed.
        This method updates the label for showing that 'num' pages have been processed so far."""
        self.work_lbl.setText(self.work_string.format(num))
        self.progress.setValue(num)

    def finishCountWork(self):
        """Method called whenever the worker thread has finished the countWorK() procedure"""
        if not self.thread.getSuccess():
            self.showInfoBox(False)
            self.showLogBox(True)
            self.alertUser("<h3>Falha ao realizar a contagem de páginas a processar</h3>"
                    + "<p>Verifique a sua conexão.</p>")
            return

        count = self.thread.getWorkCount()
        self.count_lbl.setText("Número de páginas a serem processadas: {}".format(count))
        self.work_string = "Processando páginas... ({}/{})".format("{}", count)
        self.updateWorkLabel(0)
        self.work_lbl.show()
        self.progress.show()
        self.progress.setMinimum(0)
        self.progress.setMaximum(count)
        self.progress.setValue(0)

        # Inquire the user for what directory to save results into
        while True:
            dirpath = QFileDialog.getExistingDirectory(self, "Diretório para salvar as planilhas.")
            if not dirpath:
                self.alertUser("<h3>Selecione um diretório, por favor.</h3>")
            else: break
        
        # Launch thread for processing all the pages
        self.thread.processPages(dirpath)

    def finishProcessing(self):
        """Method called whenever the worker thread has finished the processPages() procedure"""

        # Show the log in screen again
        self.showInfoBox(False)
        self.showLogBox(True)
        if not self.thread.getSuccess():
            self.alertUser("<h3>Falha ao processar as páginas do <i>website</i></h3>"
                    + "<p>Verifique a sua conexão.</p>")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ElfWindow()

    sys.exit(app.exec_())
