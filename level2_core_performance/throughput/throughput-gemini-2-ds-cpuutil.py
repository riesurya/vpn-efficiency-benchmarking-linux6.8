import matplotlib.pyplot as plt
import numpy as np

# Data CPU Utilization
cpu_data = {
    'WireGuard': {'Unidirectional': 100.27, 'Bidirectional': 152.99},
    'IPsec': {'Unidirectional': 100.22, 'Bidirectional': 152.80},
    'OpenVPN': {'Unidirectional': 100.12, 'Bidirectional': 153.52}
}

# Setup plot
plt.figure(figsize=(10, 6))
vpn_types = list(cpu_data.keys())
x = np.arange(len(vpn_types))
width = 0.35

# Colors
colors = {'Unidirectional': '#1B998B', 'Bidirectional': '#FF6B6B'}

# Create bars
uni_cpu = [cpu_data[vpn]['Unidirectional'] for vpn in vpn_types]
bi_cpu = [cpu_data[vpn]['Bidirectional'] for vpn in vpn_types]

bars1 = plt.bar(x - width/2, uni_cpu, width, label='Unidirectional', 
                color=colors['Unidirectional'], alpha=0.8, edgecolor='black', linewidth=1.2)
bars2 = plt.bar(x + width/2, bi_cpu, width, label='Bidirectional', 
                color=colors['Bidirectional'], alpha=0.8, edgecolor='black', linewidth=1.2)

# Customize plot
plt.xlabel('VPN Protocol', fontweight='bold', fontsize=12)
plt.ylabel('CPU Utilization (%)', fontweight='bold', fontsize=12)
plt.title('CPU Utilization Comparison: WireGuard vs IPSec vs OpenVPN\nby Test Configuration', 
          fontweight='bold', fontsize=14, pad=20)
plt.xticks(x, vpn_types)
plt.legend()
plt.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar in bars1 + bars2:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)

# Add performance insights
# plt.text(0.02, 0.98, 'Key Insights:\n• Bidirectional traffic increases CPU usage by ~53%\n• All protocols show similar CPU patterns\n• WireGuard has slightly better efficiency', 
#          transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
#          bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))

plt.tight_layout()
plt.show()