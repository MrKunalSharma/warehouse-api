from flask import Flask, request, jsonify
import json
from itertools import permutations

app = Flask(__name__)

# [Copy your existing warehouse and distances dictionaries here]
warehouses = {
    'C1': {'A': 3, 'B': 2, 'C': 8},
    'C2': {'D': 12, 'E': 25, 'F': 15},
    'C3': {'G': 0.5, 'H': 1, 'I': 2}
}

distances = {
    ('C1', 'L1'): 3,
    ('C2', 'L1'): 2.5,
    ('C3', 'L1'): 2,
    ('C1', 'C2'): 4,
    ('C2', 'C3'): 3,
    ('C1', 'C3'): 5
}

# [Copy your existing functions here]
def get_distance(start, end):
    # [Your existing function code]
    if (start, end) in distances:
        return distances[(start, end)]
    if (end, start) in distances:
        return distances[(end, start)]
    return float('inf')

# [Copy all other functions]

@app.route('/calculate-cost', methods=['POST'])
def calculate_cost():
    try:
        data = request.get_json()
        result = calculate_delivery_cost(json.dumps(data))
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
