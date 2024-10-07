from app.commands import Command


class DivideCommand(Command):
    def execute(self, *args):
        a = Decimal(args[0])
        b = Decimal(args[1])
        if b == Decimal(0):
            print("Error: Division by zero.")
        print(Calculator.divide(a, b))