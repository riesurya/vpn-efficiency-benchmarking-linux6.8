import pandas as pd
import altair as alt
import json

# List of file names
files = [
    'openvpn_bidirectional.json',
    'wireguard_single.json',
    'openvpn_single.json',
    'ipsec_bidirectional.json',
    'ipsec_single.json',
    'wireguard_bidirectional.json'
]

# --- 1. Data Processing for Average Throughput and CPU ---
avg_throughput_data = []
cpu_data = []

for f in files:
    with open(f, 'r') as file:
        data = json.load(file)
    
    # Extract VPN name from filename
    if 'wireguard' in f:
        vpn = 'WireGuard'
    elif 'openvpn' in f:
        vpn = 'OpenVPN'
    elif 'ipsec' in f:
        vpn = 'IPsec'
    else:
        vpn = 'Unknown'
        
    # Extract test type
    is_bidirectional = 'bidirectional' in f
    
    # Get end summary data
    end_summary = data.get('end', {})
    
    if is_bidirectional:
        test_type_label = 'Bidirectional'
        # Bidirectional (Send)
        sum_sent = end_summary.get('sum_sent', {})
        avg_throughput_data.append({
            'vpn': vpn,
            'type': 'Bidirectional (Send)',
            'throughput_gbps': sum_sent.get('bits_per_second', 0) / 1_000_000_000
        })
        # Bidirectional (Receive)
        sum_received_reverse = end_summary.get('sum_received_bidir_reverse', {})
        avg_throughput_data.append({
            'vpn': vpn,
            'type': 'Bidirectional (Receive)',
            'throughput_gbps': sum_received_reverse.get('bits_per_second', 0) / 1_000_000_000
        })
    else:
        test_type_label = 'Unidirectional'
        # Unidirectional (Send)
        sum_sent = end_summary.get('sum_sent', {})
        avg_throughput_data.append({
            'vpn': vpn,
            'type': 'Unidirectional',
            'throughput_gbps': sum_sent.get('bits_per_second', 0) / 1_000_000_000
        })
    
    # Get CPU data
    cpu_util = end_summary.get('cpu_utilization_percent', {})
    cpu_data.append({
        'vpn': vpn,
        'type': test_type_label,
        'cpu_percent': cpu_util.get('host_total', 0)
    })

# Create DataFrames
df_avg_throughput = pd.DataFrame(avg_throughput_data)
df_cpu = pd.DataFrame(cpu_data).drop_duplicates()

# --- 2. Data Processing for Throughput Stability (Unidirectional only) ---
stability_data = []
single_files = [f for f in files if 'single' in f]

for f in single_files:
    with open(f, 'r') as file:
        data = json.load(file)
    
    if 'wireguard' in f:
        vpn = 'WireGuard'
    elif 'openvpn' in f:
        vpn = 'OpenVPN'
    elif 'ipsec' in f:
        vpn = 'IPsec'
    
    intervals = data.get('intervals', [])
    for interval in intervals:
        sum_data = interval.get('sum', {})
        stability_data.append({
            'vpn': vpn,
            'time': sum_data.get('end', 0),
            'throughput_gbps': sum_data.get('bits_per_second', 0) / 1_000_000_000
        })

df_stability = pd.DataFrame(stability_data)

# --- 3. Create Charts ---

# Chart 1: Average Throughput Comparison (Faceted Grouped Bar Chart)
chart_avg_throughput = alt.Chart(df_avg_throughput).mark_bar().encode(
    x=alt.X('type', title=None, axis=None),
    y=alt.Y('throughput_gbps', title='Throughput Rata-rata (Gbps)'),
    color=alt.Color('type', title='Tipe Aliran Data'),
    column=alt.Column('vpn', title='Protokol VPN', header=alt.Header(titleOrient="bottom", labelOrient="bottom")),
    tooltip=['vpn', 'type', 'throughput_gbps']
).properties(
    title='Perbandingan Throughput Rata-rata VPN'
).interactive()

# Chart 2: Throughput Stability (Multi-Line Chart)
chart_stability = alt.Chart(df_stability).mark_line(point=True).encode(
    x=alt.X('time', title='Waktu (Detik)'),
    y=alt.Y('throughput_gbps', title='Throughput (Gbps)', scale=alt.Scale(zero=False)),
    color=alt.Color('vpn', title='Protokol VPN'),
    tooltip=['time', 'vpn', 'throughput_gbps']
).properties(
    title='Stabilitas Throughput Unidirectional (Single Stream)'
).interactive()

# Chart 3: CPU Utilization Comparison (Faceted Grouped Bar Chart)
chart_cpu = alt.Chart(df_cpu).mark_bar().encode(
    x=alt.X('type', title=None, axis=None),
    y=alt.Y('cpu_percent', title='Total Penggunaan CPU Host (%)'),
    color=alt.Color('type', title='Tipe Tes'),
    column=alt.Column('vpn', title='Protokol VPN', header=alt.Header(titleOrient="bottom", labelOrient="bottom")),
    tooltip=['vpn', 'type', 'cpu_percent']
).properties(
    title='Perbandingan Rata-rata Penggunaan CPU'
).interactive()

# Save charts
chart_avg_throughput.save('average_throughput_comparison.json')
chart_stability.save('throughput_stability_unidirectional.json')
chart_cpu.save('cpu_utilization_comparison.json')

print("Visualisasi telah dibuat dan disimpan sebagai file JSON.")