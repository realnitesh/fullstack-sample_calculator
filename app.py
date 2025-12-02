#!/usr/bin/env python3
"""
Flask API Backend for Simple Calculator
Provides REST API endpoints for calculator operations.
"""

from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Import our calculator class
from calculator import Calculator

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Enable CORS for all routes
CORS(app)

# Initialize calculator instance
calc = Calculator()

@app.route('/')
def serve_frontend():
    """Serve the calculator frontend."""
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/styles.css')
def serve_styles():
    """Serve the frontend stylesheet."""
    return send_from_directory(BASE_DIR, 'styles.css')

@app.route('/script.js')
def serve_script():
    """Serve the frontend JavaScript bundle."""
    return send_from_directory(BASE_DIR, 'script.js')

@app.route('/api')
def api_documentation():
    """API home endpoint with available endpoints."""
    return jsonify({
        'message': 'Simple Calculator API',
        'version': '1.0.0',
        'endpoints': {
            'POST /calculate': 'Perform calculations',
            'GET /history': 'Get calculation history',
            'POST /clear_history': 'Clear calculation history',
            'GET /health': 'Health check'
        },
        'usage': 'Send POST requests to /calculate with operation, operand1, operand2'
    })

@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    """API endpoint for calculator operations."""
    try:
        # Support both JSON POST body and query params (for direct browser testing)
        if request.method == 'POST':
            data = request.get_json() or {}
            operation = data.get('operation')
            operand1 = float(data.get('operand1', 0))
            operand2 = float(data.get('operand2', 0))
        else:  # GET
            operation = request.args.get('operation')
            operand1 = float(request.args.get('operand1', 0))
            operand2 = float(request.args.get('operand2', 0))
        
        result = None
        error = None
        
        # Perform calculation based on operation
        if operation == 'add':
            result = calc.add(operand1, operand2)
        elif operation == 'subtract':
            result = calc.subtract(operand1, operand2)
        elif operation == 'multiply':
            result = calc.multiply(operand1, operand2)
        elif operation == 'divide':
            if operand2 == 0:
                error = "Cannot divide by zero!"
            else:
                result = calc.divide(operand1, operand2)
        elif operation == 'power':
            result = calc.power(operand1, operand2)
        else:
            error = "Invalid operation"
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'result': result,
            'history': calc.get_history()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Get calculation history."""
    try:
        return jsonify({'history': calc.get_history()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear calculation history."""
    try:
        calc.clear_history()
        return jsonify({'message': 'History cleared successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Calculator API is running'})

if __name__ == '__main__':
    print("Starting Simple Calculator API Backend...")
    print("API Base URL: http://localhost:5000")
    print("Available endpoints:")
    print("  GET  /           - API documentation")
    print("  POST /calculate   - Perform calculations")
    print("  GET  /history     - Get calculation history")
    print("  POST /clear_history - Clear history")
    print("  GET  /health      - Health check")
    print("\nExample usage:")
    print("  curl -X POST http://localhost:5000/calculate \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"operation\": \"add\", \"operand1\": 5, \"operand2\": 3}'")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
