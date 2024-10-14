# app/plugins/subtract/__init__.py
from decimal import Decimal, InvalidOperation
from app.commands import Command
import logging

class SubtractCommand(Command):
    def execute(self, args):
        if len(args) < 2:
            logging.info("Error: The 'subtract' command requires two decimal numbers.")
            return

        try:
            a = Decimal(args[0])
            b = Decimal(args[1])
            logging.info(f"The difference is: {a - b}")
        except (ValueError, InvalidOperation) as e:
            logging.info(f"Error: Invalid input - {e}")

def register_commands(command_handler):
    command_handler.register_command('subtract', SubtractCommand())
