#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# 1. Lokacije
locations = pd.DataFrame({
    "Location": [f"L{i}" for i in range(10)],
    "X": [0, 3, 10, 17, 9, 26, -7, 20, 23, -8],
    "Y": [0, 8, 11, 9, -6, 3, 13, -8, 15, -5]
})

# 2. Strojevi
machines = pd.DataFrame({
    "Machine": [f"M{i:02d}" for i in range(1, 11)],
    "Weight": [800, 1300, 1800, 2400, 3100, 3900, 4800, 6100, 7500, 9400]
})

# 3. Kamioni
trucks = pd.DataFrame({
    "Truck": ["Kamion A", "Kamion B"],
    "MaxWeight": [3500, 10000],
    "MaxMachines": [2, 3]
})

# 4. Transportni nalozi
orders = pd.DataFrame({
    "Order": [f"N{i:02d}" for i in range(1, 11)],
    "Machine": [f"M{i:02d}" for i in range(1, 11)],
    "Pickup": ["L1", "L2", "L9", "L3", "L0", "L5", "L8", "L4", "L6", "L7"],
    "Delivery": ["L3", "L5", "L4", "L0", "L8", "L7", "L2", "L9", "L1", "L3"]
})

######################################################################################################

# Ucitavanje aktualnih podataka iz Streamlita
import sys
import json

raw_input = sys.stdin.read().strip()

if raw_input:
    podaci = json.loads(raw_input)

    trucks = pd.DataFrame(podaci["trucks"]).rename(columns={
        "Kamion": "Truck",
        "Nosivost (kg)": "MaxWeight",
        "Maks. strojeva": "MaxMachines"
    })

    machines = pd.DataFrame(podaci["machines"]).rename(columns={
        "Stroj": "Machine",
        "Težina (kg)": "Weight"
    })

    locations = pd.DataFrame(podaci["locations"]).rename(columns={
        "Lokacija": "Location"
    })

    orders = pd.DataFrame(podaci["orders"]).rename(columns={
        "Nalog": "Order",
        "Stroj": "Machine",
        "Preuzimanje": "Pickup",
        "Isporuka": "Delivery"
    })

    # Provjera nedostajucih podataka
    required = {
        "trucks": (trucks, ["Truck", "MaxWeight", "MaxMachines"]),
        "machines": (machines, ["Machine", "Weight"]),
        "locations": (locations, ["Location", "X", "Y"]),
        "orders": (orders, ["Order", "Machine", "Pickup", "Delivery"])
    }

    for naziv, (df, stupci) in required.items():
        if df.empty or df[stupci].isna().any().any():
            raise ValueError(
                f"Tablica '{naziv}' ima prazne ili nepotpune retke."
            )

    # Provjera referenci transportnih naloga
    if not orders["Machine"].isin(machines["Machine"]).all():
        raise ValueError("Nalog koristi stroj koji ne postoji.")

    if not orders["Pickup"].isin(locations["Location"]).all():
        raise ValueError("Lokacija preuzimanja ne postoji.")

    if not orders["Delivery"].isin(locations["Location"]).all():
        raise ValueError("Lokacija isporuke ne postoji.")

    if "L0" not in locations["Location"].values:
        raise ValueError("Nedostaje baza L0.")

    # Provjera nosivosti
    max_capacity = trucks["MaxWeight"].max()

    for _, order in orders.merge(machines, on="Machine").iterrows():
        if order["Weight"] > max_capacity:
            raise ValueError(
                f"Nalog {order['Order']}: stroj {order['Machine']} "
                f"({order['Weight']} kg) prelazi maksimalnu "
                f"nosivost ({max_capacity} kg)."
            )


# Dodajemo težinu stroja svakom nalogu
orders = orders.merge(machines, on="Machine", how="left")


# Provjera izvedivosti pojedinačnih naloga
max_capacity = trucks["MaxWeight"].max()

invalid_orders = orders[
    orders["Weight"] > max_capacity
]

