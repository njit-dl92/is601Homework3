# app/plugins/menu/__init__.py

from app.commands import Command
import logging

class GreetCommand(Command):
    def execute(self, args=None):
        logging.info("Hello, World!")
        print('Hello World!')

def register_commands(command_handler):
    command_handler.register_command('greet', GreetCommand())
