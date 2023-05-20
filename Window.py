import os
import shutil
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolTip, QLabel, QFileDialog, QLineEdit
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
        self.button2.setGeometry(450, 390, 300, 50)
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


        self.button4 = QtWidgets.QPushButton(self)
        self.button4.setText("Считать ключи из файла")
        self.button4.setGeometry(450, 230, 300, 50)
        self.button4.setFixedWidth(400)
        self.button4.setFont(btn_font_main)
        self.button4.setStyleSheet(btn_StyleSheet_main)
        self.button4.clicked.connect(self.click_button_4)

        self.button4.enterEvent = lambda event: self.button4.setStyleSheet(
            'background-color: #ffffff; color: #D2691E; border :1px solid; border-color: #D2691E;')
        self.button4.leaveEvent = lambda event: self.button4.setStyleSheet(
            'background-color: #ffffff; color: #4682B4; border :1px solid;')
    def click_button_1(self):
        """
         Click button 1
        :return:
        """
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

        self.count += 1

    def save_crypto(self) -> None:
        """
        Save keys in files
        :return:
        """
        way = self.input_text.text()
        if os.path.exists(way):
            shutil.rmtree(way)
        if not os.path.exists(way):
            os.mkdir(way)

        self.sym_encrpt = symmetrical_encrpt.SymmetricalEncryption(256, way)
        self.asym_encrpt = asymmetric_encrpt.AsymmetricEncryption(256, way)

        self.sym_encrpt.serialization_symmetric_key()

        self.asym_encrpt.serialization_asymmetric_private_key()
        self.asym_encrpt.serialization_asymmetric_public_key()

        self.asym_encrpt.encryption_symmetric_key(self.sym_encrpt.get_symmetric_key())

    def buttonClicked_save_input_text(self) -> None:
        """
        Save input text in variable
        :return:
        """
        self.text = self.input_text.text()
        self.input_text.close()

    def input_text_changed(self, text: str) -> None:
        """
        Show input text
        :param text:
        :return:
        """
        print(text)

    def click_button_2(self) -> None:
        """
        Click button 2
        :return:
        """
        logging.info('button 2')
        if self.count == 0:
            self.buttonClicked_fail()
        else:
            way_file = str(QFileDialog.getOpenFileName(caption='Выберите файл для шифрования', filter='*.txt'))
            way_file = way_file.split('\'')[1]
            self.asym_encrpt.encryption_text(way_file)
            way_encr = os.path.join(self.way, 'encrypted_file.txt')
            self.buttonSuccess_shifr(way_encr)

    def click_button_3(self) -> None:
        """
        Click button 3
        :return:
        """
        logging.info('button 3')
        if self.count == 0:
            self.buttonClicked_fail()
        else:
            way_file = str(QFileDialog.getOpenFileName(caption='Выберите файл для расшифрования', filter='*.txt'))
            way_file = way_file.split('\'')[1]
            self.asym_encrpt.decryption_text(way_file)
            way_decr = os.path.join(self.way, 'decrypted_file.txt')
            self.buttonSuccess_shifr(way_decr)
            self.buttonSuccess_deshifr(way_decr)

    def click_button_4(self) -> None:
        """
        Click button 4
        :return:
        """
        logging.info('button 4')

        way = str(QFileDialog.getExistingDirectory(caption='Выберите папку с ключами'))
        self.way = way

        way_public = os.path.join(way, 'public_key.txt')
        way_private = os.path.join(way, 'private_key.txt')
        way_symmetric = os.path.join(way, 'encr_symmetric_key.txt')

        self.sym_encrpt = symmetrical_encrpt.SymmetricalEncryption(256, way)
        self.asym_encrpt = asymmetric_encrpt.AsymmetricEncryption(256, way)

        self.asym_encrpt.deserialization_asymmetric_public_key(way_public)
        self.asym_encrpt.deserialization_asymmetric_private_key(way_private)
        self.sym_encrpt.deserialization_symmetric_key_way(way_symmetric)


        self.count += 1


    def buttonClicked_fail(self) -> None:
        logging.error('Сначала сгенерируйте ключи или загрузите из файла')
        self.statusBar().showMessage("Сначала сгенерируйте ключи или загрузите из файла ", 4000)
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #4682B4;")

    def buttonSuccess_gen(self) -> None:
        logging.info('Ключи сгенерированы')
        self.statusBar().showMessage("Ключи сгенерированы", 4000)
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #4682B4;")

    def buttonSuccess_shifr(self, way_file: str) -> None:
        logging.info(f"Текст зашифрован в файл {way_file}")
        self.statusBar().showMessage(f"Текст зашифрован в файл {way_file}", 4000)
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #4682B4;")

    def buttonSuccess_deshifr(self, way_file: str) -> None:
        logging.info(f"Текст дешифрован в файл {way_file}")
        self.statusBar().showMessage(f"Текст дешифрован в файл {way_file}", 4000)
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #4682B4;")

    def buttonSuccess_save(self) -> None:
        logging.info('Сохранено')
        self.statusBar().showMessage("Сохранено", 4000)
        self.statusBar().setStyleSheet("background-color: #ffffff; color: #4682B4;")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
