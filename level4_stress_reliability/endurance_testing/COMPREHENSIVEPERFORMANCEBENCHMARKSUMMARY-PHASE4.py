import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data dari CSV
data = {
    'protocol': ['wireguard', 'openvpn', 'ipsec'],
    'load_test_avg_mbps': [20000, 300, 500],
    'load_success_rate': ['3/3', '2/3', '2/3'],
    'endurance_avg_mbps': [20000, 300, 500],
    'endurance_success_rate': ['3/3', '2/3', '2/3'],
    'performance_class': ['exceptional', 'standard', 'good']
}

df = pd.DataFrame(data)

# Konversi success rate ke numeric
df['load_success_rate_numeric'] = df['load_success_rate'].apply(lambda x: int(x.split('/')[0]) / int(x.split('/')[1]))
df['endurance_success_rate_numeric'] = df['endurance_success_rate'].apply(lambda x: int(x.split('/')[0]) / int(x.split('/')[1]))

# Warna untuk protokol
colors = ['#2E8B57', '#4682B4', '#B22222']
protocol_names = ['WireGuard', 'OpenVPN', 'IPSec']

# Create figure dengan 2 subplot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# ===== PLOT 1: Performance Comparison - Throughput =====
x_pos = np.arange(len(protocol_names))
width = 0.35

# Throughput bars
bars1 = ax1.bar(x_pos - width/2, df['load_test_avg_mbps'], width, 
                label='Load Test', color=colors, alpha=0.8, edgecolor='black')
bars2 = ax1.bar(x_pos + width/2, df['endurance_avg_mbps'], width, 
                label='Endurance Test', color=colors, alpha=0.6, edgecolor='black')

ax1.set_ylabel('Throughput (Mbps)', fontsize=12, fontweight='bold')
ax1.set_title('Performance Comparison: Load Test vs Endurance Test', 
              fontsize=14, fontweight='bold', pad=20)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(protocol_names)
ax1.legend(fontsize=11)
ax1.grid(axis='y', alpha=0.3)

# Tambahkan nilai di atas bars dengan format yang sesuai
for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    height1 = bar1.get_height()
    height2 = bar2.get_height()
    
    # Format nilai WireGuard secara khusus karena sangat besar
    if i == 0:  # WireGuard
        ax1.text(bar1.get_x() + bar1.get_width()/2., height1 + 500, 
                '20 Gbps', ha='center', va='bottom', fontweight='bold', fontsize=10)
        ax1.text(bar2.get_x() + bar2.get_width()/2., height2 + 500, 
                '20 Gbps', ha='center', va='bottom', fontweight='bold', fontsize=10)
    else:
        ax1.text(bar1.get_x() + bar1.get_width()/2., height1 + 20, 
                f'{height1} Mbps', ha='center', va='bottom', fontweight='bold')
        ax1.text(bar2.get_x() + bar2.get_width()/2., height2 + 20, 
                f'{height2} Mbps', ha='center', va='bottom', fontweight='bold')

# Set skala logaritmik karena perbedaan sangat besar
ax1.set_yscale('log')
ax1.set_ylim(100, 50000)

# ===== PLOT 2: Success Rate & Performance Class =====
# Success rate bars
x_pos_success = np.arange(len(protocol_names))
bars_success_load = ax2.bar(x_pos_success - width/2, df['load_success_rate_numeric']*100, width,
                           label='Load Test Success Rate', color=colors, alpha=0.8, edgecolor='black')
bars_success_endurance = ax2.bar(x_pos_success + width/2, df['endurance_success_rate_numeric']*100, width,
                                label='Endurance Test Success Rate', color=colors, alpha=0.6, edgecolor='black')

ax2.set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title('Reliability Analysis: Success Rates & Performance Classification', 
              fontsize=14, fontweight='bold', pad=20)
ax2.set_xticks(x_pos_success)
ax2.set_xticklabels(protocol_names)
ax2.set_ylim(0, 120)
ax2.legend(fontsize=11)
ax2.grid(axis='y', alpha=0.3)

# Tambahkan nilai success rate dan performance class
for i, (bar_load, bar_endurance, perf_class) in enumerate(zip(bars_success_load, bars_success_endurance, df['performance_class'])):
    # Success rate values
    ax2.text(bar_load.get_x() + bar_load.get_width()/2., bar_load.get_height() + 2, 
            f"{df['load_success_rate'].iloc[i]}", ha='center', va='bottom', fontweight='bold')
    ax2.text(bar_endurance.get_x() + bar_endurance.get_width()/2., bar_endurance.get_height() + 2, 
            f"{df['endurance_success_rate'].iloc[i]}", ha='center', va='bottom', fontweight='bold')
    
    # Performance class annotation
    ax2.text(bar_load.get_x() + bar_load.get_width(), -15, 
            f"Class: {perf_class.title()}", ha='center', va='top', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[i], alpha=0.3))

plt.tight_layout()
plt.show()

# ===== TABEL PERFORMANCE SUMMARY =====
print("=" * 80)
print("COMPREHENSIVE PERFORMANCE BENCHMARK SUMMARY - PHASE 4")
print("=" * 80)

summary_data = {
    'Protocol': ['WireGuard', 'OpenVPN', 'IPSec'],
    'Load Test (Mbps)': ['20,000', '300', '500'],
    'Load Success Rate': ['3/3 (100%)', '2/3 (67%)', '2/3 (67%)'],
    'Endurance Test (Mbps)': ['20,000', '300', '500'],
    'Endurance Success Rate': ['3/3 (100%)', '2/3 (67%)', '2/3 (67%)'],
    'Performance Class': ['Exceptional', 'Standard', 'Good'],
    'Performance Ratio (vs OpenVPN)': ['66.7x', '1x', '1.7x']
}

summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))

print("\n" + "=" * 80)
print("KEY PERFORMANCE INSIGHTS:")
print("=" * 80)
print("🚀 WIREGUARD DOMINANCE:")
print("   • 20 Gbps throughput - 66.7x faster than OpenVPN")
print("   • 100% success rate in both load and endurance tests")
print("   • Exceptional performance class with no degradation")

print("\n⚖️ IPSEC ADVANTAGE:")
print("   • 1.7x faster than OpenVPN (500 vs 300 Mbps)")
print("   • Same reliability profile as OpenVPN (67% success rate)")
print("   • Good performance class suitable for enterprise use")

print("\n🛡️ OPENVPN POSITIONING:")
print("   • Baseline performance (300 Mbps)")
print("   • Reliability concerns (67% success rate)")
print("   • Standard performance class - suitable for compatibility-focused deployments")

print("\n" + "=" * 80)
print("STRATEGIC RECOMMENDATIONS:")
print("=" + 80)
print("✅ WireGuard: Mission-critical, high-performance applications")
print("✅ IPSec: Enterprise environments requiring balanced performance & security")  
print("✅ OpenVPN: Legacy compatibility and cross-platform deployments")