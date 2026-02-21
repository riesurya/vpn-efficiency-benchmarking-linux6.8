import matplotlib.pyplot as plt
import numpy as np

# Data untuk scalability analysis
protocols = ['WireGuard', 'OpenVPN', 'IPSec']
max_connections = [100, 25, 50]
cpu_at_50 = [35.61, 97.61, 69.55]
efficiency_scores = [69.85, 25.49, 41.82]

# Create scatter plot dengan bubble size berdasarkan efficiency score
bubble_sizes = [score * 20 for score in efficiency_scores]  # Scale untuk visualisasi

fig, ax = plt.subplots(figsize=(12, 8))

# Create scatter plot dengan bubbles
scatter = ax.scatter(max_connections, cpu_at_50, s=bubble_sizes, 
                     c=efficiency_scores, cmap='viridis', alpha=0.7,
                     edgecolors='black', linewidth=1.5)

# Add protocol labels
for i, protocol in enumerate(protocols):
    ax.annotate(protocol, (max_connections[i], cpu_at_50[i]),
                xytext=(10, 10), textcoords='offset points',
                fontweight='bold', fontsize=11,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

# Customize plot
ax.set_xlabel('Maximum Connections at 80% CPU Load', fontweight='bold', fontsize=12)
ax.set_ylabel('CPU Usage at 50 Connections (%)', fontweight='bold', fontsize=12)
ax.set_title('Scalability vs Resource Efficiency:\nVPN Protocols Performance Trade-off', 
             fontweight='bold', fontsize=14, pad=20)

# Add grid and set limits
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 110)
ax.set_ylim(30, 105)

# Add colorbar untuk efficiency scores
cbar = plt.colorbar(scatter)
cbar.set_label('Efficiency Score', fontweight='bold', fontsize=11)

# Add optimal quadrant annotations
ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, linewidth=1)
ax.axvline(x=50, color='red', linestyle='--', alpha=0.5, linewidth=1)

ax.text(75, 40, 'High Scalability\nLow CPU Usage\n(Optimal)', 
        fontweight='bold', fontsize=10, ha='center',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))

ax.text(20, 40, 'Low Scalability\nLow CPU Usage', 
        fontsize=9, ha='center',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7))

ax.text(20, 80, 'Low Scalability\nHigh CPU Usage\n(Least Efficient)', 
        fontsize=9, ha='center',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.7))

# Add performance summary
summary_text = (
    'Resource Efficiency Ranking:\n'
    '1. WireGuard: High scalability + Low CPU usage\n'
    '2. IPSec: Moderate scalability + Medium CPU usage\n'
    '3. OpenVPN: Low scalability + High CPU usage\n\n'
    'WireGuard achieves 4x better scalability\nthan OpenVPN at same CPU constraints'
)

# plt.figtext(0.09, 0.14, summary_text, fontsize=10,
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))

plt.tight_layout()
plt.show()

# Print numerical analysis
print("RESOURCE EFFICIENCY NUMERICAL ANALYSIS")
print("="*55)
print(f"{'Protocol':<12} {'Eff. Score':<12} {'Max Conn':<12} {'CPU @50':<12} {'Conn/CPU Ratio':<15}")
print("-"*55)
for i, protocol in enumerate(protocols):
    conn_cpu_ratio = max_connections[i] / (cpu_at_50[i] / 100)  # Connections per 1% CPU
    print(f"{protocol:<12} {efficiency_scores[i]:<12.1f} {max_connections[i]:<12} {cpu_at_50[i]:<12.1f} {conn_cpu_ratio:<15.1f}")