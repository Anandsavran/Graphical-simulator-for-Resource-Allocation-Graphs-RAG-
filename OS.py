import tkinter as tk
from tkinter import messagebox, simpledialog
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Module 1: GUI & User Interaction
class GUI:
    def __init__(self, root, graph_handler):
        self.root = root
        self.root.title("Resource Allocation Graph Simulator")
        self.graph_handler = graph_handler

        # UI Buttons
        self.add_process_btn = tk.Button(root, text="Add Process", command=self.graph_handler.add_process)
        self.add_process_btn.pack(pady=5)

        self.add_resource_btn = tk.Button(root, text="Add Resource", command=self.graph_handler.add_resource)
        self.add_resource_btn.pack(pady=5)

        self.add_request_btn = tk.Button(root, text="Request Resource", command=self.graph_handler.request_resource)
        self.add_request_btn.pack(pady=5)

        self.add_allocation_btn = tk.Button(root, text="Allocate Resource", command=self.graph_handler.allocate_resource)
        self.add_allocation_btn.pack(pady=5)

        self.detect_deadlock_btn = tk.Button(root, text="Detect Deadlock", command=self.graph_handler.detect_deadlock)
        self.detect_deadlock_btn.pack(pady=5)

        self.show_graph_btn = tk.Button(root, text="Show Graph", command=self.graph_handler.show_graph)
        self.show_graph_btn.pack(pady=5)


# Module 2: Graph Data Handling & Deadlock Detection
class GraphHandler:
    def __init__(self, update_graph_callback):
        self.graph = nx.DiGraph()  # Directed graph
        self.processes = set()
        self.resources = set()
        self.update_graph_callback = update_graph_callback

    def add_process(self):
        process = simpledialog.askstring("Input", "Enter Process Name (e.g., P1):")
        if process and process not in self.processes:
            self.processes.add(process)
            self.graph.add_node(process, color='lightblue', shape='o')  # Light blue for process
            self.update_graph_callback(self.graph)  # Pass the graph
        else:
            messagebox.showerror("Error", "Process already exists or invalid input.")

    def add_resource(self):
        resource = simpledialog.askstring("Input", "Enter Resource Name (e.g., R1):")
        if resource and resource not in self.resources:
            self.resources.add(resource)
            self.graph.add_node(resource, color='gray', shape='s')  # Gray for resource
            self.update_graph_callback(self.graph)  # Pass the graph
        else:
            messagebox.showerror("Error", "Resource already exists or invalid input.")

    def request_resource(self):
        process = simpledialog.askstring("Input", "Enter Process Name:")
        resource = simpledialog.askstring("Input", "Enter Resource Name:")
        if process in self.processes and resource in self.resources:
            self.graph.add_edge(process, resource, color='orange')  # Request edge
            self.update_graph_callback(self.graph)  # Pass the graph
        else:
            messagebox.showerror("Error", "Invalid Process or Resource.")

    def allocate_resource(self):
        resource = simpledialog.askstring("Input", "Enter Resource Name:")
        process = simpledialog.askstring("Input", "Enter Process Name:")
        if resource in self.resources and process in self.processes:
            self.graph.add_edge(resource, process, color='green')  # Allocation edge
            self.update_graph_callback(self.graph)  # Pass the graph
        else:
            messagebox.showerror("Error", "Invalid Resource or Process.")

    def detect_deadlock(self):
        try:
            cycles = list(nx.simple_cycles(self.graph))
            if cycles:
                messagebox.showwarning("Deadlock Detected!", f"Deadlock in: {cycles}")
            else:
                messagebox.showinfo("No Deadlock", "No deadlock detected.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_graph(self):
        self.update_graph_callback(self.graph)  # Pass the graph


# Module 3: Data Visualization & Simulation
class GraphVisualizer:
    def __init__(self, root):
        self.figure = plt.Figure(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(pady=5)

    def update_graph(self, graph):
        self.figure.clear()
        pos = nx.spring_layout(graph)

        node_colors = [graph.nodes[n].get('color', 'black') for n in graph.nodes]
        edge_colors = [graph[u][v].get('color', 'black') for u, v in graph.edges]

        nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors,
                node_size=1500, font_size=10, ax=self.figure.add_subplot(111))
        self.canvas.draw()

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    visualizer = GraphVisualizer(root)
    graph_handler = GraphHandler(visualizer.update_graph)
    app = GUI(root, graph_handler)
    root.mainloop()
