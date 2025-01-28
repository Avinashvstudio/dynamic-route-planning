# Dynamic Route Planning with SUMO

This project demonstrates a **Dynamic Route Planning** simulation using **SUMO (Simulation of Urban Mobility)** and the Python API **TraCI**. The system monitors and dynamically reroutes emergency vehicles based on traffic conditions to ensure optimal navigation.

---

## Features

1. **Dynamic Traffic Monitoring**
   - Periodically monitors traffic conditions (e.g., occupancy, speed) on roads.
   
2. **Emergency Vehicle Rerouting**
   - Detects and reroutes emergency vehicles to avoid congestion and reduce response times.
   
3. **Stuck Vehicle Detection**
   - Identifies stuck vehicles and handles rerouting or notifications.
   
4. **Route Monitoring**
   - Tracks the progress of vehicles to ensure they follow expected routes.

---

## Requirements

1. **SUMO**
   - Download and install SUMO: [SUMO Website](https://www.eclipse.org/sumo/)

2. **Python Libraries**
   - `traci`

   Install TraCI using:
   ```bash
   pip install sumolib traci
   ```

3. **Configuration Files**
   - `simulation.sumocfg`: Defines the simulation setup for SUMO.
   - Ensure the paths and settings in the `.sumocfg` file are correctly configured.

---

## File Structure

```
.
├── config/
│   └── simulation.sumocfg
├── start_simulation.py
└── README.md
```

- **`simulation.sumocfg`**: Configuration file for the SUMO simulation.
- **`start_simulation.py`**: Python script to manage the simulation.

---

## How to Run

1. **Launch the Simulation**
   Run the Python script:
   ```bash
   python start_simulation.py
   ```

2. **Select Source and Destination**
   - In the terminal, select the source (A) and destination (B) for the vehicle.
   - SUMO GUI will launch for visualization.

3. **Dynamic Routing**
   - The system will automatically monitor traffic conditions and reroute emergency vehicles as needed.

---

## Key Functions

### **1. Start Simulation**
```python
start_simulation()
```
- Connects to SUMO and begins the simulation loop.

### **2. Monitor and Reroute Emergency Vehicles**
```python
monitor_and_reroute_emergency_vehicles()
```
- Detects emergency vehicles and evaluates their current route.
- Reroutes vehicles if congestion is detected.

### **3. Traffic Monitoring**
```python
is_edge_congested(edge)
```
- Checks occupancy and speed on edges to detect congestion.

### **4. Vehicle Monitoring**
```python
monitor_vehicle_route(vehicle_id, expected_route)
```
- Tracks vehicle progress and checks for route deviations.

---

## Example Output

1. **Launching Simulation**
   - SUMO GUI will open.

2. **In Terminal**
   - Outputs traffic monitoring details, such as:
     ```
     TraCI connected successfully.
     Edge edge_1: Occupancy=0.85, Speed=3.2
     Congestion detected on edge_1 for emergency_vehicle_1. Rerouting...
     New route for emergency_vehicle_1: ['edge_2', 'edge_3']
     ```

---

## Future Improvements

- Add real-time user input for dynamic rerouting.
- Enhance stuck vehicle handling by integrating notifications or automated interventions.
- Optimize rerouting logic using machine learning or advanced algorithms.

---

## License

This project is licensed under the MIT License.

