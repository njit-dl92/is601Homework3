from app.commands import Command
import logging

class GreetCommand(Command):
    def execute(self):
        logging.info("Hello, World!")