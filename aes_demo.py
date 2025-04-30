from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib
import os

# Sinh key từ chuỗi bí mật
raw_key = "iot_demo_key"
key = hashlib.md5(raw_key.encode()).digest()

def encrypt(data: str) -> str:
    iv = os.urandom(16)  # IV ngẫu nhiên
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data.encode(), AES.block_size)  # Đệm dữ liệu
    encrypted = cipher.encrypt(padded_data)  # Mã hóa
    # Trả về IV + ciphertext (base64)
    encrypted_data = base64.b64encode(iv + encrypted).decode()
    print(f"[LOG] Dữ liệu sau khi mã hóa (AES): {encrypted_data}")
    return encrypted_data

def decrypt(enc_data: str) -> str:
    enc_bytes = base64.b64decode(enc_data)  # Giải mã Base64
    iv = enc_bytes[:16]  # Lấy IV từ dữ liệu
    encrypted = enc_bytes[16:]  # Lấy phần mã hóa
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Khởi tạo cipher với IV
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)  # Giải mã và loại bỏ đệm
    decrypted_data = decrypted.decode()  # Trả về chuỗi đã giải mã
    print(f"[LOG] Dữ liệu sau khi giải mã (AES): {decrypted_data}")
    return decrypted_data
