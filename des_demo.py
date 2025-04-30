from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib
import os

# DES cần key 8 byte
raw_key = "iot_demo_key"
key = hashlib.md5(raw_key.encode()).digest()[:8]  # Lấy 8 byte đầu

def encrypt(data: str) -> str:
    iv = os.urandom(8)  # IV 8 byte cho DES
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_data = pad(data.encode(), DES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(iv + encrypted).decode()

def decrypt(enc_data: str) -> str:
    enc_bytes = base64.b64decode(enc_data)
    iv = enc_bytes[:8]
    encrypted = enc_bytes[8:]
    cipher = DES.new(key, DES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted), DES.block_size)
    return decrypted.decode()