import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget,\
    QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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
        btn.clicked.connect( lambda: print("hey") )

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

        # Fill main box
        main_box = QVBoxLayout(self)
        main_box.setAlignment(Qt.AlignCenter)
        main_box.addWidget(headerlbl)
        main_box.addLayout(formbox)
        main_box.addWidget(btn)
        main_box.setAlignment(btn, Qt.AlignCenter)

        self.show()

    def center(self):
        frame = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(cp)
        self.move(frame.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = ElfWindow()

    sys.exit(app.exec_())
