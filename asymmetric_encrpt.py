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

settings = {
    'initial_file': 'path/to/inital/file.txt',
    'encrypted_file': 'path/to/encrypted/file.txt',
    'decrypted_file': 'path/to/decrypted/file.txt',
    'symmetric_key': 'path/to/symmetric/key.txt',
    'public_key': 'path/to/public/key.pem',
    'secret_key': 'path/to/secret/key.pem',
}


class AsymmetricEncryption:

    def __init__(self, decrypted_file: str = settings['decrypted_file'],
                 chiphed_file: str = settings["encrypted_file"], public_key_file: str = settings["public_key"],
                 private_key_file: str = settings["private_key"]):
        self.public_pem = public_key_file
        self.private_pem = private_key_file
        self.encryption_file = chiphed_file
        self.decrypted_file = decrypted_file

    # генерация пары ключей для асимметричного алгоритма шифрования
    def generation_asymmetric_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def generation_symmetric_key(self):
        return os.urandom(32)

    # сериализация приватного ключа в формате PEM
    def serialization_asymmetric_private_key(self, keys):
        private_key = keys[0]
        try:
            with open(self.private_pem, 'wb') as private_out:
                private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                            encryption_algorithm=serialization.NoEncryption()))
        except:
            logging.error(f"error in file")

    # сериализация публичного ключа в формате PEM
    def serialization_asymmetric_public_key(self, keys):
        public_key = keys[1]
        try:
            with open(self.public_pem, 'wb') as public_out:
                public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                         format=serialization.PublicFormat.SubjectPublicKeyInfo))
        except:
            logging.error(f"error in file")

    # десериализация открытого ключа
    def get_public_key(self):
        with open(self.public_pem, 'rb') as pem_in:
            public_bytes = pem_in.read()
        d_public_key = load_pem_public_key(public_bytes)
        return d_public_key

    # десериализация закрытого ключа
    def get_private_key(self):
        with open(self.private_pem, 'rb') as pem_in:
            private_bytes = pem_in.read()
        d_private_key = load_pem_private_key(private_bytes, password=None, )
        return d_private_key

    # Зашифровать ключ симметричного шифрования открытым ключом и сохранить по указанному пути.
    def encryption_symmetric_key(self, public_key, symmetric_key):
        try:
            with open(self.settings['symmetric_key'], 'wb') as file:
                file.write(public_key.encrypt(
                    symmetric_key,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None)))
        except:
            logging.error(f"error in file")

    # шифрование текста при помощи RSA-OAEP
    def encryption_text(self, public_key, text):
        try:
            ciphertext = public_key.encrypt(
                text.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None))
            return ciphertext
        except:
            logging.error(f"error in file")

    # расшифровка текста при помощи RSA-OAEP
    def decryption_text(self, private_key, ciphertext):
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
            with open(self.encryption_file, 'wb') as file:
                file.write(ciphertext)
        except:
            logging.error(f"error in file")

    # десериализация шифрованного текста
    def deserialization_encryption_text(self):
        try:
            with open(self.encryption_file, 'rb') as file:
                ciphertext = file.read()
            return ciphertext
        except:
            logging.error(f"error in file")

    # сериализация расшифрованного текста
    def serialization_decryption_text(self, plaintext):
        try:
            with open(self.decrypted_file, 'wb') as file:
                file.write(plaintext)
        except:
            logging.error(f"error in file")

    # десериализация расшифрованного текста
    def deserialization_decryption_text(self):
        try:
            with open(self.decrypted_file, 'rb') as file:
                plaintext = file.read()
            return plaintext
        except:
            logging.error(f"error in file")
