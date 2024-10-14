# app/plugins/divide/__init__.py
from decimal import Decimal, InvalidOperation
from app.commands import Command
import logging

class DivideCommand(Command):
    def execute(self, args):
        if len(args) < 2:
            logging.info("Error: The 'divide' command requires two decimal numbers.")
            return

        try:
            a = Decimal(args[0])
            b = Decimal(args[1])
            if b == 0:
                logging.info("Error: Division by zero is not allowed.")
                return
            logging.info(f"The quotient is: {a / b}")
        except (ValueError, InvalidOperation) as e:
            logging.info(f"Error: Invalid input - {e}")

def register_commands(command_handler):
    command_handler.register_command('divide', DivideCommand())
