# app/plugins/multiply/__init__.py
from decimal import Decimal, InvalidOperation
from app.commands import Command

class MultiplyCommand(Command):
    def execute(self, args):
        if len(args) < 2:
            print("Error: The 'multiply' command requires two decimal numbers.")
            return

        try:
            a = Decimal(args[0])
            b = Decimal(args[1])
            print(f"The product is: {a * b}")
        except (ValueError, InvalidOperation) as e:
            print(f"Error: Invalid input - {e}")

def register_commands(command_handler):
    command_handler.register_command('multiply', MultiplyCommand())
