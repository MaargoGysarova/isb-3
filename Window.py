import os
import shutil

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolTip, QLabel, QFileDialog, QLineEdit, QWidget, QVBoxLayout, \
    QPushButton
import sys
from PyQt6 import QtWidgets
import symmetrical_encrpt
import asymmetric_encrpt
import logging


class MainWindow(QMainWindow):

    def __init__(self):
        self.asym_encrpt = None
        self.sym_encrpt = None
        self.way = ''
        self.count = 0
        super(MainWindow, self).__init__()
        self.flag_click_button_1 = None
        btn_font_main = QFont('Impact', 25)
        btn_StyleSheet_main = 'background-color: #ffffff; color: #4682B4; border :1px solid;'

        # параметры окна
        self.setGeometry(50, 50, 1200, 675)
        self.setWindowTitle('Application programing laba 3')
        self.setFixedSize(self.size())
        QToolTip.setFont(QFont('SansSerif', 10))

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('1670825741_3-27.jpg'))
        self.label.setGeometry(0, 0, 1200, 675)
        self.label.setScaledContents(True)

        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Сгенерировать ключи")
        self.button1.setGeometry(450, 150, 300, 50)
        self.button1.setFixedWidth(400)
        self.button1.setFont(btn_font_main)
        self.button1.setStyleSheet(btn_StyleSheet_main)
        self.button1.clicked.connect(self.click_button_1)
        self.button1.enterEvent = lambda event: self.button1.setStyleSheet(
            'background-color: #ffffff; color: #D2691E; border :1px solid; border-color: #D2691E;')
        self.button1.leaveEvent = lambda event: self.button1.setStyleSheet(
            'background-color: #ffffff; color: #4682B4; border :1px solid;')
        self.buttonSuccess_save()

        self.button2 = QtWidgets.QPushButton(self)
        self.button2.setText("Зашифровать текст")
        self.button2.setGeometry(450, 230, 300, 50)
        self.button2.setFixedWidth(400)
        self.button2.setFont(btn_font_main)
        self.button2.setStyleSheet(btn_StyleSheet_main)

        self.button2.clicked.connect(self.click_button_2)

        self.button2.enterEvent = lambda event: self.button2.setStyleSheet(
            'background-color: #ffffff; color: #D2691E; border :1px solid; border-color: #D2691E;')
        self.button2.leaveEvent = lambda event: self.button2.setStyleSheet(
            'background-color: #ffffff; color: #4682B4; border :1px solid;')

        self.button3 = QtWidgets.QPushButton(self)
        self.button3.setText("Расшифровать текст")
        self.button3.setGeometry(450, 310, 300, 50)
        self.button3.setFixedWidth(400)
        self.button3.setFont(btn_font_main)
        self.button3.setStyleSheet(btn_StyleSheet_main)
        print(self.count)
        self.button3.clicked.connect(self.click_button_3)

        self.button3.enterEvent = lambda event: self.button3.setStyleSheet(
            'background-color: #ffffff; color: #D2691E; border :1px solid; border-color: #D2691E;')
        self.button3.leaveEvent = lambda event: self.button3.setStyleSheet(
            'background-color: #ffffff; color: #4682B4; border :1px solid;')

    def click_button_1(self):

        # строка для ввода текста и кнопка для его сохранения в переменную
        self.input_text = QLineEdit(self)
        self.input_text.setGeometry(450, 150, 300, 50)
        self.input_text.setFixedWidth(400)
        self.input_text.setFont(QFont('Impact', 25))
        self.input_text.setStyleSheet('background-color: #ffffff; color: #4682B4; border :1px solid;')
        self.input_text.setPlaceholderText("Введите текст")
        self.input_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_text.textChanged.connect(self.input_text_changed)

        # кнопка для сохранения введенного текста в переменную
        self.button_save_input_text = QtWidgets.QPushButton(self)
        self.button_save_input_text.setText("Сохранить")
        self.button_save_input_text.setGeometry(450, 230, 300, 50)
        self.button_save_input_text.setFixedWidth(400)
        self.button_save_input_text.setFont(QFont('Impact', 25))
        self.button_save_input_text.setStyleSheet('background-color: #ffffff; color: #4682B4; border :1px solid;')
        self.button_save_input_text.clicked.connect(self.buttonClicked_save_input_text)
        self.button_save_input_text.enterEvent = lambda event: self.button_save_input_text.setStyleSheet(
            'background-color: #ffffff; color: #D2691E; border :1px solid; border-color: #D2691E;')
        self.button_save_input_text.leaveEvent = lambda event: self.button_save_input_text.setStyleSheet(
            'background-color: #ffffff; color: #4682B4; border :1px solid;')

        # показать строку для ввода текста и кнопку для сохранения введенного текста
        self.input_text.show()
        self.button_save_input_text.show()

        # после нажатия кнопки Сохранить, скрыть строку для ввода текста и кнопку для сохранения введенного текста
        self.button_save_input_text.clicked.connect(self.input_text.hide)
        self.button_save_input_text.clicked.connect(self.button_save_input_text.hide)
        self.button_save_input_text.clicked.connect(self.save_crypto)

        print('button 1')
        self.count += 1
        print(self.count)

    def save_crypto(self):
        # read way from input_text
        way = self.input_text.text()
        # создать папку в проекте для хранения ключей с названием way
        if os.path.exists(way):
            shutil.rmtree(way)
        if not os.path.exists(way):
            os.mkdir(way)

        # классы для генерации ключей и их сериализации
        self.sym_encrpt = symmetrical_encrpt.SymmetricalEncryption(256, way)
        self.asym_encrpt = asymmetric_encrpt.AsymmetricEncryption(256, way)
        # сохранение ключей в файлы
        self.sym_encrpt.serialization_symmetric_key()

        self.asym_encrpt.serialization_asymmetric_private_key()
        self.asym_encrpt.serialization_asymmetric_public_key()

        self.asym_encrpt.encryption_symmetric_key(self.sym_encrpt.get_symmetric_key())


    def buttonClicked_save_input_text(self):
        self.text = self.input_text.text()
        # print(self.text)
        self.input_text.close()

    def input_text_changed(self, text):
        print(text)

    def click_button_2(self):
        print('button 2')
        if self.count == 0:
            self.buttonClicked_fail()
        else:
            way_file = str(QFileDialog.getOpenFileName(caption='Выберите файл для шифрования', filter='*.txt'))
            way_file = way_file.split('\'')[1]
            self.asym_encrpt.encryption_text(way_file)
            way_dcr = os.path.join(self.way, 'decrypted_file.txt')
            self.buttonSuccess_shifr(way_dcr)










    def click_button_3(self):
        print('button 3')
        if self.count == 0:
            self.buttonClicked_fail()
        else:
            self.buttonSuccess_deshifr()

    def buttonClicked_fail(self):
        self.statusBar().showMessage("Сначала сгенерируйте ключи", 2000)
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #4682B4;")

    def buttonSuccess_gen(self):
        self.statusBar().showMessage("Ключи сгенерированы", 2000)
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #4682B4;")

    def buttonSuccess_shifr(self,way_file):
        self.statusBar().showMessage(f"Текст зашифрован в файл {way_file}", 4000)
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #4682B4;")

    def buttonSuccess_deshifr(self):
        self.statusBar().showMessage("Текст дешифрован", 2000)
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #4682B4;")

    def buttonSuccess_save(self):
        self.statusBar().showMessage("Сохранено", 2000)
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #4682B4;")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
