import socket
import time
from common import send_data
from config import ENCRYPTION_METHOD
def simulate_attack():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 9999))
        print("\n💣 Kết nối tấn công...")
        
        # Dữ liệu tấn công DoS (đủ 17 features theo đúng thứ tự)
        attack_data = [
            int(time.time()),  # ts (timestamp hiện tại)
            54321,            # src_port ngẫu nhiên
            80,               # dst_port (HTTP)
            0.001,            # duration cực ngắn (đặc trưng DoS)
            9999999,          # src_bytes cực lớn (>10MB)
            0,                # dst_bytes = 0 (không phản hồi)
            0,                # missed_bytes
            10000,            # src_pkts rất cao
            9999999,          # src_ip_bytes
            0,                # dst_pkts = 0
            0,                # dst_ip_bytes = 0
            255,              # dns_qclass bất thường
            255,              # dns_qtype bất thường  
            1,                # dns_rcode lỗi
            9999,             # http_request_body_len lớn
            0,                # http_response_body_len = 0
            500               # http_status_code lỗi server
        ]
        
        send_data(s, attack_data, method=ENCRYPTION_METHOD)
        print("\n💥 Đã gửi dữ liệu tấn công")
        # time.sleep(1)  # Đợi server xử lý

if __name__ == "__main__":
    simulate_attack()