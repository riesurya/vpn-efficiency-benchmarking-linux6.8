import matplotlib.pyplot as plt
import numpy as np

# Confidence intervals data
ci_data = {
    'protocol': ['wireguard', 'openvpn', 'ipsec'],
    'mean_throughput': [842.79, 316.82, 477.16],
    'ci_lower': [827.78, 306.96, 464.05],
    'ci_upper': [857.80, 326.68, 490.28],
    'std_error': [7.66, 5.03, 6.69]
}

plt.figure(figsize=(10, 6))

colors = ['#2E86AB', '#F18F01', '#A23B72']
x_pos = np.arange(len(ci_data['protocol']))

# Plot means
bars = plt.bar(x_pos, ci_data['mean_throughput'], 
               color=colors, alpha=0.7, edgecolor='black', linewidth=1.2)

# Add error bars for confidence intervals
for i, (mean, lower, upper) in enumerate(zip(ci_data['mean_throughput'], 
                                            ci_data['ci_lower'], 
                                            ci_data['ci_upper'])):
    plt.errorbar(x_pos[i], mean, yerr=[[mean - lower], [upper - mean]], 
                 fmt='none', color='black', capsize=8, capthick=2, linewidth=2)

plt.xlabel('VPN Protocol', fontweight='bold', fontsize=12)
plt.ylabel('Throughput (Mbps)', fontweight='bold', fontsize=12)
plt.title('Mean Throughput with 95% Confidence Intervals\n', 
          fontweight='bold', fontsize=14, pad=20)
plt.xticks(x_pos, ci_data['protocol'])

# Add value labels
for i, (bar, mean, se) in enumerate(zip(bars, ci_data['mean_throughput'], ci_data['std_error'])):
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 20,
             f'{mean:.1f} ± {se:.1f}', ha='center', va='bottom', 
             fontweight='bold', fontsize=10)

plt.grid(axis='y', alpha=0.3)
plt.ylim(0, 950)

# Add interpretation
# plt.figtext(0.02, 0.02,
#            'Confidence Interval Interpretation:\n'
#            '• WireGuard: 827.8 - 857.8 Mbps (95% CI)\n'
#            '• OpenVPN: 307.0 - 326.7 Mbps (95% CI)\n'
#            '• IPSec: 464.1 - 490.3 Mbps (95% CI)',
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7),
#            fontsize=9)

plt.tight_layout()
plt.show()