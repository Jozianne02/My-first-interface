from PySide2.QtWidgets import QApplication,  QMainWindow, QPushButton, QLabel, QComboBox, QListWidget, QLineEdit, QDialog, QHBoxLayout 
from PySide2.QtCore import  Qt, QSize
#from PySide2.QtGui import  QPixmap
#from layout_color import  Color # type: ignore

import sys

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #self.button_is_checked = True
        #label
        #widget = QLabel("Pixmap")
        #font = widget.font()
        #font.setPointSize(35)
        #widget.setFont(font)

        #widget.setPixmap(QPixmap("jozi.jpg"))
        #widget.setScaledContents(True)
        #widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
         
         #QCombobox
        #self.widget = QComboBox()
        #self.widget.addItems(['Criar', 'Importar'])
     
        self.setWindowTitle("Meu orçamento")
        

        lb = QListWidget()
        lb.addItems((['Criar Lista', 'Importar Lista']))
        self.setCentralWidget(lb)

        #layout = QHBoxLayout()
        #layout.addWidget(Color('blue'))
        #layout.addWidget(Color('green'))
        
        #self.button = QPushButton("Clique aqui!")
        #button.setCheckable(True)

        #self.button.clicked.connect(self.the_button_was_clicked)
        #button.clicked.connect(self.the_button_was_toggled)
        #button.setChecked(self.button_is_checked)

        self.setMinimumSize(QSize(400, 300))
        #self.setCentralWidget(self.button)
        
        #self.setCentralWidget(self.widget)

        

    """ def the_button_was_clicked(self):
        print("botão clicado!")
        #self.button.setText("Já clicamos") 
        self.button.setEnabled(False)
        self.setWindowTitle("Just one Click")"""
       
        

    #def the_button_was_toggled(self, checked):
        #self.button_is_checked = checked

        #print(self.button_is_checked)

app = QApplication(sys.argv)

window = Mainwindow()
window.show()

app.exec_()