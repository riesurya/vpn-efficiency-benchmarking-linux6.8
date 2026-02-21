import matplotlib.pyplot as plt
import numpy as np

# Data dari performance degradation model
latency_data = {
    'connections': [1, 5, 10, 20, 50],
    'wireguard_latency': [11.13, 12.40, 13.42, 14.39, 16.14],
    'openvpn_latency': [25.95, 28.32, 35.82, 42.97, 72.85],
    'ipsec_latency': [18.07, 19.58, 23.68, 27.95, 43.68]
}

# Data dari degradation rates
latency_increase = {
    'WireGuard': 44.99,
    'OpenVPN': 180.73,
    'IPSec': 141.75
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Latency vs Connections
ax1.plot(latency_data['connections'], latency_data['wireguard_latency'], 
         'o-', linewidth=3, markersize=8, label='WireGuard', color='#2E86AB')
ax1.plot(latency_data['connections'], latency_data['openvpn_latency'], 
         's-', linewidth=3, markersize=8, label='OpenVPN', color='#F18F01')
ax1.plot(latency_data['connections'], latency_data['ipsec_latency'], 
         '^-', linewidth=3, markersize=8, label='IPSec', color='#A23B72')

ax1.set_xlabel('Number of Connections', fontweight='bold', fontsize=12)
ax1.set_ylabel('Latency (ms)', fontweight='bold', fontsize=12)
ax1.set_title('A. Latency Increase vs Connection Load', 
              fontweight='bold', fontsize=13, pad=15)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Add latency thresholds
ax1.axhline(y=50, color='red', linestyle='--', alpha=0.7, label='50ms Threshold')
ax1.text(30, 52, 'Real-time\nApplication Limit', color='red', fontweight='bold', fontsize=8)

# Plot 2: Latency Increase Percentage
protocols = list(latency_increase.keys())
increase_rates = list(latency_increase.values())
colors = ['#2E86AB', '#F18F01', '#A23B72']

bars = ax2.bar(protocols, increase_rates, color=colors, alpha=0.8, edgecolor='black')
ax2.set_xlabel('VPN Protocol', fontweight='bold', fontsize=12)
ax2.set_ylabel('Latency Increase (%)', fontweight='bold', fontsize=12)
ax2.set_title('B. Latency Degradation (1 to 50 Connections)', 
              fontweight='bold', fontsize=13, pad=15)
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, rate in zip(bars, increase_rates):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'+{rate:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.suptitle('Latency Performance Analysis Under Increasing Load', 
             fontweight='bold', fontsize=16, y=0.98)

# Add latency analysis
latency_analysis = (
    'Latency Stability Ranking:\n'
    '1. WireGuard: +45% increase (16.1ms at 50 conn)\n'
    '2. IPSec: +142% increase (43.7ms at 50 conn)\n'
    '3. OpenVPN: +181% increase (72.9ms at 50 conn)\n\n'
    'WireGuard maintains sub-20ms latency\nacross all connection loads'
)

# plt.figtext(0.02, 0.02, latency_analysis, fontsize=9,
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))

plt.tight_layout()
plt.show()