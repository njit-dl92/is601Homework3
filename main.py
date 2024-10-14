import sys
from calculator import Calculator
from decimal import Decimal, InvalidOperation
from app import App
import logging

def calculate_and_print(a, b, operation_name):
    operation_mappings = {
        'add': Calculator.add,
        'subtract': Calculator.subtract,
        'multiply': Calculator.multiply,
        'divide': Calculator.divide
    }

    # Unified error handling for decimal conversion
    try:
        a_decimal, b_decimal = map(Decimal, [a, b])
        result = operation_mappings.get(operation_name) # Use get to handle unknown operations
        if result:
            logging.info(f"The result of {a} {operation_name} {b} is equal to {result(a_decimal, b_decimal)}")
        else:
            logging.info(f"Unknown operation: {operation_name}")
    except InvalidOperation:
        logging.info(f"Invalid number input: {a} or {b} is not a valid number.")
    except ZeroDivisionError:
        logging.info("Error: Division by zero.")
    except Exception as e: # Catch-all for unexpected errors
        logging.info(f"An error occurred: {e}")

def main():
    if len(sys.argv) != 4:
        logging.info("Usage: python calculator_main.py <number1> <number2> <operation>")
        sys.exit(1)
    
    _, a, b, operation = sys.argv
    calculate_and_print(a, b, operation)

if __name__ == '__main__':
    #main()
    app = App().start()

