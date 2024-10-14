from app.commands import Command
import logging

class GoodbyeCommand(Command):
    def execute(self):
        logging.info("Goodbye")