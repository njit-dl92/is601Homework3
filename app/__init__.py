# app/__init__.py
import os
import pkgutil
import importlib
import sys
import multiprocessing
from app.commands import CommandHandler
from dotenv import load_dotenv
import logging
import logging.config

class App:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()
        self.processes = []

    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)

    def load_plugins(self):
        """Dynamically load all plugins in the plugins directory."""
        plugins_package = 'app.plugins'
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if is_pkg:  # Ensure it's a package
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                # Check if there is a register_commands function
                if hasattr(plugin_module, 'register_commands'):
                    plugin_module.register_commands(self.command_handler)

    def execute_in_process(self, command_input):
        """Execute the command in a separate process."""
        command_parts = command_input.split()
        command_name = command_parts[0]
        command_args = command_parts[1:]  # All arguments after the command name
        process = multiprocessing.Process(target=self.command_handler.execute_command, args=(command_name, command_args))
        process.start()
        self.processes.append(process)

    def start(self):
        # Load and register commands here
        self.load_plugins()
        logging.info("Type 'exit' to exit.")
        try:
            while True:  # REPL: Read, Evaluate, Print, Loop
                user_input = input(">>> ").strip()
                if user_input.lower() == 'exit':
                    break
                self.execute_in_process(user_input)
        except KeyboardInterrupt:
            logging.info("Exiting...")
        finally:
            self.cleanup_processes()

    def cleanup_processes(self):
        """Ensure all processes are properly terminated."""
        for process in self.processes:
            if process.is_alive():
                process.terminate()
        for process in self.processes:
            process.join()


