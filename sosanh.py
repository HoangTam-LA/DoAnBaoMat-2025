from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time
data_list = [
    1554198358, 1883, 52976, 0.5, 1000, 2000, 0, 10, 50000,
    5, 30000, 0, 0, 0, 0, 0, 0
]
data = ','.join(map(str, data_list)).encode('utf-8')
def pad(data, block_size):
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len]) * pad_len
def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]
iterations = 1000
key_aes = get_random_bytes(16)
cipher_aes = AES.new(key_aes, AES.MODE_ECB)
start = time.perf_counter()
for _ in range(iterations):
    ciphertext_aes = cipher_aes.encrypt(pad(data, 16))
end = time.perf_counter()
encrypt_time_aes = (end - start) / iterations * 1000  # ms
start = time.perf_counter()
for _ in range(iterations):
    plaintext_aes = unpad(cipher_aes.decrypt(ciphertext_aes))
end = time.perf_counter()
decrypt_time_aes = (end - start) / iterations * 1000  # ms
key_des = get_random_bytes(8)
cipher_des = DES.new(key_des, DES.MODE_ECB)
start = time.perf_counter()
for _ in range(iterations):
    ciphertext_des = cipher_des.encrypt(pad(data, 8))
end = time.perf_counter()
encrypt_time_des = (end - start) / iterations * 1000
start = time.perf_counter()
for _ in range(iterations):
    plaintext_des = unpad(cipher_des.decrypt(ciphertext_des))
end = time.perf_counter()
decrypt_time_des = (end - start) / iterations * 1000
key_rsa = RSA.generate(2048)
cipher_rsa = PKCS1_OAEP.new(key_rsa)
start = time.perf_counter()
for _ in range(iterations):
    ciphertext_rsa = cipher_rsa.encrypt(data)
end = time.perf_counter()
encrypt_time_rsa = (end - start) / iterations * 1000
start = time.perf_counter()
for _ in range(iterations):
    plaintext_rsa = cipher_rsa.decrypt(ciphertext_rsa)
end = time.perf_counter()
decrypt_time_rsa = (end - start) / iterations * 1000
print(f"AES Encrypt: {encrypt_time_aes:.6f} ms, Decrypt: {decrypt_time_aes:.6f} ms")
print(f"DES Encrypt: {encrypt_time_des:.6f} ms, Decrypt: {decrypt_time_des:.6f} ms")
print(f"RSA Encrypt: {encrypt_time_rsa:.6f} ms, Decrypt: {decrypt_time_rsa:.6f} ms")
