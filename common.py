import hashlib
import struct
import pickle
import time
import des_demo
import aes_demo
import rsa_demo
from config import ENCRYPTION_METHOD
raw_key = "iot_demo_key"
aes_key = hashlib.md5(raw_key.encode()).digest()

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise ConnectionError("Mất kết nối khi đang nhận dữ liệu")
        data += packet
    return data

def send_data(sock, data, method=ENCRYPTION_METHOD):
    try:
        print(f"[1/3] Chuẩn bị gửi dữ liệu...")
        start = time.perf_counter()
        if method == 'aes':
            encrypted = aes_demo.encrypt(str(data))
        elif method == 'des':
            encrypted = des_demo.encrypt(str(data))
        elif method == 'rsa':
            encrypted = rsa_demo.encrypt(str(data))
        print(f"[2/3] Mã hóa {method} xong ({time.perf_counter()-start:.6f}s)")
        pickled = pickle.dumps(encrypted)
        sock.sendall(struct.pack('>I', len(pickled)) + pickled)
        print(f"[3/3] Đã gửi {len(pickled)} bytes")
    except Exception as e:
        print(f"[LỖI] Gửi thất bại: {e}")
        raise

def recv_data(sock, method=ENCRYPTION_METHOD):
    try:
        print(f"[1/3] Đang nhận dữ liệu...")
        raw_msglen = recvall(sock, 4)
        msglen = struct.unpack('>I', raw_msglen)[0]
        encrypted = pickle.loads(recvall(sock, msglen))
        print(f"[2/3] Đã nhận {msglen} bytes")
        start = time.perf_counter()
        if method == 'aes':
            decrypted = aes_demo.decrypt(encrypted)
        elif method == 'des':
            decrypted = des_demo.decrypt(encrypted)
        elif method == 'rsa':
            decrypted = rsa_demo.decrypt(encrypted)
        print(f"[3/3] Giải mã {method} xong ({time.perf_counter()-start:.3f}s)")
        return eval(decrypted)
    except Exception as e:
        print(f"[LỖI] Nhận thất bại: {e}")
        raise