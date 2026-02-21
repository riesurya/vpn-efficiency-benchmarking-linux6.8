import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Data correlation matrix
correlation_data = {
    'throughput_mbps': [1.0, -0.8648, -0.8574, -0.8614, -0.6826],
    'latency_ms': [-0.8648, 1.0, 0.8173, 0.8195, 0.4906],
    'cpu_usage': [-0.8574, 0.8173, 1.0, 0.8325, 0.4429],
    'memory_mb': [-0.8614, 0.8195, 0.8325, 1.0, 0.3553],
    'protocol_num': [-0.6826, 0.4906, 0.4429, 0.3553, 1.0]
}

corr_matrix = pd.DataFrame(correlation_data, 
                          index=['throughput_mbps', 'latency_ms', 'cpu_usage', 'memory_mb', 'protocol_num'])

plt.figure(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, 
            square=True, fmt='.3f', cbar_kws={'shrink': 0.8},
            mask=mask, annot_kws={'size': 10, 'weight': 'bold'})

plt.title('Correlation Matrix: VPN Performance Metrics Relationships\n', 
          fontsize=14, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()

# Add insights
plt.figtext(0.02, 0.02, 
           'Key Insights:\n'
           '• Throughput strongly negatively correlated with latency (-0.865)\n'
           '• High CPU/memory usage associated with lower throughput\n'
           '• Protocol type shows moderate correlation with performance',
           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7),
           fontsize=9)

plt.show()