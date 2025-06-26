from scapy.all import *
import os
streams = [
    (("10.0.0.1", 1234, "10.0.0.2", 80), b"flag{this"),
    (("10.0.0.3", 2345, "10.0.0.4", 80), b"_is_a_"),
    (("10.0.0.5", 3456, "10.0.0.6", 80), b"flag}")
]
packets = []
for (src_ip, sport, dst_ip, dport), payload in streams:
    ip = IP(src=src_ip, dst=dst_ip)
    tcp = TCP(sport=sport, dport=dport, seq=1000, ack=1, flags='PA')
    pkt = ip/tcp/payload
    packets.append(pkt)
output_path = "fragments.pcap"
wrpcap(output_path, packets)

output_path

