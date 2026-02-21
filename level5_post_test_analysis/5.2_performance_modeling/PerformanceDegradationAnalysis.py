import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data dari performance degradation model
degradation_data = {
    'wireguard_conn': [1, 5, 10, 20, 50],
    'wireguard_throughput': [858.07, 834.36, 823.45, 805.05, 747.77],
    'openvpn_conn': [1, 5, 10, 20, 50],
    'openvpn_throughput': [331.74, 301.26, 292.41, 241.03, 124.05],
    'ipsec_conn': [1, 5, 10, 20, 50],
    'ipsec_throughput': [485.43, 460.97, 463.17, 421.85, 316.47]
}

plt.figure(figsize=(12, 8))

# Plot throughput degradation
plt.plot(degradation_data['wireguard_conn'], degradation_data['wireguard_throughput'], 
         'o-', linewidth=3, markersize=8, label='WireGuard', color='#2E86AB')
plt.plot(degradation_data['openvpn_conn'], degradation_data['openvpn_throughput'], 
         's-', linewidth=3, markersize=8, label='OpenVPN', color='#F18F01')
plt.plot(degradation_data['ipsec_conn'], degradation_data['ipsec_throughput'], 
         '^-', linewidth=3, markersize=8, label='IPSec', color='#A23B72')

plt.xlabel('Number of Concurrent Connections', fontweight='bold', fontsize=12)
plt.ylabel('Throughput (Mbps)', fontweight='bold', fontsize=12)
plt.title('Performance Degradation Analysis:\nThroughput vs Concurrent Connections', 
          fontweight='bold', fontsize=14, pad=20)
plt.legend()
plt.grid(True, alpha=0.3)

# Add degradation percentages
degradation_rates = {
    'WireGuard': 12.85,
    'OpenVPN': 62.60,
    'IPSec': 34.81
}

for i, (protocol, rate) in enumerate(degradation_rates.items()):
    y_pos = [858, 331, 485][i]  # Starting throughput
    plt.text(25, y_pos - 100 + i*50, f'{protocol}: {rate}% degradation', 
             fontweight='bold', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

# Add regression lines from coefficients
x_pred = np.array([1, 10, 25, 50, 100])
wg_pred = -2.0868 * x_pred + 849.64
ov_pred = -4.1447 * x_pred + 329.39
ip_pred = -3.4014 * x_pred + 488.08

plt.plot(x_pred, wg_pred, '--', color='#2E86AB', alpha=0.6, label='WireGuard Trend')
plt.plot(x_pred, ov_pred, '--', color='#F18F01', alpha=0.6, label='OpenVPN Trend')
plt.plot(x_pred, ip_pred, '--', color='#A23B72', alpha=0.6, label='IPSec Trend')

plt.xlim(0, 55)
plt.ylim(0, 900)

# Add insights
# plt.figtext(0.02, 0.02,
#            'Key Insights:\n'
#            '• WireGuard shows minimal degradation (12.9%)\n'
#            '• OpenVPN suffers severe degradation (62.6%)\n'
#            '• IPSec shows moderate degradation (34.8%)\n'
#            '• Dashed lines show linear regression trends',
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7),
#            fontsize=9)

plt.tight_layout()
plt.show()