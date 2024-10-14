# app/commands/command_handler.py
from abc import ABC, abstractmethod
import logging

class Command(ABC):
    @abstractmethod
    def execute(self, args=None):
        """Execute the command with optional arguments."""
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        """Register a command with its name and class."""
        self.commands[command_name] = command
        logging.info(f"Command '{command_name}' registered.")

    def is_valid_command(self, command_name: str) -> bool:
        """Check if the command is valid."""
        return command_name in self.commands

    def execute_command(self, command_name: str, args=None):
        """Execute the specified command with given arguments."""
        if command_name not in self.commands:
            logging.warning(f"No such command: {command_name}")
            print(f"No such command: {command_name}")  # Provide feedback to the user
            return
        
        try:
            logging.info(f"Executing command '{command_name}' with arguments: {args}")
            self.commands[command_name].execute(args)
            logging.info(f"Command '{command_name}' executed successfully.")
        except Exception as e:
            logging.error(f"Error executing command '{command_name}': {e}")
            print(f"Error executing command '{command_name}': {e}")  # Provide feedback to the user