if not invalid_orders.empty:
    for _, order in invalid_orders.iterrows():
        print(
            f"GREŠKA: Nalog {order['Order']} "
            f"({order['Machine']}, {order['Weight']} kg) "
            f"premašuje maksimalnu nosivost "
            f"od {max_capacity} kg."
        )

    raise ValueError("Postoje neizvedivi transportni nalozi.")



# 5. Matrica udaljenosti
coords = locations[["X", "Y"]].to_numpy()
n = len(coords)

distance_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        distance_matrix[i, j] = np.linalg.norm(coords[i] - coords[j])

distance_matrix = np.round(distance_matrix, 1)

distance_df = pd.DataFrame(
    distance_matrix,
    index=locations["Location"],
    columns=locations["Location"]
)

# 6. Prikaz podataka
print("LOKACIJE")
print(locations)

print("\nSTROJEVI")
print(machines)

print("\nKAMIONI")
print(trucks)

print("\nTRANSPORTNI NALOZI")
print(orders)

print("\nMATRICA UDALJENOSTI (km)")
print(distance_df)


# In[24]:


# 7. Logički čvorovi (baza + pickup/delivery događaji)

nodes = [{
    "Node": 0,
    "Order": None,
    "Machine": None,
    "Type": "Depot",
    "Location": "L0",
    "WeightChange": 0,
    "CountChange": 0
}]

for _, order in orders.iterrows():

    # Preuzimanje stroja
    nodes.append({
        "Node": len(nodes),
        "Order": order["Order"],
        "Machine": order["Machine"],
        "Type": "Pickup",
        "Location": order["Pickup"],
        "WeightChange": order["Weight"],
        "CountChange": 1
    })

    # Isporuka stroja
    nodes.append({
        "Node": len(nodes),
        "Order": order["Order"],
        "Machine": order["Machine"],
        "Type": "Delivery",
        "Location": order["Delivery"],
        "WeightChange": -order["Weight"],
        "CountChange": -1
    })

nodes = pd.DataFrame(nodes)

# Dodajemo X i Y koordinate
nodes = nodes.merge(locations, on="Location", how="left")

print("\nLOGIČKI ČVOROVI")
print(nodes)


# In[25]:


# 8. Matrica udaljenosti za 21 čvor

node_locations = nodes["Location"]

node_distance_matrix = distance_df.loc[
    node_locations, node_locations
].to_numpy()

# Pretvorba u cijele brojeve (0.1 km)
distance_int = np.rint(node_distance_matrix * 10).astype(int)

print("\nMATRICA UDALJENOSTI ZA 21 ČVOR")
print(node_distance_matrix)

print("\nDimenzije:", node_distance_matrix.shape)


# In[26]:


from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# 10. OR-Tools model
num_vehicles = len(trucks)
depot = 0

manager = pywrapcp.RoutingIndexManager(
    len(nodes),
    num_vehicles,
    depot
)

routing = pywrapcp.RoutingModel(manager)

# Udaljenosti između čvorova
def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)

    return int(distance_int[from_node][to_node])

distance_callback_index = routing.RegisterTransitCallback(
    distance_callback
)

routing.SetArcCostEvaluatorOfAllVehicles(
    distance_callback_index
)

# Dimenzija udaljenosti
# Dimenzija udaljenosti - potrebna za redoslijed preuzimanja
routing.AddDimension(
    distance_callback_index,
    0,
    1000000,
    True,
    "Distance"
)

# Vrijeme u minutama:
# 60 km/h = 1 km/min
# Udaljenosti su spremljene u desetinkama kilometra
# Svaki utovar i istovar traje 20 minuta

def time_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)

    # 0.1 km = 0.1 minuta pri 60 km/h
    # Koristimo desetinke minute radi preciznosti
    driving_time = int(distance_int[from_node][to_node])

    # Svaki posjeceni cvor naloga predstavlja utovar ili istovar
    handling_time = 0 if from_node == 0 else 200

    return driving_time + handling_time


time_callback_index = routing.RegisterTransitCallback(
    time_callback
)

# 5400 desetinki minute = 9 sati
routing.AddDimension(
    time_callback_index,
    0,
    5400,
    True,
    "Time"
)


