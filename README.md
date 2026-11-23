# Vehicle Routing Optimization with Pickup and Delivery Constraints


The application solves a **Capacitated Pickup and Delivery Vehicle Routing Problem (PDVRP)** using Google OR-Tools.

### Hard Constraints

Hard constraints must always be satisfied for a solution to be feasible.

- **Vehicle Weight Capacity:** The total weight of transported machines cannot exceed the truck's maximum payload.
- **Machine Count Capacity:** Each truck has a maximum number of machines it can carry simultaneously.
- **Pickup Before Delivery:** Every machine must be picked up before it can be delivered.
- **Same Vehicle Constraint:** Pickup and delivery of the same machine must be performed by the same truck.
- **Depot Constraint:** Every truck must start and finish its route at the depot (L0).
- **Working Time Limit:** Driving, loading, and unloading must fit within 9 hours per truck.
- **Order Completion:** Every transport order must be completed, otherwise the solution is reported as infeasible.

### Soft Constraints / Optimization Objective

The primary optimization objective is to **minimize the total distance traveled by all trucks**.

- **Distance Minimization:** Reduce the combined mileage of all vehicles.
- **Efficient Route Sequencing:** Find efficient pickup and delivery sequences.
- **Vehicle Utilization:** Allow the solver to choose which trucks to use based on overall route efficiency.

### Optimization Algorithm

- **Solver:** Google OR-Tools Routing Solver
- **Initial Solution:** Parallel Cheapest Insertion
- **Improvement Heuristic:** Guided Local Search (GLS)
- **Distance Metric:** Euclidean distance, rounded to one decimal place
- **Travel Speed:** 60 km/h
- **Handling Time:** 20 minutes per pickup or delivery

The solver searches for high-quality feasible solutions within a configured time limit. Global optimality is not guaranteed.

### Configurable Inputs

The application allows users to dynamically modify the following inputs:

- **Vehicles:** Number of available trucks, vehicle names, maximum weight capacity (kg), and maximum number of machines carried simultaneously.
- **Machines:** Machine identifiers and individual weights (kg).
- **Locations:** Location identifiers and X/Y coordinates (km).
- **Transport Orders:** Number of orders, machine assignments, pickup locations, and delivery locations.

Users can add, edit, or remove entries directly through the Streamlit interface without modifying the source code.

The optimization model automatically adapts to the updated inputs and recalculates the routes.
