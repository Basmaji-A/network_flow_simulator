import tkinter as tk
from tkinter import messagebox, ttk
import collections

class NetworkFlowSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Flow Simulator - Edmonds-Karp Algorithm")
        self.root.geometry("1000x700")
        
        # Graph Data Structures
        # { u: { v: { 'capacity': C, 'flow': F } } }
        self.graph = {}
        self.nodes = set()
        self.source = None
        self.sink = None
        
        # Simulation Control Variables
        self.simulation_active = False
        self.current_path = []
        self.bottleneck = 0
        self.max_flow_value = 0
        self.min_cut_edges = []

        self.setup_ui()

    def setup_ui(self):
        """Build the English User Interface"""
        # Top Frame: Control and Inputs
        control_frame = ttk.LabelFrame(self.root, text=" Control Panel & Data Input ")
        control_frame.pack(fill="x", padx=10, pady=5)

        # Add Node Components
        ttk.Label(control_frame, text="Node Name:").grid(row=0, column=0, padx=5, pady=5)
        self.node_entry = ttk.Entry(control_frame, width=10)
        self.node_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(control_frame, text="Add Node", command=self.add_node).grid(row=0, column=2, padx=5, pady=5)

        # Add Edge Components (Pipeline/Traffic)
        ttk.Label(control_frame, text="From:").grid(row=0, column=3, padx=5, pady=5)
        self.from_entry = ttk.Entry(control_frame, width=5)
        self.from_entry.grid(row=0, column=4, padx=5, pady=5)
        
        ttk.Label(control_frame, text="To:").grid(row=0, column=5, padx=5, pady=5)
        self.to_entry = ttk.Entry(control_frame, width=5)
        self.to_entry.grid(row=0, column=6, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Capacity:").grid(row=0, column=7, padx=5, pady=5)
        self.cap_entry = ttk.Entry(control_frame, width=8)
        self.cap_entry.grid(row=0, column=8, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Add Edge", command=self.add_edge).grid(row=0, column=9, padx=5, pady=5)

        # Source and Sink configuration
        ttk.Label(control_frame, text="Source (S):").grid(row=1, column=0, padx=5, pady=5)
        self.source_entry = ttk.Entry(control_frame, width=10)
        self.source_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Sink (T):").grid(row=1, column=3, padx=5, pady=5)
        self.sink_entry = ttk.Entry(control_frame, width=10)
        self.sink_entry.grid(row=1, column=4, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Set Source & Sink", command=self.set_source_sink).grid(row=1, column=5, columnspan=2, padx=5, pady=5)

        # Simulation Controls Frame (Gamification & Stepping)
        sim_frame = ttk.LabelFrame(self.root, text=" Simulation Controls & Step-by-Step Tracing ")
        sim_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(sim_frame, text="🚀 Start Simulation", command=self.start_simulation).pack(side="left", padx=10, pady=5)
        ttk.Button(sim_frame, text="⏭️ Next Step (BFS)", command=self.next_step).pack(side="left", padx=10, pady=5)
        ttk.Button(sim_frame, text="🔄 Reset Graph", command=self.reset_graph).pack(side="left", padx=10, pady=5)
        
        self.flow_label = ttk.Label(sim_frame, text="Current Max Flow: 0", font=("Helvetica", 12, "bold"))
        self.flow_label.pack(side="right", padx=20)

        # Visualization Display Area
        self.txt_display = tk.Text(self.root, font=("Courier New", 11), bg="#f4f4f4")
        self.txt_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Automatically load demo network for easy testing
        self.load_demo_graph()

    def load_demo_graph(self):
        """Loads a pre-defined flow network to save time during evaluation"""
        demo_edges = [
            ('S', 'A', 10), ('S', 'B', 10),
            ('A', 'B', 2),  ('A', 'C', 4), ('A', 'D', 8),
            ('B', 'D', 9),  ('C', 'T', 10), ('D', 'C', 6), ('D', 'T', 10)
        ]
        for u, v, c in demo_edges:
            self.nodes.add(u)
            self.nodes.add(v)
            if u not in self.graph: self.graph[u] = {}
            self.graph[u][v] = {'capacity': c, 'flow': 0}
        self.source = 'S'
        self.sink = 'T'
        self.source_entry.insert(0, 'S')
        self.sink_entry.insert(0, 'T')
        self.update_display("Demo network loaded successfully! Click 'Start Simulation' to begin.")

    def add_node(self):
        node = self.node_entry.get().strip()
        if node:
            self.nodes.add(node)
            self.node_entry.delete(0, tk.END)
            self.update_display(f"Node added: {node}")

    def add_edge(self):
        u = self.from_entry.get().strip()
        v = self.to_entry.get().strip()
        try:
            cap = int(self.cap_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Capacity must be an integer.")
            return

        if u and v and cap > 0:
            self.nodes.add(u)
            self.nodes.add(v)
            if u not in self.graph: self.graph[u] = {}
            self.graph[u][v] = {'capacity': cap, 'flow': 0}
            self.from_entry.delete(0, tk.END)
            self.to_entry.delete(0, tk.END)
            self.cap_entry.delete(0, tk.END)
            self.update_display(f"Edge added from {u} to {v} with capacity {cap}")

    def set_source_sink(self):
        s = self.source_entry.get().strip()
        t = self.sink_entry.get().strip()
        if s in self.nodes and t in self.nodes:
            self.source = s
            self.sink = t
            self.update_display(f"Source set to: {s} | Sink set to: {t}")
        else:
            messagebox.showerror("Error", "Source or Sink node does not exist.")

    def update_display(self, message=""):
        """Updates the textual UI trace, displaying flows and marking bottlenecks"""
        self.txt_display.delete("1.0", tk.END)
        if message:
            self.txt_display.insert(tk.END, f"🔔 SYSTEM STATUS: {message}\n")
            self.txt_display.insert(tk.END, "="*70 + "\n\n")
        
        self.txt_display.insert(tk.END, "📊 Current Flow Network State (Source -> Sink):\n")
        for u in sorted(self.graph.keys()):
            for v, data in sorted(self.graph[u].items()):
                flow = data['flow']
                cap = data['capacity']
                
                is_min_cut = (u, v) in self.min_cut_edges
                edge_str = f"  {u} ──({flow}/{cap})──> {v}"
                
                # Gamification & Highlighting Visual Traces
                if is_min_cut:
                    edge_str += "  ❌ [BOTTLENECK - MIN CUT] ❌"
                elif (u, v) in zip(self.current_path, self.current_path[1:]):
                    edge_str += "  ⭐ [ACTIVE AUGMENTING PATH] ⭐"
                
                self.txt_display.insert(tk.END, edge_str + "\n")
        
        self.flow_label.config(text=f"Current Max Flow: {self.max_flow_value}")

    # ────────────── Edmonds-Karp O(V E^2) Algorithm ──────────────
    
    def start_simulation(self):
        if not self.source or not self.sink:
            messagebox.showerror("Error", "Please set Source and Sink nodes first.")
            return
        
        # Reset all flows to 0
        for u in self.graph:
            for v in self.graph[u]:
                self.graph[u][v]['flow'] = 0
                
        self.max_flow_value = 0
        self.simulation_active = True
        self.min_cut_edges = []
        self.update_display("Simulation started. Click 'Next Step (BFS)' to trace paths.")

    def bfs_find_path(self):
        """BFS implementation to find the shortest augmenting path - O(E)"""
        parent = {self.source: None}
        queue = collections.deque([self.source])
        
        while queue:
            curr = queue.popleft()
            
            # Check forward edges
            if curr in self.graph:
                for nxt, data in self.graph[curr].items():
                    residual_cap = data['capacity'] - data['flow']
                    if nxt not in parent and residual_cap > 0:
                        parent[nxt] = curr
                        if nxt == self.sink:
                            return self.reconstruct_path(parent)
                        queue.append(nxt)
                        
            # Check backward edges in residual graph
            for u in self.graph:
                if curr in self.graph[u]:
                    data = self.graph[u][curr]
                    if u not in parent and data['flow'] > 0:
                        parent[u] = curr
                        if u == self.sink:
                            return self.reconstruct_path(parent)
                        queue.append(u)
        return None

    def reconstruct_path(self, parent):
        path = []
        curr = self.sink
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr)
        return path[::-1]

    def next_step(self):
        """Executes one single iteration of the Edmonds-Karp loop on button click"""
        if not self.simulation_active:
            messagebox.showwarning("Warning", "Please click 'Start Simulation' first.")
            return

        path = self.bfs_find_path()
        
        if path:
            self.current_path = path
            # 1. Compute bottleneck capacity
            bottleneck = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                if u in self.graph and v in self.graph[u]:
                    res_cap = self.graph[u][v]['capacity'] - self.graph[u][v]['flow']
                else:
                    res_cap = self.graph[v][u]['flow']
                bottleneck = min(bottleneck, res_cap)
            
            self.bottleneck = bottleneck
            
            # 2. Augment the flow along the path
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                if u in self.graph and v in self.graph[u]:
                    self.graph[u][v]['flow'] += bottleneck
                else:
                    self.graph[v][u]['flow'] -= bottleneck
            
            self.max_flow_value += bottleneck
            self.update_display(f"BFS found path: {' -> '.join(path)} | Bottleneck = {bottleneck}")
        else:
            # No more augmenting paths -> Algorithm finished, compute Min-Cut
            self.simulation_active = False
            self.current_path = []
            self.calculate_min_cut()
            self.update_display("🏁 Algorithm Finished! No more augmenting paths. Min-Cut edges highlighted below.")

    def calculate_min_cut(self):
        """Finds the minimum cut by identifying reachable nodes in the residual graph"""
        visited = {self.source}
        queue = collections.deque([self.source])
        
        while queue:
            curr = queue.popleft()
            if curr in self.graph:
                for nxt, data in self.graph[curr].items():
                    if nxt not in visited and (data['capacity'] - data['flow'] > 0):
                        visited.add(nxt)
                        queue.append(nxt)
            for u in self.graph:
                if curr in self.graph[u] and u not in visited and self.graph[u][curr]['flow'] > 0:
                    visited.add(u)
                    queue.append(u)
                    
        # Edges from visited to unvisited nodes form the Min-Cut
        self.min_cut_edges = []
        for u in self.graph:
            if u in visited:
                for v in self.graph[u]:
                    if v not in visited:
                        self.min_cut_edges.append((u, v))

    def reset_graph(self):
        self.graph = {}
        self.nodes = set()
        self.source = None
        self.sink = None
        self.max_flow_value = 0
        self.min_cut_edges = []
        self.simulation_active = False
        self.current_path = []
        self.source_entry.delete(0, tk.END)
        self.sink_entry.delete(0, tk.END)
        self.update_display("Graph reset. Ready to enter a new network.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkFlowSimulator(root)
    root.mainloop()