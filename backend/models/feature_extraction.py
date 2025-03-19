import nfstream
import pandas as pd

def extract_features(interface, output_csv):
    """Extracts network traffic features using NFStreamer and saves to CSV."""
    print(f"Starting real-time traffic feature extraction on {interface}...")

    # Initialize NFStreamer
    stream = nfstream.NFStreamer(
        source=interface, 
        decode_tunnels=True,
        promiscuous_mode=True,
        snapshot_length=1536,
        active_timeout=1800,
        statistical_analysis=True,
        splt_analysis=7,  # First 7 packet stats
        n_dissections=20   # Extracts L7 metadata
    )

    data = []

    for flow in stream:
        feature_dict = {
            "src_ip": flow.src_ip,
            "dst_ip": flow.dst_ip,
            "src_port": flow.src_port,
            "dst_port": flow.dst_port,
            "protocol": flow.protocol,
            "requested_server_name": flow.requested_server_name,
            "application_name": flow.application_name,
            "application_category_name": flow.application_category_name,
            "client_fingerprint": flow.client_fingerprint,
            "server_fingerprint": flow.server_fingerprint,
            "bidirectional_packets": flow.bidirectional_packets,
            "bidirectional_bytes": flow.bidirectional_bytes,
            "bidirectional_mean_ps": flow.bidirectional_mean_ps,
            "bidirectional_stddev_ps": flow.bidirectional_stddev_ps,
            "bidirectional_mean_piat_ms": flow.bidirectional_mean_piat_ms,
            "bidirectional_stddev_piat_ms": flow.bidirectional_stddev_piat_ms,
            "bidirectional_syn_packets": flow.bidirectional_syn_packets,
            "bidirectional_ack_packets": flow.bidirectional_ack_packets,
            "bidirectional_rst_packets": flow.bidirectional_rst_packets,
            "splt_ps": flow.splt_ps,  # Early packet size pattern
            "splt_piat_ms": flow.splt_piat_ms  # Early packet timing pattern
        }

        data.append(feature_dict)

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Feature extraction completed! Results saved in {output_csv}")

if __name__ == "__main__":
    extract_features("eth0", "data/training_data.csv")
