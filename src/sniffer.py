from scapy.all import sniff, TCP, Raw, IP

def packet_handler(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        data = pkt[Raw].load
        src = f"{pkt[IP].src}:{pkt[TCP].sport}"
        dst = f"{pkt[IP].dst}:{pkt[TCP].dport}"
        print("SNIFFER: ")
        print(f"{src} → {dst}")
        print(data.decode('utf-8', errors='replace'))
        print("---")

print("Čmuchám čmuchám co se na sítí děje...")
sniff(prn=packet_handler, store=False)
