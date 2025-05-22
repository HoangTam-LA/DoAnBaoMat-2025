import socket
import threading
import queue
import csv
import os
import time
import joblib
import tkinter as tk
from common import send_data, recv_data
import sys
from tkinter import ttk
import pandas as pd
from config import ENCRYPTION_METHOD

sys.stdout.reconfigure(encoding='utf-8')

gui_queue = queue.Queue()
connection_counter = 0
start_time = time.time()

# Tải mô hình và bộ chuẩn hóa
model_data = joblib.load("model/iot_attack_model.pkl")  # Load file đã lưu
model = model_data['model']
features = model_data['features']

# File ghi log
log_file = "attack_log.csv"
if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Source IP", "Prediction"])

def log_attack(timestamp, ip, prediction):
    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, ip, prediction])

# ==== GUI setup ====
root = tk.Tk()
root.title("🔥 Giám sát An ninh IoT - Real-time")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky="nsew")
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)

status_label = ttk.Label(frame, text="💤 Đang chờ kết nối...", font=("Arial", 14))
status_label.grid(row=0, column=0, pady=10)

tree = ttk.Treeview(frame, columns=("time", "ip", "label"), show="headings")
tree.heading("time", text="🕒 Thời gian")
tree.heading("ip", text="🌐 IP gửi")
tree.heading("label", text="🎯 Phân loại")
tree.grid(row=1, column=0, sticky="nsew")
tree.tag_configure('attack', background='#ffcccc')

def update_gui():
    try:
        while not gui_queue.empty():
            ts, ip, lbl = gui_queue.get()
            tags = ('attack',) if lbl == "🔥 TẤN CÔNG" else ()
            tree.insert("", 0, values=(ts, ip, lbl), tags=tags)
            status_label.config(text=f"🟢 Đang hoạt động | {ip}: {lbl}")
    except Exception as e:
        print(f"[GUI ERROR] {str(e)}")
    root.after(100, update_gui)

def handle_client(conn, addr):
    try:
        print(f"\n🔄 Xử lý kết nối từ {addr[0]}")
        data = recv_data(conn, method=ENCRYPTION_METHOD)
        print("📊 Dữ liệu nhận được:", data)
        feature_names = [
            'ts', 'src_port', 'dst_port', 'duration', 'src_bytes', 
            'dst_bytes', 'missed_bytes', 'src_pkts', 'src_ip_bytes', 
            'dst_pkts', 'dst_ip_bytes', 'dns_qclass', 'dns_qtype', 
            'dns_rcode', 'http_request_body_len', 'http_response_body_len', 
            'http_status_code'
        ]
        if len(data) != len(feature_names):
            missing = len(feature_names) - len(data)
            data += [0] * missing
            print(f"⚠️ Đã thêm {missing} giá trị mặc định")
        input_df = pd.DataFrame([data], columns=feature_names)
        print("\n🔥 Đặc điểm tấn công trong dữ liệu:")
        print(f"- Duration cực ngắn: {input_df['duration'].values[0]}")
        print(f"- Src_bytes cực lớn: {input_df['src_bytes'].values[0]}")
        print(f"- Src_pkts cao: {input_df['src_pkts'].values[0]}")
        print(f"- Tỉ lệ dst/src bytes: {input_df['dst_bytes'].values[0]/input_df['src_bytes'].values[0]:.6f}")
        if input_df['src_bytes'].values[0] > 1000000:
            print("⚠️ CẢNH BÁO: Lưu lượng gửi cực lớn - Dấu hiệu DoS")
        dos_conditions = [
            input_df['duration'].values[0] < 0.1,
            input_df['src_bytes'].values[0] > 1000000,
            input_df['src_pkts'].values[0] > 1000,
            input_df['dst_bytes'].values[0] < 10
        ]
        if sum(dos_conditions) >= 3:
            print("🔴 PHÁT HIỆN TẤN CÔNG QUA RULE-BASED")
            prediction = 1
        else:
            prediction = model.predict(input_df)[0]
        print(f"🔮 Kết quả: {'TẤN CÔNG' if prediction == 1 else 'BÌNH THƯỜNG'}")
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        label = "🔥 TẤN CÔNG" if prediction == 1 else "✅ BÌNH THƯỜNG"
        gui_queue.put((ts, addr[0], label))
        log_attack(ts, addr[0], label)
        
        send_data(conn, prediction, method=ENCRYPTION_METHOD)
    except Exception as e:
        print(f"⚠️ Lỗi: {str(e)}")
        send_data(conn, -1, method=ENCRYPTION_METHOD)
    finally:
        conn.close()
        print(f"🔌 Đã đóng kết nối với {addr[0]}")

def start_server():
    HOST, PORT = "localhost", 9999
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((HOST, PORT))
    srv.listen()
    status_label.config(text=f"🟢 Server đang chạy tại {HOST}:{PORT}")
    print(f"🚀 Server started on {HOST}:{PORT}")

    while True:
        conn, addr = srv.accept()
        print(f"🔗 Kết nối từ {addr[0]}")
        threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        ).start()

threading.Thread(target=start_server, daemon=True).start()
update_gui()
root.mainloop()
