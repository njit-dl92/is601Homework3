import sys
from app.commands import Command
import logging

class DiscordCommand(Command):
    def execute(self):
        logging.info(f'I WIll send something to discord')