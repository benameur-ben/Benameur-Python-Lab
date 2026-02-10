"""
Benameur Python Lab - Professional Series
Network-Insight: Professional Port Scanner
--------------------------------------
Author: Benameur Mohamed
Entity: Benameur Soft
"""

import socket
import threading
from queue import Queue
import time
import logging

# Configure Logging / إعداد سجل العمليات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NetInsight")

class PortScanner:
    """
    Multithreaded network scanner for infrastructure audit.
    ماسح ضوئي للشبكة متعدد الخيوط لتدقيق البنية التحتية.
    """
    def __init__(self, target, threads=50):
        self.target = target
        self.threads = threads
        self.queue = Queue()
        self.open_ports = []

    def scan_port(self, port):
        """Standard socket scan / مسح قياسي للمنافذ"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                self.open_ports.append(port)
                logger.info(f"🔓 Port {port} is OPEN on {self.target}")
            sock.close()
        except:
            pass

    def worker(self):
        while not self.queue.empty():
            port = self.queue.get()
            self.scan_port(port)
            self.queue.task_done()

    def run(self, port_range=(1, 1024)):
        logger.info(f"🌐 Starting network scan on: {self.target}")
        for port in range(port_range[0], port_range[1]):
            self.queue.put(port)

        thread_list = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            thread_list.append(t)
            t.start()

        for t in thread_list:
            t.join()
        
        logger.info(f"✅ Scan complete for {self.target}. {len(self.open_ports)} ports found.")
        return sorted(self.open_ports)

if __name__ == "__main__":
    # Test on localhost / تجربة على المضيف المحلي
    target_ip = "127.0.0.1"
    scanner = PortScanner(target_ip)
    
    start_time = time.perf_counter()
    open_ports = scanner.run()
    end_time = time.perf_counter()
    
    print(f"\n--- Benameur-Soft Network Report ---")
    print(f"📍 Target: {target_ip}")
    print(f"📂 Open Ports: {open_ports if open_ports else 'None found'}")
    print(f"⏱️ Duration: {end_time - start_time:.2f} seconds")
