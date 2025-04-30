from Crypto.PublicKey import RSA
import os

# Tạo thư mục keys nếu chưa tồn tại
if not os.path.exists("keys"):
    os.makedirs("keys")

# Tạo cặp khóa RSA 2048-bit
key = RSA.generate(2048)

# Lưu khóa riêng tư (Private Key)
with open("keys/private_key.pem", "wb") as priv_file:
    priv_file.write(key.export_key())

# Lưu khóa công khai (Public Key)
with open("keys/public_key.pem", "wb") as pub_file:
    pub_file.write(key.publickey().export_key())

print("✅ Đã tạo cặp khóa RSA và lưu vào thư mục 'keys'")
print("- private_key.pem: Khóa riêng tư (giữ bí mật)")
print("- public_key.pem: Khóa công khai (có thể phân phối)")