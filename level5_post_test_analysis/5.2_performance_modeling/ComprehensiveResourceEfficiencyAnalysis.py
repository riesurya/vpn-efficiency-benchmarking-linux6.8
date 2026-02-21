import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Data dari resource efficiency analysis
efficiency_data = {
    'protocol': ['wireguard', 'openvpn', 'ipsec'],
    'avg_efficiency_score': [69.85, 25.49, 41.82],
    'max_connections_80pct_cpu': [100, 25, 50],
    'cpu_usage_at_50_connections': [35.61, 97.61, 69.55]
}

# Normalisasi data untuk radar chart (0-100 scale)
def normalize_data(values):
    max_val = max(values)
    return [v/max_val*100 for v in values]

categories = ['Efficiency Score', 'Max Connections\n@80% CPU', 'CPU Usage\n@50 Connections\n(inverted)']

# Data untuk radar chart
wireguard_data = [
    efficiency_data['avg_efficiency_score'][0],  # Efficiency Score
    efficiency_data['max_connections_80pct_cpu'][0],  # Max Connections
    100 - efficiency_data['cpu_usage_at_50_connections'][0]  # Inverted CPU Usage (lower is better)
]

openvpn_data = [
    efficiency_data['avg_efficiency_score'][1],
    efficiency_data['max_connections_80pct_cpu'][1],
    100 - efficiency_data['cpu_usage_at_50_connections'][1]
]

ipsec_data = [
    efficiency_data['avg_efficiency_score'][2],
    efficiency_data['max_connections_80pct_cpu'][2],
    100 - efficiency_data['cpu_usage_at_50_connections'][2]
]

# Setup radar chart
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, polar=True)

# Hitung sudut untuk setiap kategori
angles = np.linspace(0, 2*pi, len(categories), endpoint=False).tolist()
angles += angles[:1]  # Tutup lingkaran

# Data untuk plotting (tutup lingkaran)
wg_data = wireguard_data + [wireguard_data[0]]
ov_data = openvpn_data + [openvpn_data[0]]
ip_data = ipsec_data + [ipsec_data[0]]

# Plot data
ax.plot(angles, wg_data, 'o-', linewidth=2, label='WireGuard', color='#2E86AB', markersize=8)
ax.fill(angles, wg_data, alpha=0.25, color='#2E86AB')
ax.plot(angles, ov_data, 'o-', linewidth=2, label='OpenVPN', color='#F18F01', markersize=8)
ax.fill(angles, ov_data, alpha=0.25, color='#F18F01')
ax.plot(angles, ip_data, 'o-', linewidth=2, label='IPSec', color='#A23B72', markersize=8)
ax.fill(angles, ip_data, alpha=0.25, color='#A23B72')

# Customize chart
ax.set_theta_offset(pi/2)
ax.set_theta_direction(-1)
ax.set_thetagrids(np.degrees(angles[:-1]), categories)
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(['20', '40', '60', '80', '100%'])
ax.grid(True)

plt.title('Comprehensive Resource Efficiency Analysis:\nVPN Protocols Performance Comparison', 
          fontsize=14, fontweight='bold', pad=30)
#plt.legend(bbox_to_anchor=(1.2, 1), loc='upper left')
plt.legend(bbox_to_anchor=(1, -0.1), loc='lower right')

# Add performance insights
# efficiency_text = (
#     'Key Efficiency Metrics:\n'
#     '• WireGuard: Highest efficiency (69.85/100)\n'
#     '• Supports 100 connections at 80% CPU\n'
#     '• Only 35.6% CPU usage at 50 connections\n'
#     '• IPSec: Moderate efficiency (41.82/100)\n'
#     '• OpenVPN: Lowest efficiency (25.49/100)'
# )

# plt.figtext(0.02, 0.02, efficiency_text, fontsize=10,
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))

plt.tight_layout()
plt.show()