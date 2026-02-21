import matplotlib.pyplot as plt
import numpy as np

# Data Throughput Stability
stability_data = {
    'WireGuard': {
        'time': [1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.00],
        'throughput': [29.87, 28.20, 29.65, 27.76, 27.78, 27.83, 29.43, 29.40, 29.92, 30.38],
        'color': '#2E86AB',
        'avg': 29.02,
        'std': 0.96
    },
    'OpenVPN': {
        'time': [1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.00],
        'throughput': [30.58, 30.46, 29.78, 27.94, 29.15, 28.63, 26.77, 25.18, 24.89, 27.15],
        'color': '#F18F01', 
        'avg': 28.13,
        'std': 2.01
    },
    'IPsec': {
        'time': [1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.00],
        'throughput': [28.48, 28.77, 28.99, 27.94, 28.39, 23.03, 28.20, 28.01, 26.17, 28.56],
        'color': '#A23B72',
        'avg': 27.65,
        'std': 1.73
    }
}

# Setup plot
plt.figure(figsize=(12, 6))

# Plot throughput lines with markers
for vpn, data in stability_data.items():
    plt.plot(data['time'], data['throughput'], marker='o', linewidth=2.5, 
             markersize=6, label=f'{vpn} (Avg: {data["avg"]:.1f} Gbps)', 
             color=data['color'], alpha=0.8)
    
    # Add average line
    plt.axhline(y=data['avg'], color=data['color'], linestyle='--', alpha=0.4, linewidth=1)

# Customize plot
plt.xlabel('Time (Seconds)', fontweight='bold', fontsize=12)
plt.ylabel('Throughput (Gbps)', fontweight='bold', fontsize=12)
plt.title('Throughput Stability Analysis: Unidirectional Single Stream Performance Over Time', 
          fontweight='bold', fontsize=14, pad=20)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.xticks(range(1, 11))

# Set y-axis limits for better visualization
plt.ylim(20, 32)

# Add stability analysis
stability_text = (
    'Stability Analysis (Standard Deviation):\n'
    f'• WireGuard: {stability_data["WireGuard"]["std"]:.2f} Gbps (Most Stable)\n'
    f'• IPSec: {stability_data["IPsec"]["std"]:.2f} Gbps\n'
    f'• OpenVPN: {stability_data["OpenVPN"]["std"]:.2f} Gbps (Least Stable)\n\n'
    'Key Observations:\n'
    '• WireGuard maintains consistent performance\n'
    '• IPSec shows significant dip at 6 seconds\n'
    '• OpenVPN exhibits gradual performance decline'
)

plt.text(0.02, 0.02, stability_text, transform=plt.gca().transAxes, fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7),
         verticalalignment='bottom')

plt.tight_layout()
plt.show()

# Print detailed stability metrics
print("THROUGHPUT STABILITY METRICS")
print("="*50)
print(f"{'Protocol':<12} {'Average':<10} {'Std Dev':<10} {'Min':<8} {'Max':<8} {'Range':<8}")
print("-"*50)
for vpn, data in stability_data.items():
    min_throughput = min(data['throughput'])
    max_throughput = max(data['throughput'])
    range_throughput = max_throughput - min_throughput
    print(f"{vpn:<12} {data['avg']:<10.2f} {data['std']:<10.2f} {min_throughput:<8.2f} {max_throughput:<8.2f} {range_throughput:<8.2f}")