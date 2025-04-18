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

def validate_input(data):
    """Validate input data and return error messages if any"""
    errors = []
    
    # Check if source exists
    if 'source' not in data:
        errors.append("Source warehouse is required")
    elif data['source'] not in warehouses:
        errors.append(f"Invalid source warehouse: {data['source']}. Valid warehouses are: C1, C2, C3")
    
    # Check if weight is valid
    if 'weight' not in data:
        errors.append("Weight is required")
    elif not isinstance(data['weight'], (int, float)):
        errors.append("Weight must be a number")
    elif data['weight'] <= 0:
        errors.append("Weight must be greater than 0")
    
    # Check if destination is valid
    valid_destinations = ['L1', 'C1', 'C2', 'C3']
    if 'destination' in data and data['destination'] not in valid_destinations:
        errors.append(f"Invalid destination: {data['destination']}. Valid destinations are: {', '.join(valid_destinations)}")
    
    return errors

def get_distance(start, end):
    """Get distance between two points"""
    if (start, end) in distances:
        return distances[(start, end)]
    if (end, start) in distances:
        return distances[(end, start)]
    return None  # Changed from float('inf') to None

def calculate_delivery_cost(data):
    """Calculate the minimum delivery cost based on weight and route"""
    data = json.loads(data) if isinstance(data, str) else data
    
    # Validate input
    errors = validate_input(data)
    if errors:
        raise ValueError({"errors": errors})
    
    source = data['source']
    destination = data.get('destination', 'L1')
    weight = data['weight']
    
    # Get distance
    distance = get_distance(source, destination)
    if distance is None:
        raise ValueError({"errors": [f"No valid route found between {source} and {destination}"]})
    
    # Calculate costs
    base_cost = weight * 10
    distance_cost = distance * weight * 0.5
    total_cost = base_cost + distance_cost
    
    return {
        'total_cost': round(total_cost, 2),
        'base_cost': round(base_cost, 2),
        'distance_cost': round(distance_cost, 2),
        'route': f'{source} -> {destination}',
        'distance': distance
    }

@app.route('/calculate-cost', methods=['POST'])
def calculate_cost():
    try:
        if not request.is_json:
            return jsonify({
                'error': 'Request must be JSON',
                'example_format': {
                    'source': 'C1',
                    'destination': 'L1',
                    'weight': 100
                }
            }), 400
        
        data = request.get_json()
        result = calculate_delivery_cost(data)
        return jsonify({'result': result})
    
    except ValueError as e:
        # Handle validation errors
        error_dict = e.args[0] if isinstance(e.args[0], dict) else {'errors': [str(e)]}
        return jsonify(error_dict), 400
    except Exception as e:
        # Handle unexpected errors
        return jsonify({
            'error': 'An unexpected error occurred',
            'message': str(e)
        }), 500

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
