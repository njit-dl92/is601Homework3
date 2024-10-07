# app/commands/command_handler.py
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, args=None):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command

    def execute_command(self, command_name: str, args=None):
        try:
            self.commands[command_name].execute(args)
        except KeyError:
            print(f"No such command: {command_name}")
