# UP RENT – Smart Logistics Planner

**Capacitated Pickup and Delivery Vehicle Routing Problem (PDVRP)**

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

## 3. Optimization Model

The problem is modeled as a **Capacitated Pickup and Delivery Vehicle Routing Problem (PDVRP)** using Google OR-Tools.

### Hard Constraints

Every feasible solution must satisfy:

- **Weight Capacity:** A truck cannot exceed its maximum carrying capacity at any point along its route.
- **Machine Count:** A truck cannot carry more than its permitted number of machines simultaneously.
- **Pickup Before Delivery:** Each machine must be collected before being delivered.
- **Same Vehicle:** The same truck must perform both pickup and delivery of an assigned machine.
- **Depot Return:** Every truck starts and finishes at the depot (L0).
- **Working Time:** Driving, loading, and unloading must fit within 9 hours per truck.
- **Order Completion:** All transport orders must be fulfilled.

If the constraints cannot be satisfied, the application reports that no feasible solution was found.

### Optimization Objective

**Minimize the combined distance traveled by all trucks.**

The solver can distribute orders across vehicles and change their visiting sequence to reduce unnecessary travel.

### Optimization Algorithm

- **Solver:** Google OR-Tools Routing Solver
- **Initial Solution:** Parallel Cheapest Insertion
- **Local Search:** Guided Local Search (GLS)
- **Distance:** Euclidean distance, rounded to 0.1 km per segment
- **Average Speed:** 60 km/h
- **Loading / Unloading:** 20 minutes per operation
- **Working Time Limit:** 540 minutes per truck

The solver searches for high-quality feasible solutions within a predefined time limit. It does not guarantee a globally optimal solution.



# pip install streamlit ortools pandas matplotlib networkx












## 6. Running the Application

### Requirements

- Python 3.11 or compatible version
- Streamlit
- Google OR-Tools
- Pandas
- Matplotlib

### Installation

```bash
pip install streamlit ortools pandas matplotlib
```

### Start the Application

```bash
streamlit run app.py
```
# pip install streamlit ortools pandas matplotlib networkx

Then open the URL displayed by Streamlit.

### Usage

1. Load the example dataset.
2. Review or modify the input tables.
3. Click **Optimize Routes**.
4. Inspect the optimized truck assignments, distances, and working times.
5. Review the route visualization and pickup/delivery actions.


## 9. Limitations and Future Improvements

- Euclidean distances are used instead of real road networks.
- Travel speed and handling times are assumed constant.
- The optimization algorithm does not guarantee a global optimum.
- Future improvements could include real-world routing APIs, traffic conditions, and additional scheduling constraints.
