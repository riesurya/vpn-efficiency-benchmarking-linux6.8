import matplotlib.pyplot as plt
import numpy as np

# Data dari hasil benchmark
protocols = ['WireGuard', 'IPSec', 'OpenVPN']
single_throughput = [
    30494.86,  # WireGuard single (Mbps)
    28475.69,  # IPSec single (Mbps)
    29284.96   # OpenVPN single (Mbps)
]

bidirectional_throughput = [
    (26378.32 + 25621.63) / 2,  # WireGuard bidirectional average
    (24134.08 + 24227.18) / 2,  # IPSec bidirectional average  
    (24938.41 + 24528.88) / 2   # OpenVPN bidirectional average
]

# Konversi ke Gbps untuk skala yang lebih mudah dibaca
single_throughput_gbps = [x / 1000 for x in single_throughput]
bidirectional_throughput_gbps = [x / 1000 for x in bidirectional_throughput]

# Warna kontras untuk visualisasi
colors_single = ['#2E86AB', '#A23B72', '#F18F01']
colors_bidirectional = ['#1B998B', '#FF9B71', '#5D4E6D']

# Membuat visualisasi
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Single Direction Throughput
bars1 = ax1.bar(protocols, single_throughput_gbps, color=colors_single, alpha=0.8, edgecolor='black', linewidth=1.2)
ax1.set_title('Single Direction TCP Throughput\nby VPN Protocol', fontsize=14, fontweight='bold', pad=20)
ax1.set_ylabel('Throughput (Gbps)', fontsize=12, fontweight='bold')
ax1.set_xlabel('VPN Protocol', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Menambahkan nilai pada bar
for i, bar in enumerate(bars1):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{single_throughput[i]:.0f} Mbps',
             ha='center', va='bottom', fontweight='bold', fontsize=10)

# Plot 2: Bidirectional Throughput
bars2 = ax2.bar(protocols, bidirectional_throughput_gbps, color=colors_bidirectional, alpha=0.8, edgecolor='black', linewidth=1.2)
ax2.set_title('Bidirectional TCP Throughput\nby VPN Protocol', fontsize=14, fontweight='bold', pad=20)
ax2.set_ylabel('Average Throughput (Gbps)', fontsize=12, fontweight='bold')
ax2.set_xlabel('VPN Protocol', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Menambahkan nilai pada bar
for i, bar in enumerate(bars2):
    height = bar.get_height()
    avg_throughput = (bidirectional_throughput[i] * 2)  # Total bidirectional throughput
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{avg_throughput:.0f} Mbps\nTotal',
             ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.show()

# Perbandingan performa relatif
wireguard_single_gain = ((single_throughput[0] - single_throughput[1]) / single_throughput[1]) * 100
wireguard_bidir_gain = ((bidirectional_throughput[0] - bidirectional_throughput[1]) / bidirectional_throughput[1]) * 100

print(f"\nPerformance Analysis:")
print(f"WireGuard shows {wireguard_single_gain:.1f}% higher single-direction throughput than IPSec")
print(f"WireGuard shows {wireguard_bidir_gain:.1f}% higher bidirectional throughput than IPSec")
print(f"OpenVPN performs competitively with {single_throughput[2]/single_throughput[0]*100:.1f}% of WireGuard's single-direction throughput")