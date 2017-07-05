import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget,\
    QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont

class Worker(QThread):

    def __init__(self):
        pass
    
    def logIn(self, user, password):
        pass

    def countWork(self):
        pass

    def processPages(self):
        pass

    def __del__(self):
        pass

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
        info_lbl = QLabel("Information here")
        info_lbl.setAlignment(Qt.AlignCenter)
        info_lbl.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        infobox = QVBoxLayout()
        infobox.setAlignment(Qt.AlignCenter)
        infobox.addWidget(info_lbl)

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
        self.info_lbl = info_lbl

        self.show()
        self.showInfoBox(False)

    def center(self):
        frame = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(cp)
        self.move(frame.topLeft())

    def showLogBox(self, show):
        self.plbl.setVisible(show)
        self.ulbl.setVisible(show)
        self.ptxt.setVisible(show)
        self.utxt.setVisible(show)
        self.headerlbl.setVisible(show)
        self.btn.setVisible(show)

    def showInfoBox(self, show):
        self.info_lbl.setVisible(show)

    def finishCountWork(self, webpages):
        # Process all webpages in another thread, calling updateProgress() when convenient
        # Call finishProcessing() after thread runs
        pass

    def finishLogIn(self, isSuccess):
        if isSuccess:
            # Attempt to count work in another thread
            # call finishCountWork after the thread runs
            pass
        else:
            pass

    def onClick(self):
        self.showLogBox(False)

        # Attempt log in in another thread
        # call finishLogIn( result ) after the thread runs

        print(self.utxt.text())
        print(self.ptxt.text())
        self.utxt.clear()
        self.ptxt.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ElfWindow()

    sys.exit(app.exec_())
