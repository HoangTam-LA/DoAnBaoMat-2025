import socket
from common import send_data, recv_data
from config import ENCRYPTION_METHOD
# Dữ liệu mẫu
test_data = [
    1554198358,  # ts
    1883,        # src_port
    52976,       # dst_port
    0.5,         # duration
    1000,        # src_bytes
    2000,        # dst_bytes
    0,           # missed_bytes
    10,          # src_pkts
    50000,       # src_ip_bytes
    5,           # dst_pkts
    30000,       # dst_ip_bytes
    0, 0, 0,     # dns_qclass, dns_qtype, dns_rcode
    0, 0, 0      # http_request_body_len, http_response_body_len, http_status_code
]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("localhost", 9999))
    print("\n🔗 Đã kết nối tới server")
    
    send_data(s, test_data, method=ENCRYPTION_METHOD)
    print("\n🔄 Đang chờ phản hồi...")
    
    result = recv_data(s, method=ENCRYPTION_METHOD)
    print(f"\n🎯 Kết quả: {'NGUY HIỂM' if result == 1 else 'AN TOÀN'}")