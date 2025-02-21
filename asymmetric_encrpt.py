import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
import logging
from cryptography.hazmat.primitives.ciphers.algorithms import ChaCha20


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

    def generation_asymmetric_key(self) -> tuple:
        """
        Генерация пары ключей для асимметричного алгоритма шифрования
        :param size: размер ключа
        :return:
        """
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = keys
        public_key = keys.public_key()
        return private_key, public_key

    def serialization_asymmetric_private_key(self) -> None:
        """
        Сериализация приватного ключа в формате PEM
        :param private_key: приватный ключ
        :return: None
        """
        private_key = self.private_key
        try:
            with open(self.settings['private_key'], 'wb') as private_out:
                private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                            encryption_algorithm=serialization.NoEncryption()))
        except:
            logging.error("error in file")

    def serialization_asymmetric_public_key(self) -> None:
        """
        Сериализация публичного ключа в формате PEM
        :return: None
        """
        public_key = self.public_key
        try:
            with open(self.settings['public_key'], 'wb') as public_out:
                public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                         format=serialization.PublicFormat.SubjectPublicKeyInfo))
        except:
            logging.error("error in file")

    def get_public_key(self) -> bytes:
        """
        Функция десериализации открытого ключа
        :return: открытый ключ
        """
        with open(self.settings['public_key'], 'rb') as pem_in:
            public_bytes = pem_in.read()
        d_public_key = load_pem_public_key(public_bytes)
        return d_public_key

    def get_private_key(self) -> bytes:
        """
        Функция десериализации закрытого ключа
        :return: закрытый ключ
        """
        with open(self.settings['privet_key'], 'rb') as pem_in:
            private_bytes = pem_in.read()
        d_private_key = load_pem_private_key(private_bytes, password=None, )
        return d_private_key

    def deserialization_asymmetric_private_key(self, way) -> bytes:
        """
        Десериализация закрытого ключа с указанным путем
        :param way: путь к закрытому ключу
        :return: закрытый ключ
        """
        try:
            with open(way, 'rb') as pem_in:
                private_bytes = pem_in.read()
        except OSError as err:
            logging.warning(f"{err} ошибка при чтении из файла {way}")
        else:
            logging.info("Приватный ключ прочитан")
        d_private_key = load_pem_private_key(private_bytes, password=None, )
        self.private_key = d_private_key

    def deserialization_asymmetric_public_key(self, way) -> None:
        """
        Десериализация открытого ключа с указанным путем
        :param way: путь к открытому ключу
        :return: None
        """
        try:
            with open(way, 'rb') as pem_in:
                public_bytes = pem_in.read()
        except OSError as err:
            logging.warning(f"{err} ошибка при чтении из файла {way}")
        else:
            logging.info("Публичный ключ прочитан")
        d_public_key = load_pem_public_key(public_bytes)
        self.public_key = d_public_key

    def encryption_text(self, way_file: str) -> None:
        """
        Функция шифрования текста алгоритмом RSA-OAEP
        :param way_file:
        :return: None
        """

        symmetric_key = self.decryption_symmetric_key()

        try:
            with open(way_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except OSError as err:
            logging.warning(f"{err} ошибка при чтении из файла {way_file}")
        else:
            logging.info("Текст прочитан")

        padder = sym_padding.ANSIX923(128).padder()
        padded_text = padder.update(bytes(text, 'utf-8')) + padder.finalize()
        nonce = os.urandom(16)
        algorithm = algorithms.ChaCha20(symmetric_key, nonce)
        cipher = Cipher(algorithm, mode=None)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_text) + encryptor.finalize()

        try:
            with open(self.settings['iv_path'], 'wb') as key_file:
                key_file.write(nonce)
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

    def decryption_text(self, way_file) -> None:
        """
            Функция расшифровки текста алгоритма 3DES

            Возвращает путь до расщифрованного файла
        """
        symmetric_key = self.decryption_symmetric_key()

        try:
            with open(way_file, 'rb') as f:
                ciphertext = f.read()
        except OSError as err:
            logging.warning(
                f"{err} ошибка при чтении из файла {way_file}")
        try:
            with open(self.settings['iv_path'], "rb") as f:
                nonce = f.read()
        except OSError as err:
            logging.warning(
                f"{err} ошибка при чтении из файла {self.settings['iv_path']}")
        algorithm = algorithms.ChaCha20(symmetric_key, nonce)
        cipher = Cipher(algorithm, mode=None)
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = sym_padding.ANSIX923(128).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        try:
            with open(self.settings['decrypted_file'], 'wb') as f:
                f.write(unpadded_dc_text)
        except OSError as err:
            logging.warning(
                f"{err} ошибка при записи в файл {self.settings['decrypted_file']}")
        else:
            logging.info("Текст расшифрован")

    def encryption_symmetric_key(self, key: bytes) -> None:
        """
            Функция шифрования ключа симметричного шифрования

            Возвращает путь до зашифрованного ключа
        """
        try:
            ciphertext = self.public_key.encrypt(key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                   algorithm=hashes.SHA256(), label=None))
            with open(self.settings['encr_symmetric_key'], 'wb') as file:
                file.write(ciphertext)
        except:
            logging.error("error in file")

    def decryption_symmetric_key(self) -> bytes:
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
            symmetric_decr_key = private_key.decrypt(encr_symm_key,
                                                     padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                  algorithm=hashes.SHA256(), label=None))
            with open(self.settings['decr_symmetric_key'], 'wb') as file:
                file.write(symmetric_decr_key)
        except:
            logging.error("error in file")

        return symmetric_decr_key
