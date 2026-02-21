import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter

# Data dari file teks
wireguard_times = [101.769673, 97.080781, 94.330205, 115.736051, 88.388870]
openvpn_times = [101.482615, 88.514605, 101.489379, 97.969644, 112.085111]
ipsec_times = [117.237931, 107.936890, 97.101780, 98.859669, 90.560141]

# Konversi ke milliseconds
wireguard_ms = [t * 1000 for t in wireguard_times]
openvpn_ms = [t * 1000 for t in openvpn_times]
ipsec_ms = [t * 1000 for t in ipsec_times]

# Hitung statistik
def calculate_stats(times):
    return {
        'mean': np.mean(times),
        'std': np.std(times),
        'min': np.min(times),
        'max': np.max(times)
    }

wireguard_stats = calculate_stats(wireguard_ms)
openvpn_stats = calculate_stats(openvpn_ms)
ipsec_stats = calculate_stats(ipsec_ms)

# Create figure dengan 2 subplot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# ===== PLOT 1: Bar chart dengan error bars =====
protocols = ['WireGuard', 'OpenVPN', 'IPSec']
means = [wireguard_stats['mean'], openvpn_stats['mean'], ipsec_stats['mean']]
stds = [wireguard_stats['std'], openvpn_stats['std'], ipsec_stats['std']]

bars = ax1.bar(protocols, means, yerr=stds, capsize=8, 
               color=['#2E8B57', '#4682B4', '#B22222'], alpha=0.7,
               edgecolor='black', linewidth=0.5)

ax1.set_ylabel('Connection Time (ms)', fontsize=12, fontweight='bold')
ax1.set_title('Average Connection Establishment Time\nwith Standard Deviation', 
              fontsize=14, fontweight='bold', pad=20)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Tambahkan nilai di atas bars
for i, (bar, mean, std) in enumerate(zip(bars, means, stds)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + std + 2,
             f'{mean:.1f}±{std:.1f}ms', ha='center', va='bottom', fontweight='bold')

ax1.set_ylim(0, max(means) + max(stds) + 15)

# ===== PLOT 2: Time series per attempt =====
attempts = np.arange(1, 6)

ax2.plot(attempts, wireguard_ms, 'o-', linewidth=2, markersize=8, 
         label='WireGuard', color='#2E8B57', markerfacecolor='white', markeredgewidth=2)
ax2.plot(attempts, openvpn_ms, 's-', linewidth=2, markersize=8, 
         label='OpenVPN', color='#4682B4', markerfacecolor='white', markeredgewidth=2)
ax2.plot(attempts, ipsec_ms, '^-', linewidth=2, markersize=8, 
         label='IPSec', color='#B22222', markerfacecolor='white', markeredgewidth=2)

ax2.set_xlabel('Connection Attempt', fontsize=12, fontweight='bold')
ax2.set_ylabel('Connection Time (ms)', fontsize=12, fontweight='bold')
ax2.set_title('Connection Time per Attempt', fontsize=14, fontweight='bold', pad=20)
ax2.set_xticks(attempts)
ax2.legend(fontsize=11, framealpha=0.9)
ax2.grid(True, alpha=0.3, linestyle='--')

# Tambahkan horizontal lines untuk rata-rata
ax2.axhline(y=wireguard_stats['mean'], color='#2E8B57', linestyle='--', alpha=0.7)
ax2.axhline(y=openvpn_stats['mean'], color='#4682B4', linestyle='--', alpha=0.7)
ax2.axhline(y=ipsec_stats['mean'], color='#B22222', linestyle='--', alpha=0.7)

# Format y-axis
ax2.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

plt.tight_layout()
plt.show()

# ===== TABEL STATISTIK DETAIL =====
print("=" * 65)
print("DETAILED CONNECTION ESTABLISHMENT TIME ANALYSIS")
print("=" * 65)

stats_data = {
    'Protocol': ['WireGuard', 'OpenVPN', 'IPSec'],
    'Mean (ms)': [f"{wireguard_stats['mean']:.2f}", f"{openvpn_stats['mean']:.2f}", f"{ipsec_stats['mean']:.2f}"],
    'Std Dev (ms)': [f"{wireguard_stats['std']:.2f}", f"{openvpn_stats['std']:.2f}", f"{ipsec_stats['std']:.2f}"],
    'Min (ms)': [f"{wireguard_stats['min']:.2f}", f"{openvpn_stats['min']:.2f}", f"{ipsec_stats['min']:.2f}"],
    'Max (ms)': [f"{wireguard_stats['max']:.2f}", f"{openvpn_stats['max']:.2f}", f"{ipsec_stats['max']:.2f}"],
    'Range (ms)': [f"{wireguard_stats['max']-wireguard_stats['min']:.2f}", 
                   f"{openvpn_stats['max']-openvpn_stats['min']:.2f}", 
                   f"{ipsec_stats['max']-ipsec_stats['min']:.2f}"]
}

df = pd.DataFrame(stats_data)
print(df.to_string(index=False))

print("\n" + "=" * 65)
print("PERFORMANCE RANKING:")
print("=" * 65)

# Ranking berdasarkan mean time
ranking = sorted(zip(['WireGuard', 'OpenVPN', 'IPSec'], 
                    [wireguard_stats['mean'], openvpn_stats['mean'], ipsec_stats['mean']]),
                key=lambda x: x[1])

for i, (protocol, time) in enumerate(ranking, 1):
    print(f"{i}. {protocol}: {time:.2f} ms")

print("\n" + "=" * 65)
print("KEY INSIGHTS:")
print("=" * 65)
print("✓ WireGuard: Fastest average connection time")
print("✓ OpenVPN: Most consistent (lowest standard deviation)") 
print("✓ IPSec: Slowest but still competitive performance")
print("✓ All protocols: Sub-120ms performance suitable for real-time applications")