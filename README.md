# **Capacitated Pickup and Delivery Vehicle Routing Problem (PDVRP)**

A Python-based logistics optimization application that automatically assigns transport orders to available trucks and determines efficient pickup and delivery routes while respecting vehicle capacity, pickup-delivery precedence, and working-time constraints.

Built using **Python, Google OR-Tools, Streamlit, Pandas, and Matplotlib**.

## 1. Project Overview

The application solves a real-world logistics optimization problem: transporting construction machinery between multiple locations using a fleet of trucks.

The goal is to **minimize total distance traveled** while ensuring that every transport order is completed and all operational constraints are satisfied.

## 2. Configurable Inputs

Users can add, modify, or remove the following data directly through the web interface:

- **Vehicles:** Number of trucks, vehicle identifiers, maximum carrying capacity (kg), and maximum number of machines transported simultaneously.
- **Machines:** Machine identifiers and individual weights (kg).
- **Locations:** Location identifiers and X/Y coordinates in kilometers.
- **Transport Orders:** Machine assignments, pickup locations, and delivery locations.

The optimization model automatically adapts to changes in the input data.


### Hard Constraints(solution must satisfy):

- **Weight Capacity:** A truck cannot exceed its maximum carrying capacity at any point along its route.
- **Machine Count:** A truck cannot carry more than its permitted number of machines simultaneously.
- **Pickup Before Delivery:** Each machine must be collected before being delivered.
- **Same Vehicle:** The same truck must perform both pickup and delivery of an assigned machine.
- **Depot Return:** Every truck starts and finishes at the depot (L0).
- **Working Time:** Driving, loading, and unloading must fit within 9 hours per truck.
- **Order Completion:** All transport orders must be fulfilled.

### Optimization Objective

**Minimize the combined distance traveled by all trucks.**

### Optimization Algorithm

- **Solver:** Google OR-Tools Routing Solver
- **Initial Solution:** Parallel Cheapest Insertion
- **Local Search:** Guided Local Search (GLS)
- **Distance:** Euclidean distance, rounded to 0.1 km per segment
- **Average Speed:** 60 km/h
- **Loading / Unloading:** 20 minutes per operation

The solver searches for high-quality feasible solutions within a predefined time limit. It does not guarantee a globally optimal solution.


## 🚀 Installation & Getting Started

### Prerequisites

- **Python 3.11** (recommended)
- **pip** (Python package manager)

### 1. Install Dependencies

Open a terminal in the project directory and run:

```bash
python -m pip install -r requirements.txt
```

This installs all required libraries, including Streamlit, Google OR-Tools, Pandas, Matplotlib, and NetworkX.

### 2. Launch the Application

Start the Streamlit web application:

```bash
python -m streamlit run app.py
```

Once started, open the local URL displayed in your terminal, typically:

**http://localhost:8501**

### 3. Using the Application

1. **Load sample data** — Click `📥 Učitaj primjerne podatke` to populate the application with the provided dataset.
2. **Review and customize inputs** — Edit trucks, machines, locations, and transport orders directly in the interface.
3. **Run optimization** — Click `Optimiziraj rute` to calculate efficient transport routes.
4. **Analyze results** — Review truck assignments, total distances, completed orders, and estimated working hours.
5. **Explore routes** — Inspect the route visualization and the sequence of pickup and delivery locations.



## 9. Limitations and Future Improvements

- Euclidean distances are used instead of real road networks.
- Travel speed and handling times are assumed constant.
- The optimization algorithm does not guarantee a global optimum.
- Future improvements could include real-world routing APIs, traffic conditions, and additional scheduling constraints.
