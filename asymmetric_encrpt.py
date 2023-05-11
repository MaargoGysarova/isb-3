import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from PyQt6 import QtWidgets
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import logging


class AsymmetricEncryption:

    def __init__(self, size: int, way: str) -> None:
        self.size = int(size / 8)
        self.way = way
        self.settings = {
            'initial_file': os.path.join(self.way, 'initial_file.txt'),
            'encrypted_file': os.path.join(self.way, 'encrypted_file.txt'),
            'decrypted_file': os.path.join(self.way, 'decrypted_file.txt'),
            'symmetric_key': os.path.join(self.way, 'symmetric_key.txt'),
            'public_key': os.path.join(self.way, 'public_key.txt'),
            'private_key': os.path.join(self.way, 'private_key.txt'),
            'encr_symmetric_key': os.path.join(self.way, 'encr_symmetric_key.txt'),
            'decr_symmetric_key': os.path.join(self.way, 'decr_symmetric_key.txt'),
            'iv_path': os.path.join(self.way, 'iv_path.txt'),
        }
        self.private_key, self.public_key = self.generation_asymmetric_key()

    # генерация пары ключей для асимметричного алгоритма шифрования
    def generation_asymmetric_key(self):
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = keys
        public_key = keys.public_key()
        return private_key, public_key

    # сериализация приватного ключа в формате PEM
    def serialization_asymmetric_private_key(self):
        private_key = self.private_key
        try:
            with open(self.settings['private_key'], 'wb') as private_out:
                private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                            encryption_algorithm=serialization.NoEncryption()))
        except:
            logging.error(f"error in file")

    # сериализация публичного ключа в формате PEM
    def serialization_asymmetric_public_key(self):
        public_key = self.public_key
        try:
            with open(self.settings['public_key'], 'wb') as public_out:
                public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                         format=serialization.PublicFormat.SubjectPublicKeyInfo))
        except:
            logging.error(f"error in file")

    # десериализация открытого ключа
    def get_public_key(self):
        with open(self.settings['public_key'], 'rb') as pem_in:
            public_bytes = pem_in.read()
        d_public_key = load_pem_public_key(public_bytes)
        return d_public_key

    # десериализация закрытого ключа
    def get_private_key(self):
        with open(self.settings['privet_key'], 'rb') as pem_in:
            private_bytes = pem_in.read()
        d_private_key = load_pem_private_key(private_bytes, password=None, )
        return d_private_key

    # шифрование текста при помощи RSA-OAEP
    def encryption_text(self, way_file):
        # расшифровка симметричного ключа
        symmetric_key = self.decryption_symmetric_key()
        # чтение файла
        try:
            with open(way_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except OSError as err:
            logging.warning(f"{err} ошибка при чтении из файла {way_file}")
        else:
            logging.info("Текст прочитан")
        # шифрование текста
        padder = sym_padding.ANSIX923(128).padder()
        padded_text = padder.update(bytes(text, 'utf-8')) + padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_text) + encryptor.finalize()

        try:
            with open(self.settings['iv_path'], 'wb') as key_file:
                key_file.write(iv)
        except OSError as err:
            logging.warning(
                f"{err} ошибка при записи в файл {self.settings['iv_path']}")
        try:
            with open(self.settings['encrypted_file'], 'wb') as f_text:
                f_text.write(ciphertext)
        except OSError as err:
            logging.warning(
                f"{err} ошибка при записи в файл {self.settings['encrypted_file']}")
        else:
            logging.info("Тескт зашифрован")


    # расшифровка текста при помощи RSA-OAEP
    def decryption_text(self, ciphertext):
        private_key = self.private_key
        try:
            plaintext = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None))
            return plaintext
        except:
            logging.error(f"error in file")

    # сериализация шифрованного текста
    def serialization_encryption_text(self, ciphertext):
        try:
            with open(self.settings['encrypted_file'], 'wb') as file:
                file.write(ciphertext)
        except:
            logging.error(f"error in file")

    # десериализация шифрованного текста
    def deserialization_encryption_text(self):
        try:
            with open(self.settings['encrypted_file'], 'rb') as file:
                ciphertext = file.read()
            return ciphertext
        except:
            logging.error(f"error in file")

    # сериализация расшифрованного текста
    def serialization_decryption_text(self, plaintext):
        try:
            with open(self.settings['decrypted_file'], 'wb') as file:
                file.write(plaintext)
        except:
            logging.error(f"error in file")

    # десериализация расшифрованного текста
    def deserialization_decryption_text(self):
        try:
            with open(self.settings['decrypted_file'], 'rb') as file:
                plaintext = file.read()
            return plaintext
        except:
            logging.error(f"error in file")

    # Зашифровать ключ симметричного шифрования открытым ключом и сохранить по указанному пути.
    def encryption_symmetric_key(self, key):
        try:
            ciphertext = self.public_key.encrypt(key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                   algorithm=hashes.SHA256(), label=None))
            with open(self.settings['encr_symmetric_key'], 'wb') as file:
                file.write(ciphertext)
        except:
            logging.error(f"error in file")

    # Расшифровать ключ симметричного шифрования закрытым ключом и сохранить по указанному пути.
    def decryption_symmetric_key(self)->bytes:
        """
                Функция расшифровки ключа симметричного шифрования

                Возвращает расшифрованный симметричный ключ
        """
        try:
            with open(self.settings['private_key'], "rb") as f:
                private_key = serialization.load_pem_private_key(
                    f.read(), password=None)
        except OSError as err:
            logging.warning(
                f"{err} ошибка при чтении из файла {self.settings['private_key']}")

        try:
            with open(self.settings['encr_symmetric_key'], 'rb') as file:
                encr_symm_key = file.read()
        except OSError as err:
            logging.warning(
                f"{err} ошибка при чтении из файла {self.settings['encr_symmetric_key']}")

        try:
            symmetric_decr_key = private_key.decrypt(encr_symm_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                          algorithm=hashes.SHA256(), label=None))
            with open(self.settings['decr_symmetric_key'], 'wb') as file:
                file.write(symmetric_decr_key)
        except:
            logging.error(f"error in file")

        return symmetric_decr_key

