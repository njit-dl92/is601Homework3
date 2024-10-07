import pkgutil
import importlib
import multiprocessing
from app.commands import CommandHandler, Command

class App:
    def __init__(self):
        self.command_handler = CommandHandler()
        self.processes = []

    def load_plugins(self):
        # Dynamically load all plugins in the plugins directory
        plugins_package = 'app.plugins'
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if is_pkg:  # Ensure it's a package
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, Command):  # Assuming a Command class exists
                            self.command_handler.register_command(plugin_name, item())
                    except TypeError:
                        continue  # If item is not a class or unrelated class, just ignore

    def execute_in_process(self, command_input):
        """Execute the command in a separate process."""
        process = multiprocessing.Process(target=self.command_handler.execute_command, args=(command_input,))
        process.start()
        self.processes.append(process)

    def start(self):
        # Register commands here
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
