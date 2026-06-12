# Network Flow Simulator (Edmonds-Karp Algorithm)

A Python-based desktop application that simulates and visualizes how data, traffic, or fluids move through a network. The program utilizes the **Edmonds-Karp algorithm** (Breadth-First Search) to compute the maximum possible flow from a source to a destination and automatically highlights system bottlenecks.

---

## 🌟 Features

* **Visual Step-by-Step Tracing:** Watch the algorithm find augmenting paths in real-time using Breadth-First Search (BFS).
* **Automatic Bottleneck Detection:** Once the simulation finishes, the app calculates and highlights the **Min-Cut** edges (the exact pipelines causing the traffic or restriction).
* **Interactive Network Builder:** Easily add custom nodes, set path capacities, and configure your Source (S) and Sink (T) points through the interface.
* **Built-in Demo Network:** Comes pre-loaded with a default network configuration so you can test and evaluate the algorithm immediately with a single click.

---

## 🛠️ Built With

* **Python** - Core programming language.
* **Tkinter** - Python's standard GUI (Graphical User Interface) framework used to build the control panel and data display area.
* **Collections (Deque)** - Used to manage the double-ended queue for fast, efficient BFS path tracking.

---

## ⚙️ How It Works

1. **Path Finding (BFS):** The simulator scans the network to find the shortest available path from the Source to the Sink that still has remaining capacity.
2. **Flow Augmentation:** It identifies the tightest bottleneck along that path and pushes as much flow as possible through it.
3. **Min-Cut Calculation:** When no more paths can be found, the simulation stops and cuts the network into reachable and unreachable sections, revealing the core bottlenecks.

---

## 🚀 Getting Started

### Prerequisites
This project uses Python's built-in libraries, meaning **no external `pip` installations are required** to run it.

### Running the Application
Simply run the script using your terminal:

```bash
python network_flow_simulator.py
