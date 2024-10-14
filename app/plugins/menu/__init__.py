# app/plugins/menu/__init__.py

from app.commands import Command
import logging

class MenuCommand(Command):
    def execute(self, args=None):
        logging.info('Menu')

def register_commands(command_handler):
    command_handler.register_command('menu', MenuCommand())
