from src import buy_me_a_coffee  # type: ignore
from moccasin.config import get_active_network  # type: ignore
from moccasin.boa_tools import VyperContract  # type: ignore


def deploy_coffee(price_feed: VyperContract) -> VyperContract:
    print("Deployed BuyMeACoffee Successfully...")
    print("Using price feed at ", price_feed.address)
    coffee: VyperContract = buy_me_a_coffee.deploy(price_feed)

    active_network = get_active_network()
    if (
        active_network.has_explorer()
        and active_network.is_local_or_forked_network() is False
    ):
        print("Verifying contract on explorer...")
        result = active_network.moccasin_verify(coffee)
        result.wait_for_verification()
    return coffee


def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    price_feed: VyperContract = active_network.manifest_named("price_feed")
    print(f"Using price feed at {price_feed.address} on {active_network.name}")
    return deploy_coffee(price_feed)
