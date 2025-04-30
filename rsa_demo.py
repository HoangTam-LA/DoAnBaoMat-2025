from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Đọc khóa từ file
with open("keys/private_key.pem", "rb") as f:
    private_key = RSA.import_key(f.read())
with open("keys/public_key.pem", "rb") as f:
    public_key = RSA.import_key(f.read())

def encrypt(data: str) -> str:
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(data.encode())
    return base64.b64encode(encrypted).decode()

def decrypt(enc_data: str) -> str:
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(base64.b64decode(enc_data))
    return decrypted.decode()