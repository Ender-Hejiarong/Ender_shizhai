from scapy.all import *
import re
from concurrent.futures import ProcessPoolExecutor
class Nids:
    def __init__(self):
        self.netcard = None
        self.feature_library=[{'ID':1001,'NAME':'SQL_injection_select','Pattern':r'select\s+.*\s+from','severity':'High','description':'Someone is accessing the database!'},
                            {'ID':1002,'NAME':'Sensitive_File_Access','Pattern':r'etc/passwd|boot\.ini','severity':'Critical','description':'Someone is accessing sensitive system files!'}]
    def start(self):
        interfaces = get_if_list()
        print("\n--- Available network cards list ---")
        for idx, iface in enumerate(interfaces):
            print(f"[{idx}] {iface}")
        while True:
            try:
                idx = int(input("\nPlease select the network card number (enter a number): "))
                if 0 <= idx < len(interfaces):
                    self.netcard = interfaces[idx]
                    print(f"[+] Successfully locked the network card: {self.netcard}")
                    break
                else:
                    print("[!]Error: Index out of range, please select again. ")
            except ValueError as v:
                print("[!] Error: Please enter a valid number!",v)
    def dpi_analyze(self,pkt):
        if pkt.haslayer('IP') and pkt.haslayer('Raw'):
            try:
                payload=pkt['Raw'].load.decode('utf-8',errors='ignore')
                for rule in self.feature_library:
                    if re.search(rule['Pattern'],payload,re.I | re.S):
                        self.alert(pkt,rule,payload)
            except Exception as e:
                print("Oh no, I can't figure it out!",e)
    def alert(self,pkt,rule,payload):
        src=pkt[IP].src
        dst=pkt[IP].dst
        print(f"[+]DPI Alarm types: {rule['NAME']}")
        print(f'[+]Flow direction: {src}————>{dst}')
        print(f'[+]Illegal clips: {payload[:50].strip()}...')
        print(f"{rule['description']}")
    def run(self):
        print(f"[+]Starting moniter on {self.netcard}")
        self.executor=ProcessPoolExecutor(max_workers=10)
        def async_analyse(pkt):
            self.executor.submit(self.dpi_analyze,pkt)
            sniff(ifaces=self.netcard,prn=async_analyse,store=0)
if __name__=='__main__':
    Ender_nids=Nids()
    Ender_nids.start()
    Ender_nids.run()