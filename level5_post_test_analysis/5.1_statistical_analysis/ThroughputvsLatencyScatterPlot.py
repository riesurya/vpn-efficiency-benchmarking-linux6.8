import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Using the analysis dataset
data = pd.read_csv('analysis_dataset.csv')

plt.figure(figsize=(12, 8))

colors = {'wireguard': '#2E86AB', 'openvpn': '#F18F01', 'ipsec': '#A23B72'}
markers = {'wireguard': 'o', 'openvpn': 's', 'ipsec': '^'}

# Create scatter plot
for protocol in data['protocol'].unique():
    subset = data[data['protocol'] == protocol]
    plt.scatter(subset['throughput_mbps'], subset['latency_ms'],
               c=colors[protocol], marker=markers[protocol], 
               s=60, alpha=0.7, label=protocol.capitalize(),
               edgecolors='black', linewidth=0.5)

plt.xlabel('Throughput (Mbps)', fontweight='bold', fontsize=12)
plt.ylabel('Latency (ms)', fontweight='bold', fontsize=12)
plt.title('Throughput vs Latency: Performance Trade-off Analysis\n', 
          fontweight='bold', fontsize=14, pad=20)
plt.legend()

# Add correlation line and annotation
correlation = -0.8648  # From correlation matrix
plt.text(0.05, 0.95, f'Correlation: r = {correlation:.3f}', 
         transform=plt.gca().transAxes, fontsize=12, fontweight='bold',
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

# Add performance zones
plt.axvspan(800, 950, alpha=0.1, color='green', label='High Performance')
plt.axvspan(400, 800, alpha=0.1, color='yellow', label='Medium Performance')
plt.axvspan(200, 400, alpha=0.1, color='red', label='Low Performance')

plt.grid(True, alpha=0.3)
plt.xlim(200, 950)
plt.ylim(5, 35)

# Add performance insights
# plt.figtext(0.02, 0.02,
#            'Performance Trade-offs:\n'
#            '• WireGuard: High throughput, low latency (optimal)\n'
#            '• IPSec: Moderate throughput, variable latency\n'
#            '• OpenVPN: Lower throughput, higher latency',
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7),
#            fontsize=9)

plt.tight_layout()
plt.show()