import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Create DataFrame from analysis dataset
data = pd.read_csv('analysis_dataset.csv')  # Using the provided dataset

plt.figure(figsize=(12, 8))

# Create box plot with swarm plot overlay
box_plot = sns.boxplot(data=data, x='protocol', y='throughput_mbps', 
                       palette=['#2E86AB', '#F18F01', '#A23B72'],
                       order=['wireguard', 'openvpn', 'ipsec'])

# Add swarm plot for individual data points
swarm_plot = sns.swarmplot(data=data, x='protocol', y='throughput_mbps',
                          color='black', alpha=0.5, size=3,
                          order=['wireguard', 'openvpn', 'ipsec'])

plt.xlabel('VPN Protocol', fontweight='bold', fontsize=12)
plt.ylabel('Throughput (Mbps)', fontweight='bold', fontsize=12)
plt.title('Distribution Analysis: Throughput Performance Across VPN Protocols\n', 
          fontweight='bold', fontsize=14, pad=20)

# Add descriptive statistics from the provided data
desc_stats = {
    'wireguard': {'mean': 842.79, 'std': 41.94, 'median': 841.25},
    'openvpn': {'mean': 316.82, 'std': 27.56, 'median': 318.94},
    'ipsec': {'mean': 477.16, 'std': 36.65, 'median': 482.25}
}

# Add statistics annotations
y_positions = [900, 400, 580]
for i, protocol in enumerate(['wireguard', 'openvpn', 'ipsec']):
    stats = desc_stats[protocol]
    plt.text(i, y_positions[i],
             f'Mean: {stats["mean"]:.1f}\nStd: {stats["std"]:.1f}\nMedian: {stats["median"]:.1f}',
             ha='center', va='center', fontweight='bold', fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

# Add distribution insights
# plt.figtext(0.02, 0.02,
#            'Distribution Characteristics:\n'
#            '• WireGuard: High throughput with moderate variability\n'
#            '• OpenVPN: Consistent but lower performance\n'
#            '• IPSec: Moderate performance with some outliers',
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7),
#            fontsize=9)

plt.show()