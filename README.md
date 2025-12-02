## Simple Calculator App (Frontend + Backend)

This project is a **full-stack calculator** consisting of:

- **Python Flask backend** exposing REST APIs for all calculator operations.  
- **Modern web frontend** (`index.html`, `styles.css`, `script.js`) that talks to the backend over HTTP.

You can open a browser, visit `http://localhost:5000`, and use the calculator UI while all calculations are processed on the server.

---

## Features

- **Frontend**
  - **Responsive calculator UI** built with HTML, CSS, and vanilla JavaScript.
  - **Keyboard support** for numbers, operators, Enter, Escape, and Backspace.
  - **Animated buttons** with ripple effects and a live **connection status** indicator.
  - **History panel** that shows the last few calculations returned by the API.

- **Backend**
  - **REST API** endpoints for calculator operations (`/calculate`, `/history`, `/clear_history`, `/health`).
  - **Basic operations**: Addition, Subtraction, Multiplication, Division, and Power.
  - **Server-side history** using the `Calculator` class in `calculator.py`.
  - **CORS support** so the frontend can talk to the backend safely.
  - **JSON-based requests and responses** with clear error messages.

---

## Requirements

- **Python 3.6+**
- **pip** (Python package manager)
- A modern web browser (Chrome, Edge, Firefox, etc.)

Python packages (installed via `requirements.txt`):

- `Flask`
- `Flask-Cors`

---

## Installation & Setup

1. **Clone or download** this repository.
2. **Create and activate a virtual environment** (optional but recommended).
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the App

1. **Start the Flask backend**:

   ```bash
   python app.py
   ```

   By default the server runs on `http://localhost:5000`.

2. **Open the frontend in a browser**:

   - Visit: `http://localhost:5000/`
   - You should see the **Python Calculator** UI.
   - The connection indicator in the header should show **“Connected to Python API”** once the backend is reachable.

> Note: If you open `index.html` directly from the filesystem (e.g., `file:///.../index.html`), the frontend will fall back to calling `http://localhost:5000` as the API base URL. In that case you still must have `python app.py` running.

---

## API Endpoints (Backend)

All endpoints are served from `http://localhost:5000`.

### 1. **GET /** – Frontend UI

Serves the calculator web interface (`index.html`).

### 2. **GET /api** – API Documentation (JSON)

Returns JSON information about available API endpoints.

Example:

```json
{
  "message": "Simple Calculator API",
  "version": "1.0.0",
  "endpoints": {
    "POST /calculate": "Perform calculations",
    "GET /history": "Get calculation history",
    "POST /clear_history": "Clear calculation history",
    "GET /health": "Health check"
  }
}
```

### 3. **POST /calculate** – Perform Calculations (JSON)

Performs an arithmetic operation using JSON input.

- **Request body**:

  ```json
  {
    "operation": "add",
    "operand1": 10,
    "operand2": 5
  }
  ```

- **Supported operations**:
  - `add`
  - `subtract`
  - `multiply`
  - `divide`
  - `power`

- **Response**:

  ```json
  {
    "result": 15.0,
    "history": ["10.0 + 5.0 = 15.0"]
  }
  ```

### 4. **GET /calculate** – Quick Browser Testing (Query Params)

Same calculation logic, but accepts **query parameters** so you can test directly in the address bar.

- **Example URL**:

  - `http://localhost:5000/calculate?operation=add&operand1=10&operand2=5`

- **Response** (same format as POST):

  ```json
  {
    "result": 15.0,
    "history": ["10.0 + 5.0 = 15.0"]
  }
  ```

### 5. **GET /history** – Get Calculation History

Returns the server-side history of all calculations.

```json
{
  "history": [
    "10.0 + 5.0 = 15.0",
    "8.0 × 3.0 = 24.0",
    "15.0 ÷ 3.0 = 5.0"
  ]
}
```

### 6. **POST /clear_history** – Clear History

Clears all saved calculations.

```json
{
  "message": "History cleared successfully"
}
```

### 7. **GET /health** – Health Check

Simple status check used by the frontend’s connection indicator.

```json
{
  "status": "healthy",
  "message": "Calculator API is running"
}
```

---

## Example Usage (CLI)

### Using `curl`

```bash
# Perform addition
curl -X POST http://localhost:5000/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "operand1": 10, "operand2": 5}'

# Perform division
curl -X POST http://localhost:5000/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "divide", "operand1": 15, "operand2": 3}'

# Get history
curl http://localhost:5000/history

# Clear history
curl -X POST http://localhost:5000/clear_history
```

### Using Python `requests`

```python
import requests

base_url = "http://localhost:5000"

response = requests.post(f"{base_url}/calculate", json={
    "operation": "add",
    "operand1": 10,
    "operand2": 5
})
print("Result:", response.json()["result"])

history = requests.get(f"{base_url}/history").json()
print("History:", history["history"])
```

---

## Project Structure

```text
simple-calculator-app/
├── app.py             # Flask API server + static file serving for frontend
├── calculator.py      # Calculator class and CLI implementation
├── index.html         # Frontend HTML UI
├── styles.css         # Frontend styling
├── script.js          # Frontend logic and API calls
├── test_connection.py # API testing script
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation (this file)
```

---

## Testing the Backend

Run the test script to verify core API functionality:

```bash
python test_connection.py
```

---

## Contributing

Feel free to fork this project and submit pull requests for improvements!

---

## License

This project is open source and available under the **MIT License**.
