from flask import Flask, request, jsonify
import json
from itertools import permutations

app = Flask(__name__)

# Warehouse locations and their internal distances
warehouses = {
    'C1': {'A': 3, 'B': 2, 'C': 8},
    'C2': {'D': 12, 'E': 25, 'F': 15},
    'C3': {'G': 0.5, 'H': 1, 'I': 2}
}

# Distances between warehouses and delivery location
distances = {
    ('C1', 'L1'): 3,
    ('C2', 'L1'): 2.5,
    ('C3', 'L1'): 2,
    ('C1', 'C2'): 4,
    ('C2', 'C3'): 3,
    ('C1', 'C3'): 5
}

def get_distance(start, end):
    """Get distance between two points"""
    if (start, end) in distances:
        return distances[(start, end)]
    if (end, start) in distances:
        return distances[(end, start)]
    return float('inf')

def calculate_delivery_cost(data):
    """
    Calculate the minimum delivery cost based on weight and route
    """
    data = json.loads(data)
    
    # Get source warehouse and destination
    source = data.get('source', '')  # e.g., 'C1'
    destination = data.get('destination', 'L1')  # Default destination is L1
    weight = data.get('weight', 0)
    
    if not source or weight <= 0:
        raise ValueError("Invalid input: source and weight are required")
    
    # Calculate base cost based on weight
    base_cost = weight * 10  # Basic rate per unit weight
    
    # Find the shortest path and its distance
    distance = get_distance(source, destination)
    
    # Calculate total cost
    total_cost = base_cost + (distance * weight * 0.5)  # Distance factor
    
    return {
        'total_cost': round(total_cost, 2),
        'base_cost': round(base_cost, 2),
        'distance_cost': round(distance * weight * 0.5, 2),
        'route': f'{source} -> {destination}',
        'distance': distance
    }

@app.route('/calculate-cost', methods=['POST'])
def calculate_cost():
    try:
        data = request.get_json()
        result = calculate_delivery_cost(json.dumps(data))
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Welcome to Warehouse Delivery Cost Calculator API',
        'usage': {
            'endpoint': '/calculate-cost',
            'method': 'POST',
            'body_format': {
                'source': 'Warehouse ID (C1, C2, or C3)',
                'destination': 'Delivery location (default: L1)',
                'weight': 'Weight of the package in units'
            },
            'example': {
                'source': 'C1',
                'destination': 'L1',
                'weight': 100
            }
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
