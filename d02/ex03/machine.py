#!/usr/bin/python3

from beverages import Coffee, HotBeverage, Chocolate, Tea, Cappuccino
import random


class CoffeeMachine:

    def __init__(self) -> None:
        self.broken = 10
    
    class EmptyCup(HotBeverage):
        def __init__(self) -> None:
            self.name = "empty cup"
            self.price = 0.90

        def description(self) -> str:
            return "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        def __init__(self) -> None:
            super().__init__("This coffee machine has to be repaired.")

    def repair(self) -> None:
        self.broken = 10

    def serve(self, description: HotBeverage) -> HotBeverage():
        if self.broken <= 0:
            raise CoffeeMachine.BrokenMachineException
        self.broken -= 1
        if random.randint(0, 5) == 0:
            return CoffeeMachine.EmptyCup()
        return description()

def main():
    machine = CoffeeMachine()
    for x in range(0, 12):
        try:
            print(machine.serve(random.choice([Coffee, Cappuccino, Chocolate, Tea])))
        except CoffeeMachine.BrokenMachineException as e:
            print(e)
            machine.repair()


if __name__ == '__main__':
    main()