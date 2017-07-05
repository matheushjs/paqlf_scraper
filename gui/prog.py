import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget,\
    QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt

class ElfWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.center()

        # Set form header text
        headerlbl = QLabel('Digite as informações de <i>log in</i> para o site da Allims')

        # Set form
        ulbl = QLabel('Usuário')
        ulbl.setAlignment(Qt.AlignCenter)
        ulbl.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        utxt = QLineEdit()
        utxt.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        utxt.setMaxLength(25)
        
        plbl = QLabel('Senha')
        plbl.setAlignment(Qt.AlignCenter)
        plbl.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        ptxt = QLineEdit()
        ptxt.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        ptxt.setMaxLength(25)
        ptxt.setEchoMode(QLineEdit.Password)

        lblbox = QVBoxLayout()
        lblbox.addWidget(ulbl)
        lblbox.addWidget(plbl)

        txtbox = QVBoxLayout()
        txtbox.addWidget(utxt)
        txtbox.addWidget(ptxt)
        txtbox.setContentsMargins(0, 10, 0, 10)

        formbox = QHBoxLayout()
        formbox.addLayout(lblbox)
        formbox.addLayout(txtbox)

        # Set button
        btn = QPushButton("Iniciar")
        btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

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
