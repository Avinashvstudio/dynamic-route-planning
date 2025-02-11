import traci

def start_simulation():
    try:
        # Start SUMO and connect
        traci.start(["sumo-gui", "-c", "E:/Education/Python/dynamic-route-planning/config/simulation.sumocfg"])
        print("TraCI connected successfully.")

        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            monitor_and_reroute_emergency_vehicles()
            monitor_routes()  # Periodically monitor routes of vehicles

    except Exception as e:
        print(f"Simulation error: {e}")
    finally:
        traci.close()
        print("Simulation ended.")

def monitor_and_reroute_emergency_vehicles():
    vehicles = traci.vehicle.getIDList()
    for vehicle_id in vehicles:
        if "emergency" in vehicle_id:  # Identify emergency vehicles
            current_edge = traci.vehicle.getRoadID(vehicle_id)
            target_edge = "-269696412#0"  # Replace with the desired destination edge

            # Check for congestion
            if is_edge_congested(current_edge):
                print(f"Congestion detected on {current_edge} for {vehicle_id}. Rerouting...")
                reroute_emergency_vehicle(vehicle_id, current_edge, target_edge)
            else:
                print(f"{vehicle_id} is proceeding on {current_edge} without congestion.")


def is_edge_congested(edge):
    """Check if a given edge is congested dynamically."""
    try:
        occupancy = traci.edge.getLastStepOccupancy(edge)
        mean_speed = traci.edge.getLastStepMeanSpeed(edge)
        queue_length = traci.edge.getLastStepHaltingNumber(edge)  # Vehicles waiting
        max_speed = traci.lane.getMaxSpeed(edge + "_0")  # Max speed limit of the edge

        # Dynamic congestion threshold based on road type
        congestion_threshold = 0.7 if max_speed > 15 else 0.5  # Highway vs city roads
        is_congested = (occupancy > congestion_threshold) or (mean_speed < max_speed * 0.2) or (queue_length > 5)

        print(f"Edge {edge}: Occupancy={occupancy}, Speed={mean_speed}, Queue={queue_length}")
        return is_congested
    except Exception as e:
        print(f"Error checking traffic condition for edge {edge}: {e}")
        return False


def reroute_emergency_vehicle(vehicle_id, current_edge, target_edge):
    """Compute a new route using the correct routing mode and update the vehicle's path."""
    try:
        route = traci.simulation.findRoute(current_edge, target_edge, routingMode=1)  # Use integer value
        traci.vehicle.setRoute(vehicle_id, route.edges)
        print(f"New optimized route for {vehicle_id}: {route.edges}")
    except Exception as e:
        print(f"Error rerouting {vehicle_id}: {e}")




def monitor_vehicle_route(vehicle_id, expected_route):
    """Check if the vehicle is following its expected route."""
    current_edge = traci.vehicle.getRoadID(vehicle_id)

    # Check if the vehicle has reached its destination or is progressing through the route
    if current_edge == expected_route[-1]:
        print(f"{vehicle_id} has reached its destination.")
        return True  # Vehicle reached destination
    elif current_edge in expected_route:
        print(f"{vehicle_id} is progressing on its route.")
        return False  # Vehicle is still moving along the route
    else:
        print(f"{vehicle_id} has deviated from the expected route.")
        return False  # Vehicle has deviated from the expected route

def is_vehicle_stuck(vehicle_id):
    """Check if the vehicle is stuck based on its speed or time on a road."""
    current_edge = traci.vehicle.getRoadID(vehicle_id)
    speed = traci.vehicle.getSpeed(vehicle_id)

    if speed < 1:  # Vehicle speed is below 1 m/s, potentially stuck
        print(f"{vehicle_id} is moving very slowly on {current_edge}.")
        return True
    else:
        return False

def monitor_routes():
    """Check vehicle routes periodically during the simulation."""
    vehicles = traci.vehicle.getIDList()
    for vehicle_id in vehicles:
        if "emergency" in vehicle_id:  # Identify emergency vehicles
            current_edge = traci.vehicle.getRoadID(vehicle_id)
            target_edge = "-269696412#0"  # Replace with the desired destination edge

            if is_vehicle_stuck(vehicle_id):
                print(f"{vehicle_id} seems to be stuck on {current_edge}.")
                # Handle stuck vehicle (e.g., try rerouting again or notify)
            elif monitor_vehicle_route(vehicle_id, [current_edge, target_edge]):
                print(f"{vehicle_id} is following the route.")
            else:
                print(f"{vehicle_id} is not following its expected route properly.")


def adjust_traffic_lights_for_emergency(vehicle_id):
    """Turn traffic lights green for emergency vehicles approaching intersections."""
    try:
        junctions = traci.trafficlight.getIDList()
        vehicle_position = traci.vehicle.getPosition(vehicle_id)

        for junction in junctions:
            junction_position = traci.junction.getPosition(junction)
            distance = ((vehicle_position[0] - junction_position[0]) ** 2 + (
                        vehicle_position[1] - junction_position[1]) ** 2) ** 0.5

            if distance < 50:  # If vehicle is within 50 meters of a junction
                traci.trafficlight.setPhase(junction, 0)  # Set green for the emergency route
                print(f"Traffic light at {junction} turned green for {vehicle_id}")

    except Exception as e:
        print(f"Error adjusting traffic lights: {e}")


if __name__ == "__main__":
    start_simulation()
