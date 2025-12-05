import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class CustomerSegmenter:
    def __init__(self, n_segments=3):
        self.n_segments = n_segments
        self.kmeans = KMeans(n_clusters=n_segments, random_state=42)
        self.scaler = StandardScaler()

    def segment_customers(self, customer_data):
        """
        Segment customers based on RFM (Recency, Frequency, Monetary) analysis.
        
        Args:
            customer_data: List of dicts with keys: customer_id, recency, frequency, monetary
        
        Returns:
            Dict mapping customer_id to segment_id
        """
        if not customer_data or len(customer_data) < self.n_segments:
            # Not enough data, assign all to segment 0
            return {item['customer_id']: 0 for item in customer_data}
        
        # Extract features
        customer_ids = [item['customer_id'] for item in customer_data]
        features = np.array([
            [item['recency'], item['frequency'], item['monetary']]
            for item in customer_data
        ])
        
        # Normalize features
        features_scaled = self.scaler.fit_transform(features)
        
        # Perform clustering
        cluster_labels = self.kmeans.fit_predict(features_scaled)
        
        # Map segment IDs (0=Low Value, 1=Medium Value, 2=High Value)
        # Based on mean monetary value of each cluster
        cluster_means = []
        for i in range(self.n_segments):
            cluster_mask = cluster_labels == i
            if cluster_mask.any():
                mean_monetary = features[cluster_mask, 2].mean()
                cluster_means.append((i, mean_monetary))
        
        # Sort by monetary value
        cluster_means.sort(key=lambda x: x[1])
        
        # Create mapping: original_cluster -> ranked_segment
        segment_mapping = {cluster_means[i][0]: i for i in range(len(cluster_means))}
        
        # Map customers to segments
        result = {}
        for customer_id, cluster_id in zip(customer_ids, cluster_labels):
            result[customer_id] = segment_mapping[cluster_id]
        
        return result
