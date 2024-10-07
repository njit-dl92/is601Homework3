from app.commands import Command


class MultiplyCommand(Command):
    def execute(self, *args):
        a = Decimal(args[0])
        b = Decimal(args[1])
        print(Calculator.multiply(a, b))