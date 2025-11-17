from src.mocks import mock_v3_aggregator  # type: ignore
from moccasin.boa_tools import VyperContract  # type: ignore

STARTING_DECIMALS = 8
STARTING_PRICE = int(2000e8)  # 2000 * 10**8


def deploy_feed() -> VyperContract:
    return mock_v3_aggregator.deploy(STARTING_DECIMALS, STARTING_PRICE)


def moccasin_main() -> VyperContract:
    return deploy_feed()
