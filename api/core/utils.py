import os
import binascii


def generate_token(length: int = 20):
    return binascii.hexlify(os.urandom(length)).decode()