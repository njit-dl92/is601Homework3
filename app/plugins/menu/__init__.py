# app/plugins/menu/__init__.py

from app.commands import Command

class MenuCommand(Command):
    def execute(self, args=None):
        print('Menu')

def register_commands(command_handler):
    command_handler.register_command('menu', MenuCommand())
