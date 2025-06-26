import os
import subprocess
from scapy.all import rdpcap, TCP, IP
packets = rdpcap("fragments.pcap")
streams = {}
for pkt in packets:
    if TCP in pkt and pkt[TCP].payload:
        stream_id = (pkt[IP].src, pkt[IP].dst, pkt[TCP].sport, pkt[TCP].dport)
        streams.setdefault(stream_id, []).append((pkt[TCP].seq, bytes(pkt[TCP].payload)))
output_dir = "streams_output"
os.makedirs(output_dir, exist_ok=True)
combined_data = b""
for stream_id, segments in streams.items():
    segments.sort(key=lambda x: x[0])
    data = b''.join(seg[1] for seg in segments)
    combined_data += data
    filename = f"{output_dir}/stream_{stream_id[0].replace('.', '_')}_{stream_id[2]}_{stream_id[1].replace('.', '_')}_{stream_id[3]}.bin"
    with open(filename, "wb") as f:
        f.write(data)
    os.system(f"file {filename}")
    os.system(f"binwalk {filename}")
    os.system(f"zsteg {filename} || echo 'Not a supported image for zsteg.'")
with open("final.bin", "wb") as f:
    f.write(combined_data)
print("\nsaved to final.bin")
from scapy.all import rdpcap, TCP, IP
packets = rdpcap('fragments.pcap')
streams = {}
for pkt in packets:
    if TCP in pkt and pkt[TCP].payload:
        stream_id = (pkt[IP].src, pkt[IP].dst, pkt[TCP].sport, pkt[TCP].dport)
        if stream_id not in streams:
            streams[stream_id] = []
        streams[stream_id].append((pkt[TCP].seq, bytes(pkt[TCP].payload)))
for stream_id, segments in streams.items():
    segments.sort(key=lambda x: x[0])
    data = b''.join(seg[1] for seg in segments)
    filename = f"stream_{stream_id[0].replace('.', '_')}_{stream_id[2]}_{stream_id[1].replace('.', '_')}_{stream_id[3]}.bin"
    with open(filename, "wb") as f:
        f.write(data)
    print(f"Wrote {filename}")
