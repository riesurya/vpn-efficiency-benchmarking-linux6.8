import matplotlib.pyplot as plt
import numpy as np

# Data Average Throughput
throughput_data = {
    'WireGuard': {
        'Unidirectional': 30.49,
        'Bidirectional_Send': 26.38,
        'Bidirectional_Receive': 25.61,
        'Bidirectional_Avg': (26.38 + 25.61) / 2
    },
    'IPsec': {
        'Unidirectional': 28.48,
        'Bidirectional_Send': 24.13,
        'Bidirectional_Receive': 24.23,
        'Bidirectional_Avg': (24.13 + 24.23) / 2
    },
    'OpenVPN': {
        'Unidirectional': 29.28,
        'Bidirectional_Send': 24.94,
        'Bidirectional_Receive': 24.52,
        'Bidirectional_Avg': (24.94 + 24.52) / 2
    }
}

# Setup plot
plt.figure(figsize=(12, 6))
vpn_types = list(throughput_data.keys())
x = np.arange(len(vpn_types))
width = 0.25

# Colors
colors = {
    'Unidirectional': '#2E86AB',
    'Bidirectional_Send': '#A23B72', 
    'Bidirectional_Receive': '#F18F01'
}

# Create bars
uni_throughput = [throughput_data[vpn]['Unidirectional'] for vpn in vpn_types]
bi_send = [throughput_data[vpn]['Bidirectional_Send'] for vpn in vpn_types]
bi_receive = [throughput_data[vpn]['Bidirectional_Receive'] for vpn in vpn_types]

bars1 = plt.bar(x - width, uni_throughput, width, label='Unidirectional',
                color=colors['Unidirectional'], alpha=0.8, edgecolor='black', linewidth=1.2)
bars2 = plt.bar(x, bi_send, width, label='Bidirectional (Send)',
                color=colors['Bidirectional_Send'], alpha=0.8, edgecolor='black', linewidth=1.2)
bars3 = plt.bar(x + width, bi_receive, width, label='Bidirectional (Receive)',
                color=colors['Bidirectional_Receive'], alpha=0.8, edgecolor='black', linewidth=1.2)

# Customize plot
plt.xlabel('VPN Protocol', fontweight='bold', fontsize=12)
plt.ylabel('Throughput (Gbps)', fontweight='bold', fontsize=12)
plt.title('Average Throughput Performance: WireGuard vs IPSec vs OpenVPN\nby Traffic Direction', 
          fontweight='bold', fontsize=14, pad=20)
plt.xticks(x, vpn_types)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3, axis='y')

# Add value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                 f'{height:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

# Calculate and display performance differences
wireguard_gain = ((throughput_data['WireGuard']['Unidirectional'] - throughput_data['IPsec']['Unidirectional']) / throughput_data['IPsec']['Unidirectional']) * 100

# plt.text(0.02, 0.98, f'Key Insights:\n• WireGuard leads by +{wireguard_gain:.1f}% over IPSec\n• Bidirectional throughput ~18% lower than unidirectional\n• All protocols show symmetric send/receive performance', 
#          transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
#          bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))

plt.tight_layout()
plt.show()