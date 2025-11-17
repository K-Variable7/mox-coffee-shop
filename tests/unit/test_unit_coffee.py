from eth_utils import to_wei  # type: ignore
import boa  # type: ignore
from tests.conftest import SEND_VALUE


RANDOM_USER = boa.env.generate_address("non-owner")


# Testing that the price feed is set correctly
def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address


# Testing starting values
def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address


# Funding fails without enough ETH
def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts():
        coffee.fund()


# Owner can fund with enough money
def test_fund_with_money(coffee, account):
    # Arrange
    boa.env.set_balance(account.address, SEND_VALUE)
    # Act
    coffee.fund(value=SEND_VALUE)
    # Assert
    funder = coffee.funders(0)
    assert funder == account.address
    assert coffee.funder_to_amount_funded(funder) == SEND_VALUE


# Non-owner cannot withdraw
def test_non_owner_cannot_withdraw(coffee_funded, account):
    # Act / Assert
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee_funded.withdraw()


# Owner can withdraw
def test_owner_can_withdraw(coffee_funded, account):
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) == 0


# Testing multiple funders
def test_multiple_funders_withdraw(coffee, account):
    # Arrange
    number_of_funders = 10
    funders = []
    for i in range(number_of_funders):
        funder = boa.env.generate_address(f"funder-{i}")
        funders.append(funder)
        boa.env.set_balance(funder, SEND_VALUE)
        with boa.env.prank(funder):
            coffee.fund(value=SEND_VALUE)
    starting_owner_balance = boa.env.get_balance(coffee.OWNER())

    # Act
    with boa.env.prank(coffee.OWNER()):
        coffee.withdraw()

    # Assert
    assert boa.env.get_balance(coffee.address) == 0
    assert boa.env.get_balance(coffee.OWNER()) == starting_owner_balance + (
        SEND_VALUE * number_of_funders
    )

    for funder in funders:
        assert coffee.funder_to_amount_funded(funder) == 0


def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_VALUE) > 0
