import matplotlib.pyplot as plt
import numpy as np

# Data dari regression coefficients
regression_data = {
    'protocol': ['WireGuard', 'OpenVPN', 'IPSec'],
    'throughput_coef': [-2.0868, -4.1447, -3.4014],
    'throughput_intercept': [849.64, 329.39, 488.08],
    'throughput_r2': [0.6041, 0.8875, 0.7606],
    'latency_coef': [0.0915, 0.9607, 0.5230],
    'latency_intercept': [11.92, 24.66, 17.60],
    'latency_r2': [0.3937, 0.9542, 0.9107]
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Throughput Regression Coefficients
x_pos = np.arange(len(regression_data['protocol']))
width = 0.35

# Throughput degradation rates (negative coefficients)
ax1.bar(x_pos - width/2, np.abs(regression_data['throughput_coef']), width,
        label='Throughput Degradation Rate', color='#2E86AB', alpha=0.8, edgecolor='black')

# R-squared values
ax1_twin = ax1.twinx()
ax1_twin.bar(x_pos + width/2, regression_data['throughput_r2'], width,
             label='R² (Goodness of Fit)', color='#F18F01', alpha=0.8, edgecolor='black')

ax1.set_xlabel('VPN Protocol', fontweight='bold', fontsize=12)
ax1.set_ylabel('Throughput Degradation Rate\n(Mbps loss per connection)', fontweight='bold', fontsize=10)
ax1_twin.set_ylabel('R-squared (Goodness of Fit)', fontweight='bold', fontsize=10)
ax1.set_title('A. Throughput Regression Model Parameters', 
              fontweight='bold', fontsize=13, pad=15)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(regression_data['protocol'])
ax1.legend(loc='upper left')
ax1_twin.legend(loc='upper right')
ax1.grid(True, alpha=0.3, axis='y')

# Plot 2: Latency Regression Coefficients
# Latency increase rates (positive coefficients)
ax2.bar(x_pos - width/2, regression_data['latency_coef'], width,
        label='Latency Increase Rate', color='#A23B72', alpha=0.8, edgecolor='black')

# R-squared values
ax2_twin = ax2.twinx()
ax2_twin.bar(x_pos + width/2, regression_data['latency_r2'], width,
             label='R² (Goodness of Fit)', color='#1B998B', alpha=0.8, edgecolor='black')

ax2.set_xlabel('VPN Protocol', fontweight='bold', fontsize=12)
ax2.set_ylabel('Latency Increase Rate\n(ms increase per connection)', fontweight='bold', fontsize=10)
ax2_twin.set_ylabel('R-squared (Goodness of Fit)', fontweight='bold', fontsize=10)
ax2.set_title('B. Latency Regression Model Parameters', 
              fontweight='bold', fontsize=13, pad=15)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(regression_data['protocol'])
ax2.legend(loc='upper left')
ax2_twin.legend(loc='upper right')
ax2.grid(True, alpha=0.3, axis='y')

plt.suptitle('Regression Model Analysis: Performance Prediction Accuracy', 
             fontweight='bold', fontsize=16, y=0.98)

# Add model interpretation
model_analysis = (
    'Model Interpretation:\n'
    '• OpenVPN models show highest accuracy (R² > 0.88)\n'
    '• WireGuard throughput model has lower R² (0.60)\n'
    '• OpenVPN latency degrades fastest (+0.96ms/conn)\n'
    '• WireGuard shows most stable performance'
)

# plt.figtext(0.02, 0.02, model_analysis, fontsize=9,
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))

plt.tight_layout()
plt.show()