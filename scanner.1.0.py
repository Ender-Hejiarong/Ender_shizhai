import socket
import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor,as_completed
class scanner:
    def __init__(self,target,threads=50):
        self.target  = target
        self.threads = threads
        self.open_ports = {}
        self.lock = threading.Lock()
    def get_banner(self,conn,port):
        try:
            conn.settimeout(2)
            if port in [80,8080]:
                conn.sent(b"GET / HTTP/ l.l\r\nHost: " + self.target.encode() + b"\r\n\r\n")
            banner = conn.recv(1024).decode(errors='ignore').strip()
            return banner if banner else "The ports are not open."
        except Exception:
            return "Failed."
    def scan(self,port):
        time.sleep(random.uniform(0.01,0.1))
        try:
            s = socket.socket((socket.AF_INET,socket.SOCK_STREAM))
            s.settimeout(1.5)
            result = s.connect_ex((self.target,port))
            if result == 0:
                banner = self.get_banner(s,port)
                with self.lock:
                    self.open_ports[port] = banner
                    print(f"[*] [Found] Port {port:5} | Info : {banner[:60]}")
            s.close()
        except Exception:
            pass
    def run(self,start_port=1,end_port=1024):
        scan_list = list(range(start_port,end_port+1))
        random.shuffle(scan_list)
        with ThreadPoolExecutor(max_workers=self.threads) as excutor:
            excutor.map(self.scan,scan_list)