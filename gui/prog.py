import sys, time
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget,\
    QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, \
    QProgressBar
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont

class Worker(QThread):
    DO_NOTHING = 0
    LOG_IN = 1
    COUNT_WORK = 2
    DO_WORK = 3
    
    onProgress = pyqtSignal(int)

    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        
        self.shouldExit = False
        self.loginSuccess = False
        self.workCount = 0
        self.type = Worker.DO_NOTHING

    def logIn(self, user, password):
        self.type = Worker.LOG_IN
        self.loginSuccess = False
        self.start()

    def countWork(self):
        self.type = Worker.COUNT_WORK
        self.workCount = 0
        self.start()

    def processPages(self):
        self.type = Worker.DO_WORK
        self.start()

    def getState(self):
        return self.type

    def getLoginSuccess(self):
        return self.loginSuccess

    def getWorkCount(self):
        return self.workCount

    def run(self):
        if self.type == Worker.DO_NOTHING:
            time.sleep(1)
        elif self.type == Worker.LOG_IN:
            time.sleep(1)
            self.loginSuccess = True
        elif self.type == Worker.COUNT_WORK:
            time.sleep(1)
            self.workCount = 5
        elif self.type == Worker.DO_WORK:
            for i in range(self.workCount):
                time.sleep(1)
                self.onProgress.emit(i+1)
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

        # Set form header text
        headerlbl = QLabel('Digite as informações de <i>log in</i> para o <i>website</i> da Allims')
        font = QFont()
        font.setPointSize(12)
        font.setStyleHint(QFont.TypeWriter)
        headerlbl.setFont(font)

        # Set button
        btn = QPushButton("Iniciar")
        btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        btn.clicked.connect( self.onClick )

        # Set form
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
        #progress.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

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
        frame = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(cp)
        self.move(frame.topLeft())

    def showLogBox(self, show):
        QWidget.setFocus(self.utxt)
        self.plbl.setVisible(show)
        self.ulbl.setVisible(show)
        self.ptxt.setVisible(show)
        self.utxt.setVisible(show)
        self.headerlbl.setVisible(show)
        self.btn.setVisible(show)

    def showInfoBox(self, show):
        self.login_lbl.setVisible(show)
        self.count_lbl.setVisible(show)
        self.work_lbl.setVisible(show)
        self.progress.setVisible(show)

    def onClick(self):
        self.showLogBox(False)
        
        self.login_lbl.setText("Realizando <i>log in</i>...")
        self.login_lbl.show()
        
        self.thread.logIn(self.utxt.text(), self.ptxt.text())

    def joinThread(self):
        state = self.thread.getState()
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
        self.utxt.clear()
        self.ptxt.clear()

        if self.thread.getLoginSuccess():
            self.login_lbl.setText("<i>Log in</i> realizado com sucesso.")
            self.count_lbl.setText("Contando a quantidade de trabalho a ser realizada...")
            self.count_lbl.show()
            self.thread.countWork()
        else:
            self.loginlbl.setText("Falha ao realizar o <i>log in</i>.")

    @pyqtSlot(int)
    def updateWorkLabel(self, num):
        self.work_lbl.setText(self.work_string.format(num))
        self.progress.setValue(num)

    def finishCountWork(self):
        # Process all webpages in another thread, calling updateProgress() when convenient
        # Call finishProcessing() after thread runs
        count = self.thread.getWorkCount()
        self.count_lbl.setText("Número de páginas a serem processadas: {}".format(count))
        self.work_string = "Processando páginas... ({}/{})".format("{}", count)
        self.updateWorkLabel(0)
        self.work_lbl.show()
        self.progress.show()
        self.progress.setMinimum(0)
        self.progress.setMaximum(count)
        self.progress.setValue(0)
        self.thread.processPages()

    def finishProcessing(self):
        self.showInfoBox(False)
        self.showLogBox(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ElfWindow()

    sys.exit(app.exec_())
