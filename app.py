#!/usr/bin/env python3
"""
Flask API Backend for Simple Calculator
Provides REST API endpoints for calculator operations.
"""

from pathlib import Path
import os

import psycopg2
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Import our calculator class
from calculator import Calculator

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Enable CORS for all routes
CORS(app)

# Initialize calculator instance (still used for core math/CLI)
calc = Calculator()


def get_db_connection():
    """Create a new database connection using environment variables."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "calculator_db"),
        user=os.getenv("DB_USER", "calculator_user"),
        password=os.getenv("DB_PASSWORD", "calculator_pass"),
    )


def init_db():
    """Ensure the calculations table exists."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS calculations (
                id SERIAL PRIMARY KEY,
                expression TEXT NOT NULL,
                result DOUBLE PRECISION,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            """
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as exc:
        # Log to stdout; app can still run but history endpoints will fail
        print(f"[WARN] Failed to initialize database: {exc}")

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

def _operation_symbol(operation: str) -> str:
    """Map backend operation name to human-readable symbol."""
    return {
        "add": "+",
        "subtract": "-",
        "multiply": "×",
        "divide": "÷",
        "power": "^",
    }.get(operation, "?")


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

        # Perform calculation based on operation (reuse Calculator for math only)
        if operation == 'add':
            result = operand1 + operand2
        elif operation == 'subtract':
            result = operand1 - operand2
        elif operation == 'multiply':
            result = operand1 * operand2
        elif operation == 'divide':
            if operand2 == 0:
                return jsonify({'error': "Cannot divide by zero!"}), 400
            result = operand1 / operand2
        elif operation == 'power':
            result = operand1 ** operand2
        else:
            return jsonify({'error': "Invalid operation"}), 400

        # Build history expression string and persist to DB
        expression = f"{operand1} {_operation_symbol(operation)} {operand2} = {result}"

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO calculations (expression, result) VALUES (%s, %s);",
                (expression, result),
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as db_exc:
            # Don't fail the calculation if history persistence fails
            print(f"[WARN] Failed to save calculation to DB: {db_exc}")

        # Fetch latest history from DB
        history = []
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT expression FROM calculations ORDER BY id DESC LIMIT 10;"
            )
            rows = cur.fetchall()
            history = [row[0] for row in rows]
            cur.close()
            conn.close()
        except Exception as db_exc:
            print(f"[WARN] Failed to load history from DB: {db_exc}")

        return jsonify({
            'result': result,
            'history': history
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Get calculation history."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT expression FROM calculations ORDER BY id DESC LIMIT 50;"
        )
        rows = cur.fetchall()
        history = [row[0] for row in rows]
        cur.close()
        conn.close()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear calculation history."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM calculations;")
        conn.commit()
        cur.close()
        conn.close()
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