# In[27]:


# 11. Ograničenje nosivosti

weight_changes = nodes["WeightChange"].astype(int).tolist()

def weight_callback(from_index):
    node = manager.IndexToNode(from_index)
    return weight_changes[node]

weight_callback_index = routing.RegisterUnaryTransitCallback(
    weight_callback
)

routing.AddDimensionWithVehicleCapacity(
    weight_callback_index,
    0,
    trucks["MaxWeight"].astype(int).tolist(),
    True,
    "Weight"
)


# In[28]:


# 12. Ograničenje broja strojeva

count_changes = nodes["CountChange"].astype(int).tolist()

def count_callback(from_index):
    node = manager.IndexToNode(from_index)
    return count_changes[node]

count_callback_index = routing.RegisterUnaryTransitCallback(
    count_callback
)

routing.AddDimensionWithVehicleCapacity(
    count_callback_index,
    0,
    trucks["MaxMachines"].astype(int).tolist(),
    True,
    "MachineCount"
)


# In[29]:


# 13. Povezivanje preuzimanja i isporuke

solver = routing.solver()

for i in range(len(orders)):
    pickup_node = 2 * i + 1
    delivery_node = 2 * i + 2

    pickup_index = manager.NodeToIndex(pickup_node)
    delivery_index = manager.NodeToIndex(delivery_node)

    routing.AddPickupAndDelivery(pickup_index, delivery_index)

    # Isti kamion mora preuzeti i isporučiti stroj
    solver.Add(
        routing.VehicleVar(pickup_index) ==
        routing.VehicleVar(delivery_index)
    )

    # Preuzimanje mora biti prije isporuke
    solver.Add(
        routing.GetDimensionOrDie("Distance").CumulVar(pickup_index) <=
        routing.GetDimensionOrDie("Distance").CumulVar(delivery_index)
    )


# In[30]:


# 14. Pokretanje optimizacije

search_parameters = pywrapcp.DefaultRoutingSearchParameters()

search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
)

search_parameters.local_search_metaheuristic = (
    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
)

search_parameters.time_limit.seconds = 10

solution = routing.SolveWithParameters(search_parameters)

if solution:
    print("Rješenje pronađeno!")
else:
    print("Nije pronađeno izvedivo rješenje.")


# Rezultati optimizacije za web-aplikaciju
import json

if solution:
    results = {
        "success": True,
        "trucks": [],
        "total_km": 0
    }

    weight_dim = routing.GetDimensionOrDie("Weight")
    count_dim = routing.GetDimensionOrDie("MachineCount")

    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route_km = 0
        completed = 0
        stops = []

        while not routing.IsEnd(index):
            node_id = manager.IndexToNode(index)
            node = nodes.iloc[node_id]

            if node["Type"] != "Depot":
                stops.append({
                    "Lokacija": str(node["Location"]),
                    "Radnja": str(node["Type"]),
                    "Stroj": str(node["Machine"]),
                    "Teret (kg)": int(
                        solution.Value(weight_dim.CumulVar(index))
                        + node["WeightChange"]
                    ),
                    "Broj strojeva": int(
                        solution.Value(count_dim.CumulVar(index))
                        + node["CountChange"]
                    )
                })

                if node["Type"] == "Delivery":
                    completed += 1

            next_index = solution.Value(routing.NextVar(index))
            route_km += routing.GetArcCostForVehicle(
                index, next_index, vehicle_id
            )
            index = next_index

        results["trucks"].append({
            "name": str(trucks.iloc[vehicle_id]["Truck"]),
            "km": round(route_km / 10, 1),
            "orders": completed,
            "route": ["L0"] + [
                stop["Lokacija"] for stop in stops
            ] + ["L0"],
            "stops": stops
        })

        results["total_km"] += route_km / 10

    results["total_km"] = round(results["total_km"], 1)

else:
    results = {
        "success": False,
        "message": "Nije pronađeno izvedivo rješenje."
    }

print("RESULT_JSON:" + json.dumps(results))

