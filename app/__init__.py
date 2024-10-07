# app/__init__.py
import pkgutil
import importlib
import multiprocessing
from app.commands import CommandHandler

class App:
    def __init__(self):
        self.command_handler = CommandHandler()
        self.processes = []

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
        print("Type 'exit' to exit.")
        try:
            while True:  # REPL: Read, Evaluate, Print, Loop
                user_input = input(">>> ").strip()
                if user_input.lower() == 'exit':
                    break
                self.execute_in_process(user_input)
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            self.cleanup_processes()

    def cleanup_processes(self):
        """Ensure all processes are properly terminated."""
        for process in self.processes:
            if process.is_alive():
                process.terminate()
        for process in self.processes:
            process.join()


