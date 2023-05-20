import os
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import logging
from cryptography.hazmat.primitives.ciphers.algorithms import ChaCha20





class SymmetricalEncryption:
    def __init__(self, size: int, way: str) -> None:
        self.size = int(size / 8)
        self.way = way
        self.settings = {
            'initial_file': os.path.join(self.way, 'initial_file.txt'),
            'encrypted_file': os.path.join(self.way, 'encrypted_file.txt'),
            'decrypted_file': os.path.join(self.way, 'decrypted_file.txt'),
            'symmetric_key': os.path.join(self.way, 'symmetric_key.txt'),
            'public_key': os.path.join(self.way, 'public_key.txt'),
            'private_key': os.path.join(self.way, 'private_key.txt')
        }
        self.symm_key = self.generation_symmetric_key()

    # генерация симметричного ключа
    def generation_symmetric_key(self):
        """
        :param size: размер ключа
        :return:
        """
        return os.urandom(self.size)

    def get_symmetric_key(self):
        return self.symm_key

    # сериализация симметричного ключа
    def serialization_symmetric_key(self):
        try:
            with open(self.settings['symmetric_key'], 'wb') as key_out:
                key_out.write(self.symm_key)
        except:
            logging.error(f"error in file")

    # десериализация симметричного ключа
    def deserialization_symmetric_key(self):
        try:
            with open(self.settings['symmetric_key'], 'rb') as key_in:
                key = key_in.read()
        except:
            logging.error(f"error in file")
        return key

    def deserialization_symmetric_key_way(self, way):
        try:
            with open(way, 'rb') as key_in:
                key = key_in.read()
        except OSError as err:
            logging.warning(f"{err} ошибка при чтении из файла {way}")
        else:
            logging.info("Приватный ключ прочитан")
        self.symm_key =  key