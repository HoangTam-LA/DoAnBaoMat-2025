import socket
import time
from common import send_data
from config import ENCRYPTION_METHOD
def simulate_attack():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 9999))
        print("\n💣 Kết nối tấn công...")
        attack_data = [
            int(time.time()),  
            54321,            
            80,               
            0.001,            
            9999999,          
            0,              
            0,               
            10000,         
            9999999,        
            0,                
            0,                
            255,           
            255,            
            1,          
            9999,          
            0,               
            500             
        ]
    
        send_data(s, attack_data, method=ENCRYPTION_METHOD)
        print("\n💥 Đã gửi dữ liệu tấn công")
if __name__ == "__main__":
    simulate_attack()