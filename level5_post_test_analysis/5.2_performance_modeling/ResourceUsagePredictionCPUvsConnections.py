import matplotlib.pyplot as plt
import numpy as np

# Data dari resource usage predictions
resource_data = {
    'connections': [1, 10, 25, 50, 100],
    'wireguard_cpu': [14.7, 18.54, 24.94, 35.61, 56.94],
    'openvpn_cpu': [46.95, 56.25, 71.76, 97.61, 100.0],
    'ipsec_cpu': [32.02, 38.92, 50.4, 69.55, 100.0],
    'wireguard_eff': [85.3, 81.46, 75.06, 64.39, 43.06],
    'openvpn_eff': [53.05, 43.75, 28.24, 2.39, 0.0],
    'ipsec_eff': [67.98, 61.08, 49.6, 30.45, 0.0]
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: CPU Usage Prediction
ax1.plot(resource_data['connections'], resource_data['wireguard_cpu'], 
         'o-', linewidth=3, markersize=8, label='WireGuard', color='#2E86AB')
ax1.plot(resource_data['connections'], resource_data['openvpn_cpu'], 
         's-', linewidth=3, markersize=8, label='OpenVPN', color='#F18F01')
ax1.plot(resource_data['connections'], resource_data['ipsec_cpu'], 
         '^-', linewidth=3, markersize=8, label='IPSec', color='#A23B72')

ax1.set_xlabel('Number of Connections', fontweight='bold', fontsize=12)
ax1.set_ylabel('Predicted CPU Usage (%)', fontweight='bold', fontsize=12)
ax1.set_title('A. CPU Usage Prediction vs Connection Load', 
              fontweight='bold', fontsize=13, pad=15)
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 105)

# Add critical points
ax1.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='80% CPU Threshold')
ax1.text(60, 82, 'CPU Saturation\nThreshold', color='red', fontweight='bold', fontsize=9)

# Plot 2: Efficiency Score
ax2.plot(resource_data['connections'], resource_data['wireguard_eff'], 
         'o-', linewidth=3, markersize=8, label='WireGuard', color='#2E86AB')
ax2.plot(resource_data['connections'], resource_data['openvpn_eff'], 
         's-', linewidth=3, markersize=8, label='OpenVPN', color='#F18F01')
ax2.plot(resource_data['connections'], resource_data['ipsec_eff'], 
         '^-', linewidth=3, markersize=8, label='IPSec', color='#A23B72')

ax2.set_xlabel('Number of Connections', fontweight='bold', fontsize=12)
ax2.set_ylabel('Efficiency Score', fontweight='bold', fontsize=12)
ax2.set_title('B. Efficiency Score Degradation', 
              fontweight='bold', fontsize=13, pad=15)
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 100)

# Add saturation points
wg_saturation = 100  # WireGuard reaches 80% CPU at 100 connections
ov_saturation = 25   # OpenVPN reaches 80% CPU at ~25 connections
ip_saturation = 50   # IPSec reaches 80% CPU at ~50 connections

ax2.axvline(x=wg_saturation, color='#2E86AB', linestyle=':', alpha=0.7)
ax2.axvline(x=ov_saturation, color='#F18F01', linestyle=':', alpha=0.7)
ax2.axvline(x=ip_saturation, color='#A23B72', linestyle=':', alpha=0.7)

plt.suptitle('Resource Usage Modeling and Efficiency Analysis', 
             fontweight='bold', fontsize=16, y=0.98)

# Add comprehensive analysis
analysis_text = (
    'Scalability Limits (@80% CPU):\n'
    f'• WireGuard: {wg_saturation} connections\n'
    f'• IPSec: {ip_saturation} connections\n'
    f'• OpenVPN: {ov_saturation} connections\n\n'
    'WireGuard shows 4x better scalability\nthan OpenVPN at CPU saturation'
)

# plt.figtext(0.02, 0.02, analysis_text, fontsize=10,
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))

plt.tight_layout()
plt.show()