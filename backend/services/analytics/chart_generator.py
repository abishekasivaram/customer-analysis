import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
from pathlib import Path

class ChartGenerator:
    def __init__(self):
        # Setup seaborn style
        sns.set_theme(style="whitegrid")
        
    def generate(self, behaviors_json, zone_analytics_json, base_name):
        out_dir = Path("outputs/analytics/charts")
        
        with open(behaviors_json, 'r') as f:
            behaviors = json.load(f)
            
        with open(zone_analytics_json, 'r') as f:
            zones = json.load(f)
            
        if not behaviors:
            return
            
        df = pd.DataFrame(behaviors)
        
        # 1. Behavior Distribution Chart
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='behavior', hue='behavior', legend=False)
        plt.title('Behavior Distribution')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(str(out_dir / f"{base_name}_behavior_distribution.png"))
        plt.close()
        
        # 2. Behavior Timeline Chart
        plt.figure(figsize=(12, 6))
        for index, row in df.iterrows():
            plt.plot([row['start_time'], row['end_time']], [row['track_id'], row['track_id']], marker='|')
        plt.title('Behavior Timeline by Customer ID')
        plt.xlabel('Time (s)')
        plt.ylabel('Customer ID')
        plt.tight_layout()
        plt.savefig(str(out_dir / f"{base_name}_behavior_timeline.png"))
        plt.close()
        
        # 3. Detection Confidence Distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='confidence', bins=20, kde=True)
        plt.title('Behavior Confidence Distribution')
        plt.tight_layout()
        plt.savefig(str(out_dir / f"{base_name}_confidence_distribution.png"))
        plt.close()
        
        # 4. Track Duration Histogram
        df['duration'] = df['end_time'] - df['start_time']
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='duration', bins=20)
        plt.title('Track Duration Histogram')
        plt.xlabel('Duration (s)')
        plt.tight_layout()
        plt.savefig(str(out_dir / f"{base_name}_duration_histogram.png"))
        plt.close()
        
        # 5. Zone Occupancy Chart
        if zones:
            zdf = pd.DataFrame(zones)
            plt.figure(figsize=(10, 6))
            sns.barplot(data=zdf, x='zone_name', y='customer_count')
            plt.title('Zone Occupancy (Unique Visitors)')
            plt.tight_layout()
            plt.savefig(str(out_dir / f"{base_name}_zone_occupancy.png"))
            plt.close()
