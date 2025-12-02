// Calculator Frontend - Connected to Python Backend API
class Calculator {
    constructor() {
        this.previousOperand = '';
        this.currentOperand = '';
        this.operation = undefined;
        this.history = [];
        const defaultApiUrl = 'http://localhost:5000';
        const isHttpProtocol = window.location.protocol.startsWith('http');
        this.apiBaseUrl = isHttpProtocol ? window.location.origin : defaultApiUrl;
        this.isConnected = false;
        
        // Initialize connection check
        this.checkConnection();
    }

    // Check connection to Python backend
    async checkConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            if (response.ok) {
                this.isConnected = true;
                this.updateConnectionStatus('connected', 'Connected to Python API');
                await this.loadHistory();
            } else {
                this.isConnected = false;
                this.updateConnectionStatus('disconnected', 'API not responding');
            }
        } catch (error) {
            this.isConnected = false;
            this.updateConnectionStatus('disconnected', 'Cannot connect to API');
            console.error('Connection error:', error);
        }
    }

    // Update connection status display
    updateConnectionStatus(status, message) {
        const statusElement = document.getElementById('connection-status');
        statusElement.className = `connection-status ${status}`;
        statusElement.querySelector('span').textContent = message;
    }

    // Clear the calculator
    clear() {
        this.currentOperand = '';
        this.previousOperand = '';
        this.operation = undefined;
        this.updateDisplay();
    }

    // Delete the last character
    delete() {
        this.currentOperand = this.currentOperand.toString().slice(0, -1);
        this.updateDisplay();
    }

    // Append a number to the current operand
    appendNumber(number) {
        if (number === '.' && this.currentOperand.includes('.')) return;
        this.currentOperand = this.currentOperand.toString() + number.toString();
        this.updateDisplay();
    }

    // Choose an operation
    chooseOperation(operation) {
        if (this.currentOperand === '') return;
        if (this.previousOperand !== '') {
            this.compute();
        }
        this.operation = operation;
        this.previousOperand = this.currentOperand;
        this.currentOperand = '';
        this.updateDisplay();
    }

    // Compute the result using Python backend API
    async compute() {
        if (!this.isConnected) {
            this.showError('Not connected to Python API. Please start the backend server.');
            return;
        }

        const prev = parseFloat(this.previousOperand);
        const current = parseFloat(this.currentOperand);
        
        if (isNaN(prev) || isNaN(current)) return;
        
        // Map frontend operations to backend operations
        const operationMap = {
            '+': 'add',
            '-': 'subtract',
            '×': 'multiply',
            '÷': 'divide',
            '^': 'power'
        };
        
        const backendOperation = operationMap[this.operation];
        if (!backendOperation) return;
        
        try {
            // Show loading state
            this.showLoading(true);
            
            // Make API call to Python backend
            const response = await fetch(`${this.apiBaseUrl}/calculate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    operation: backendOperation,
                    operand1: prev,
                    operand2: current
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Update display with result from Python backend
                this.currentOperand = data.result;
                this.operation = undefined;
                this.previousOperand = '';
                
                // Update history from Python backend
                this.history = data.history || [];
                this.updateHistory();
                
                this.updateDisplay();
            } else {
                // Handle error from Python backend
                this.showError(data.error || 'Calculation failed');
            }
        } catch (error) {
            console.error('API Error:', error);
            this.showError('Connection error. Please check if the Python server is running.');
            this.isConnected = false;
            this.updateConnectionStatus('disconnected', 'Connection lost');
        } finally {
            this.showLoading(false);
        }
    }

    // Get operation symbol for display
    getOperationSymbol(operation) {
        switch (operation) {
            case '+': return '+';
            case '-': return '-';
            case '×': return '×';
            case '÷': return '÷';
            case '^': return '^';
            default: return '';
        }
    }

    // Format number for display
    getDisplayNumber(number) {
        const stringNumber = number.toString();
        const integerDigits = parseFloat(stringNumber.split('.')[0]);
        const decimalDigits = stringNumber.split('.')[1];
        let integerDisplay;
        
        if (isNaN(integerDigits)) {
            integerDisplay = '';
        } else {
            integerDisplay = integerDigits.toLocaleString('en', { maximumFractionDigits: 0 });
        }
        
        if (decimalDigits != null) {
            return `${integerDisplay}.${decimalDigits}`;
        } else {
            return integerDisplay;
        }
    }

    // Update the display
    updateDisplay() {
        const currentOperandElement = document.getElementById('current-operand');
        const previousOperandElement = document.getElementById('previous-operand');
        
        currentOperandElement.textContent = this.getDisplayNumber(this.currentOperand) || '0';
        
        if (this.operation != null) {
            previousOperandElement.textContent = 
                `${this.getDisplayNumber(this.previousOperand)} ${this.getOperationSymbol(this.operation)}`;
        } else {
            previousOperandElement.textContent = '';
        }
    }

    // Update the history display
    updateHistory() {
        const historyList = document.getElementById('history-list');
        
        if (this.history.length === 0) {
            historyList.innerHTML = '<p class="no-history">No calculations yet</p>';
            return;
        }
        
        historyList.innerHTML = this.history
            .slice(0, 10) // Show only last 10 calculations
            .map(entry => `<div class="history-item">${entry}</div>`)
            .join('');
    }

    // Clear history using Python backend API
    async clearHistory() {
        if (!this.isConnected) {
            this.showError('Not connected to Python API. Please start the backend server.');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/clear_history`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                this.history = [];
                this.updateHistory();
            } else {
                const data = await response.json();
                this.showError(data.error || 'Failed to clear history');
            }
        } catch (error) {
            console.error('Clear History Error:', error);
            this.showError('Connection error. Please check if the Python server is running.');
        }
    }

    // Load history from Python backend
    async loadHistory() {
        if (!this.isConnected) return;

        try {
            const response = await fetch(`${this.apiBaseUrl}/history`);
            const data = await response.json();
            
            if (response.ok) {
                this.history = data.history || [];
                this.updateHistory();
            }
        } catch (error) {
            console.error('Load History Error:', error);
            // Don't show error for history loading, just use empty history
        }
    }

    // Show loading state
    showLoading(show) {
        const currentOperandElement = document.getElementById('current-operand');
        if (show) {
            currentOperandElement.classList.add('loading');
            currentOperandElement.textContent = 'Calculating...';
        } else {
            currentOperandElement.classList.remove('loading');
        }
    }

    // Show error message
    showError(message) {
        const currentOperandElement = document.getElementById('current-operand');
        const originalText = currentOperandElement.textContent;
        
        currentOperandElement.textContent = message;
        currentOperandElement.style.color = '#e53e3e';
        
        setTimeout(() => {
            currentOperandElement.textContent = originalText;
            currentOperandElement.style.color = '#ffffff';
        }, 3000);
    }
}

// Initialize calculator
const calculator = new Calculator();

// Keyboard support
document.addEventListener('keydown', (e) => {
    if (e.key >= '0' && e.key <= '9' || e.key === '.') {
        calculator.appendNumber(e.key);
    }
    if (e.key === '+' || e.key === '-') {
        calculator.chooseOperation(e.key);
    }
    if (e.key === '*') {
        calculator.chooseOperation('×');
    }
    if (e.key === '/') {
        e.preventDefault();
        calculator.chooseOperation('÷');
    }
    if (e.key === '^') {
        calculator.chooseOperation('^');
    }
    if (e.key === 'Enter' || e.key === '=') {
        calculator.compute();
    }
    if (e.key === 'Escape') {
        calculator.clear();
    }
    if (e.key === 'Backspace') {
        calculator.delete();
    }
});

// Add click animations and ripple effects
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
        // Click animation
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
        }, 150);

        // Ripple effect
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Periodic connection check
setInterval(() => {
    calculator.checkConnection();
}, 10000); // Check every 10 seconds

// Initialize display
calculator.updateDisplay();




