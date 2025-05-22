import socket
from common import send_data, recv_data
from config import ENCRYPTION_METHOD
# Dữ liệu mẫu
test_data = [
    1554198358,
    1883,        
    52976,      
    0.5,      
    1000,        
    2000,        
    0,          
    10,         
    50000,       
    5,           
    30000,      
    0, 0, 0,     
    0, 0, 0 
]
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("localhost", 9999))
    print("\n🔗 Đã kết nối tới server")
    
    send_data(s, test_data, method=ENCRYPTION_METHOD)
    print("\n🔄 Đang chờ phản hồi...")
    
    result = recv_data(s, method=ENCRYPTION_METHOD)
    print(f"\n🎯 Kết quả: {'NGUY HIỂM' if result == 1 else 'AN TOÀN'}")