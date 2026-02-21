import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Create synthetic data for heatmap visualization
connections = [1, 10, 25, 50]
metrics = ['Throughput\n(Mbps)', 'Latency\n(ms)', 'CPU Usage\n(%)', 'Efficiency\nScore']

# Data matrix (protocols x metrics x connections)
performance_matrix = np.array([
    # WireGuard
    [[858, 823, 805, 748],   # Throughput
     [11.1, 13.4, 14.4, 16.1], # Latency  
     [14.7, 18.5, 24.9, 35.6], # CPU
     [85.3, 81.5, 75.1, 64.4]], # Efficiency
    
    # OpenVPN
    [[332, 292, 241, 124],   # Throughput
     [25.9, 35.8, 43.0, 72.8], # Latency
     [47.0, 56.3, 71.8, 97.6], # CPU
     [53.1, 43.8, 28.2, 2.4]], # Efficiency
     
    # IPSec
    [[485, 463, 422, 316],   # Throughput
     [18.1, 23.7, 27.9, 43.7], # Latency
     [32.0, 38.9, 50.4, 69.6], # CPU
     [68.0, 61.1, 49.6, 30.5]]  # Efficiency
])

protocols = ['WireGuard', 'OpenVPN', 'IPSec']

# Create subplot grid
fig, axes = plt.subplots(3, 4, figsize=(16, 12))
# fig.suptitle('Comprehensive Performance Heatmap Analysis:\nVPN Protocols Across Varying Connection Loads', 
             # fontweight='bold', fontsize=16, y=0.95)

# Custom colormaps
cmap_throughput = 'Greens'
cmap_latency = 'Reds_r'  # Reversed - lower latency is better
cmap_cpu = 'Reds'
cmap_efficiency = 'viridis'

for i, protocol in enumerate(protocols):
    for j, metric in enumerate(metrics):
        ax = axes[i, j]
        data = performance_matrix[i, j, :]
        
        # Select appropriate colormap
        if j == 0:  # Throughput
            cmap = cmap_throughput
            vmin, vmax = 0, 900
        elif j == 1:  # Latency
            cmap = cmap_latency
            vmin, vmax = 0, 80
        elif j == 2:  # CPU Usage
            cmap = cmap_cpu
            vmin, vmax = 0, 100
        else:  # Efficiency
            cmap = cmap_efficiency
            vmin, vmax = 0, 100
        
        # Create heatmap cell
        im = ax.imshow([data], cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax)
        
        # Customize subplot
        if i == 0:
            ax.set_title(f'{metric}', fontweight='bold', fontsize=11, pad=10)
        if j == 0:
            ax.set_ylabel(protocol, fontweight='bold', fontsize=11, rotation=0, ha='right')
        
        ax.set_xticks(range(len(connections)))
        ax.set_xticklabels(connections)
        ax.set_yticks([])
        
        # Add value annotations
        for k, value in enumerate(data):
            color = 'white' if value > (vmax - vmin) / 2 else 'black'
            ax.text(k, 0, f'{value:.1f}', ha='center', va='center', 
                   fontweight='bold', fontsize=9, color=color)

# Add colorbars
for j, (metric, cmap) in enumerate(zip(metrics, [cmap_throughput, cmap_latency, cmap_cpu, cmap_efficiency])):
    cax = fig.add_axes([0.92, 0.15 + (3-j)*0.2, 0.02, 0.15])
    cb = plt.colorbar(axes[0,j].images[0], cax=cax)
    cb.set_label(metric.split('\n')[0], fontweight='bold', fontsize=9)

# Add overall analysis
analysis_text = (
    'Performance Summary:\n'
    '• WireGuard: Maintains high performance across all loads\n'
    '• OpenVPN: Severe degradation beyond 25 connections\n'
    '• IPSec: Moderate degradation, better than OpenVPN\n'
    '• Efficiency: WireGuard maintains >60% score at 50 connections'
)

# plt.figtext(0.02, 0.02, analysis_text, fontsize=10,
#            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))

plt.tight_layout()
plt.subplots_adjust(top=0.90, bottom=0.08)
plt.show()