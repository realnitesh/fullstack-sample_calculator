#!/usr/bin/env python3
"""
Simple Calculator App
A command-line calculator that performs basic arithmetic operations.
"""

class Calculator:
    """A simple calculator class that performs basic arithmetic operations."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        """Subtract second number from first number."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        result = a * b
        self.history.append(f"{a} × {b} = {result}")
        return result
    
    def divide(self, a, b):
        """Divide first number by second number."""
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        result = a / b
        self.history.append(f"{a} ÷ {b} = {result}")
        return result
    
    def power(self, a, b):
        """Raise first number to the power of second number."""
        result = a ** b
        self.history.append(f"{a} ^ {b} = {result}")
        return result
    
    def get_history(self):
        """Return calculation history."""
        return self.history
    
    def clear_history(self):
        """Clear calculation history."""
        self.history = []


def get_number_input(prompt):
    """Get a valid number input from user."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def display_menu():
    """Display the calculator menu."""
    print("\n" + "="*50)
    print("           SIMPLE CALCULATOR APP")
    print("="*50)
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (×)")
    print("4. Division (÷)")
    print("5. Power (^)")
    print("6. View History")
    print("7. Clear History")
    print("8. Exit")
    print("="*50)


def main():
    """Main function to run the calculator app."""
    calc = Calculator()
    
    print("Welcome to the Simple Calculator App!")
    print("This calculator can perform basic arithmetic operations.")
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                print("\n--- ADDITION ---")
                a = get_number_input("Enter first number: ")
                b = get_number_input("Enter second number: ")
                result = calc.add(a, b)
                print(f"Result: {a} + {b} = {result}")
                
            elif choice == '2':
                print("\n--- SUBTRACTION ---")
                a = get_number_input("Enter first number: ")
                b = get_number_input("Enter second number: ")
                result = calc.subtract(a, b)
                print(f"Result: {a} - {b} = {result}")
                
            elif choice == '3':
                print("\n--- MULTIPLICATION ---")
                a = get_number_input("Enter first number: ")
                b = get_number_input("Enter second number: ")
                result = calc.multiply(a, b)
                print(f"Result: {a} × {b} = {result}")
                
            elif choice == '4':
                print("\n--- DIVISION ---")
                a = get_number_input("Enter first number: ")
                b = get_number_input("Enter second number: ")
                try:
                    result = calc.divide(a, b)
                    print(f"Result: {a} ÷ {b} = {result}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == '5':
                print("\n--- POWER ---")
                a = get_number_input("Enter base number: ")
                b = get_number_input("Enter exponent: ")
                result = calc.power(a, b)
                print(f"Result: {a} ^ {b} = {result}")
                
            elif choice == '6':
                print("\n--- CALCULATION HISTORY ---")
                history = calc.get_history()
                if history:
                    for i, calculation in enumerate(history, 1):
                        print(f"{i}. {calculation}")
                else:
                    print("No calculations performed yet.")
                    
            elif choice == '7':
                calc.clear_history()
                print("\nHistory cleared!")
                
            elif choice == '8':
                print("\nThank you for using the Simple Calculator App!")
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice! Please enter a number between 1-8.")
                
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        # Ask if user wants to continue
        if choice in ['1', '2', '3', '4', '5']:
            continue_choice = input("\nPress Enter to continue or 'q' to quit: ").strip().lower()
            if continue_choice == 'q':
                print("\nThank you for using the Simple Calculator App!")
                print("Goodbye!")
                break


if __name__ == "__main__":
    main()

