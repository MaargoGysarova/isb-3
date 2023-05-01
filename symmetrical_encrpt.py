import os
from cryptography.hazmat.primitives import padding as sym_padding
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


class SymmetricalEncryption:
    def __init__(self, size: int = 256, decrypt_file: str = settings["decrypted_file"], encrypt_file: str = settings["encrypted_file"],
                 symmetric_key_file: str = settings["symmetric_key"]) -> None:
        self.size = size
        self.sym_key_file = symmetric_key_file
        self.decrypt_file = decrypt_file
        self.encrypt_file = encrypt_file

    # генерация симметричного ключа
    def generation_symmetric_key(self):
        return os.urandom(self.size)

    def get_symmetric_key(self):
        return self.generation_symmetric_key()

    # сериализация симметричного ключа
    def serialization_symmetric_key(self):
        try:
            with open(self.sym_key_file, 'wb') as key_out:
                key_out.write(self.generation_symmetric_key())
        except:
            logging.error(f"error in file")

    # десериализация симметричного ключа
    def deserialization_symmetric_key(self):
        try:
            with open(self.sym_key_file, 'rb') as key_in:
                key = key_in.read()
        except:
            logging.error(f"error in file")
        return key

    def padding(self, data):
        padder = sym_padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    def serialize_padding(self, data):
        try:
            with open("padding.txt", 'wb') as file_out:
                file_out.write(data)
        except:
            logging.error(f"error in file")

    def deserialize_padding(self):
        try:
            with open("padding.txt", 'rb') as file_in:
                data = file_in.read()
        except:
            logging.error(f"error in file")
        return data

    # шифрование и паддинг текста симметричным алгоритмом
    def encrypt_simm(self, key, data):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.ChaCha20(self.deserialization_symmetric_key()), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = sym_padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return iv + ct

    # дешифрование и депаддинг текста симметричным алгоритмом
    def decrypt_simm(self, key, data):
        iv = data[:16]
        ct = data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ct) + decryptor.finalize()
        unpadder = sym_padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data
