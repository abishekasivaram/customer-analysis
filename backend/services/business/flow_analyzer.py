import os
import json
import glob
import csv
import matplotlib.pyplot as plt
import networkx as nx
from backend.core.logger import bus_logger

class FlowAnalyzer:
    def __init__(self):
        self.output_dir = "outputs/business"
        self.graph_dir = os.path.join(self.output_dir, "graphs")
        os.makedirs(self.graph_dir, exist_ok=True)
        
    def analyze(self):
        bus_logger.info("Starting Customer Flow analysis.")
        timeline_files = glob.glob("outputs/behavior/timeline/*_timeline.json")
        
        # We will build a simple transition matrix between behaviors (as a proxy for zones)
        transitions = {}
        entry_paths = {}
        exit_paths = {}
        
        for tf in timeline_files:
            with open(tf, 'r') as f:
                events = json.load(f)
                
            # Group by track_id
            tracks = {}
            for ev in events:
                tid = ev['track_id']
                if tid not in tracks:
                    tracks[tid] = []
                tracks[tid].append(ev['behavior'])
                
            for tid, path in tracks.items():
                if not path: continue
                
                # Entry
                entry = path[0]
                entry_paths[entry] = entry_paths.get(entry, 0) + 1
                
                # Exit
                exit_beh = path[-1]
                exit_paths[exit_beh] = exit_paths.get(exit_beh, 0) + 1
                
                # Transitions
                for i in range(len(path)-1):
                    source = path[i]
                    target = path[i+1]
                    if source != target: # Skip self loops for flow network
                        pair = (source, target)
                        transitions[pair] = transitions.get(pair, 0) + 1
                        
        flow_data = {
            "flow_network": [{"source": k[0], "target": k[1], "weight": v} for k, v in transitions.items()],
            "entry_paths": entry_paths,
            "exit_paths": exit_paths,
            "most_common_route": max(transitions, key=transitions.get) if transitions else None,
            "least_used_route": min(transitions, key=transitions.get) if transitions else None,
            "dead_zones": [], # Derived from zone data ideally, empty for now
            "congested_areas": [] # Same
        }
        
        # Save JSON
        with open(os.path.join(self.output_dir, "customer_flow.json"), 'w') as f:
            json.dump(flow_data, f, indent=4)
            
        # Draw Networkx graph
        self._draw_network_graph(transitions)
            
        bus_logger.info("Customer Flow analysis completed.")
        return flow_data
        
    def _draw_network_graph(self, transitions):
        try:
            G = nx.DiGraph()
            for (u, v), w in transitions.items():
                G.add_edge(u, v, weight=w)
                
            plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(G)
            
            # Edges
            weights = [G[u][v]['weight'] for u,v in G.edges()]
            if weights:
                max_w = max(weights)
                widths = [(w/max_w)*5 for w in weights]
            else:
                widths = 1.0
                
            nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
            nx.draw_networkx_edges(G, pos, width=widths, arrowsize=20, edge_color='gray')
            nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
            
            plt.title("Customer Flow Network")
            plt.axis('off')
            plt.tight_layout()
            
            plt.savefig(os.path.join(self.graph_dir, "customer_flow_graph.png"), dpi=150)
            plt.savefig(os.path.join(self.graph_dir, "zone_transition_graph.png"), dpi=150) # Alias
            plt.close()
        except Exception as e:
            bus_logger.error(f"Failed to generate flow graph: {e}")
