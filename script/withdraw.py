from src import buy_me_a_coffee  # type: ignore
from moccasin.config import get_active_network  # type: ignore


def withdraw():
    active_network = get_active_network()
    coffee = active_network.manifest_named("coffee")
    print(f"Working with contract {coffee.address}")
    print(f"On network {active_network.name}, withdrawing from {coffee.address}")
    coffee.withdraw()
    print("Withdrawal completed successfully!")


def moccassin_main():
    return withdraw()
