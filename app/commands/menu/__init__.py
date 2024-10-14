import sys
from app.commands import Command
import logging

class MenuCommand(Command):
    def execute(self):
        logging.info(f'Menu')