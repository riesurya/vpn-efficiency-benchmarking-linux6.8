import matplotlib.pyplot as plt
import numpy as np

# Data preparation
metrics = ['Average Efficiency\nScore', 'Max Connections\nat 80% CPU', 'CPU Usage at\n50 Connections']
wireguard = [69.85, 100, 35.61]
openvpn = [25.49, 25, 97.61]
ipsec = [41.82, 50, 69.55]

x = np.arange(len(metrics))
width = 0.25

fig, ax = plt.subplots(figsize=(12, 8))

# Create bars
bars1 = ax.bar(x - width, wireguard, width, label='WireGuard', 
               color='#2E86AB', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x, openvpn, width, label='OpenVPN', 
               color='#F18F01', alpha=0.8, edgecolor='black')
bars3 = ax.bar(x + width, ipsec, width, label='IPSec', 
               color='#A23B72', alpha=0.8, edgecolor='black')

# Customize plot
ax.set_xlabel('Efficiency Metrics', fontweight='bold', fontsize=12)
ax.set_ylabel('Performance Score / Percentage', fontweight='bold', fontsize=12)
ax.set_title('Quantitative Resource Efficiency Comparison:\nVPN Protocols Scalability Analysis', 
             fontweight='bold', fontsize=14, pad=20)
ax.set_xticks(x)
ax.set_xticklabels(metrics)
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# Add value labels dengan format berbeda untuk setiap metrik
for i, (wg, ov, ip) in enumerate(zip(wireguard, openvpn, ipsec)):
    # Efficiency Score
    if i == 0:
        ax.text(i - width, wg + 2, f'{wg:.1f}', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
        ax.text(i, ov + 2, f'{ov:.1f}', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
        ax.text(i + width, ip + 2, f'{ip:.1f}', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
    # Max Connections
    elif i == 1:
        ax.text(i - width, wg + 2, f'{wg:.0f}', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
        ax.text(i, ov + 2, f'{ov:.0f}', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
        ax.text(i + width, ip + 2, f'{ip:.0f}', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
    # CPU Usage (lower is better)
    else:
        ax.text(i - width, wg + 2, f'{wg:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=9, color='green')
        ax.text(i, ov + 2, f'{ov:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=9, color='red')
        ax.text(i + width, ip + 2, f'{ip:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=9, color='orange')

# Add performance ratio analysis
wg_advantage = wireguard[1] / openvpn[1]  # Max connections ratio
cpu_efficiency = openvpn[2] / wireguard[2]  # CPU usage ratio

analysis_text = (
    'Scalability Advantages:\n'
    f'• WireGuard handles {wg_advantage:.0f}x more connections than OpenVPN\n'
    f'• WireGuard uses {cpu_efficiency:.1f}x less CPU at 50 connections\n'
    f'• IPSec shows {ipsec[0]/openvpn[0]:.1f}x better efficiency than OpenVPN'
)

# plt.figtext(0.02, 0.02, analysis_text, fontsize=10,
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))

plt.tight_layout()
plt.show()