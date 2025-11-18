from eth_utils import to_wei  # type: ignore
import boa  # type: ignore
from tests.conftest import SEND_VALUE
from moccasin.config import get_active_network  # type: ignore


RANDOM_USER = boa.env.generate_address("non-owner")


# Testing that the price feed is set correctly #
def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address


# Testing starting values #
def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address


# Funding fails without enough ETH #
def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts():
        coffee.fund()


# Owner can fund with enough money #
def test_fund_with_money(coffee, account):
    # Arrange #
    boa.env.set_balance(account.address, SEND_VALUE)
    # Act #
    coffee.fund(value=SEND_VALUE)
    # Assert #
    funder = coffee.funders(0)
    assert funder == account.address
    assert coffee.funder_to_amount_funded(funder) == SEND_VALUE


# Non-owner cannot withdraw #
def test_non_owner_cannot_withdraw(coffee_funded, account):
    # Act / Assert #
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee_funded.withdraw()


# Owner can withdraw #
def test_owner_can_withdraw(coffee_funded, account):
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) == 0


# Testing multiple funders #
def test_multiple_funders_withdraw(coffee, account):
    # Arrange #
    number_of_funders = 10
    funders = []
    for i in range(number_of_funders):
        funder = boa.env.generate_address(f"funder-{i}")
        funders.append(funder)
        boa.env.set_balance(funder, SEND_VALUE)
        with boa.env.prank(funder):
            coffee.fund(value=SEND_VALUE)
    starting_owner_balance = boa.env.get_balance(coffee.OWNER())

    # Act #
    with boa.env.prank(coffee.OWNER()):
        coffee.withdraw()

    # Assert #
    assert boa.env.get_balance(coffee.address) == 0
    assert boa.env.get_balance(coffee.OWNER()) == starting_owner_balance + (
        SEND_VALUE * number_of_funders
    )

    for funder in funders:
        assert coffee.funder_to_amount_funded(funder) == 0


# Testing get_eth_to_usd_rate function #
def test_get_rate(coffee):
    # Test with 1 ETH: should be 2000 USD * 10**18 #
    expected = 2000 * 10**18  # 2000000000000000000000 #
    assert coffee.get_eth_to_usd_rate(SEND_VALUE) == expected

    # Test with 0 ETH #
    assert coffee.get_eth_to_usd_rate(0) == 0

    # Test with half ETH #
    half_eth = SEND_VALUE // 2
    expected_half = expected // 2
    assert coffee.get_eth_to_usd_rate(half_eth) == expected_half


#####################################################################
#  Further Tests # EXPANDED #
#####################################################################
# Testing if the contract is verified #
def test_if_contract_is_verified(coffee):
    # Just a placeholder test to ensure the contract is verified after deployment #
    assert coffee.address is not None
    assert boa.env.get_code(coffee.address) != b""
    print("Contract is verified and code is present at address:", coffee.address)


# Testing active network name #
def test_active_network_name():
    # Just a placeholder test to print the active network name #
    active_network = get_active_network()
    assert active_network.name is not None
    print("Active network name is:", active_network.name)


# Testing price feed address from manifest #
def test_price_feed_address(eth_usd):
    # Just a placeholder test to print the price feed address from manifest #
    assert eth_usd.address is not None
    print("Price feed address from manifest is:", eth_usd.address)


# Testing contract verification on non-local network #
def test_deploy_coffee_verification(monkeypatch, eth_usd):
    from script.deploy import deploy_coffee
    from unittest.mock import Mock

    # Create a mock network #
    mock_network = Mock()
    mock_network.has_explorer.return_value = True
    mock_network.is_local_or_forked_network.return_value = False
    mock_verify_result = Mock()
    mock_network.moccasin_verify.return_value = mock_verify_result

    # Patch get_active_network to return the mock #
    monkeypatch.setattr("script.deploy.get_active_network", lambda: mock_network)

    # Call deploy_coffee #
    coffee = deploy_coffee(eth_usd)

    # Assert that verification was attempted #
    mock_network.moccasin_verify.assert_called_once_with(coffee)
    mock_verify_result.wait_for_verification.assert_called_once()


#####################################################################
#  Tests for moccasin_main  #
#####################################################################
def test_moccasin_main(monkeypatch):
    from script.deploy import moccasin_main
    from unittest.mock import Mock

    # Create mocks #
    mock_network = Mock()
    mock_price_feed = Mock()
    mock_coffee = Mock()
    mock_network.manifest_named.return_value = mock_price_feed
    mock_network.name = "test_network"
    mock_price_feed.address = "0x123"

    # Mock deploy_coffee #
    def mock_deploy_coffee(price_feed):
        assert price_feed == mock_price_feed
        return mock_coffee

    # Patch functions #
    monkeypatch.setattr("script.deploy.get_active_network", lambda: mock_network)
    monkeypatch.setattr("script.deploy.deploy_coffee", mock_deploy_coffee)

    # Call moccasin_main #
    result = moccasin_main()

    # Assert #
    mock_network.manifest_named.assert_called_once_with("price_feed")
    assert result == mock_coffee


#####################################################################
#  Tests for MockV3Aggregator  #
#####################################################################
def test_mock_aggregator_initialization(eth_usd):
    # Check initial values
    assert eth_usd.version() == 4
    round_id, answer, started_at, updated_at, answered_in_round = (
        eth_usd.latestRoundData()
    )
    assert round_id == 1  # After first updateAnswer
    assert answer == 200000000000  # 2000 * 10**8

#####################################################################
#  Further Tests for MockV3Aggregator  #
#####################################################################
def test_mock_aggregator_update_round_data(eth_usd):
    # Update round data
    eth_usd.updateRoundData(2, 210000000000, 1234567890, 1234567800)
    round_id, answer, started_at, updated_at, answered_in_round = (
        eth_usd.latestRoundData()
    )
    assert round_id == 2
    assert answer == 210000000000
    assert updated_at == 1234567890
    assert started_at == 1234567800

######################################################################
#  Further Tests for MockV3Aggregator  #
######################################################################
def test_mock_aggregator_get_round_data(eth_usd):
    # Get round data for round 1
    round_id, answer, started_at, updated_at, answered_in_round = eth_usd.getRoundData(
        1
    )
    assert round_id == 1
    assert answer == 200000000000


#####################################################################
#  Tests for script/withdraw.py  #
#####################################################################
def test_withdraw(monkeypatch):
    from script.withdraw import withdraw
    from unittest.mock import Mock

    # Create mocks #
    mock_network = Mock()
    mock_coffee = Mock()
    mock_network.manifest_named.return_value = mock_coffee
    mock_network.name = "test_network"
    mock_coffee.address = "0x123"

    # Patch get_active_network #
    monkeypatch.setattr("script.withdraw.get_active_network", lambda: mock_network)

    # Call withdraw #
    withdraw()

    # Assert #
    mock_network.manifest_named.assert_called_once_with("coffee")
    mock_coffee.withdraw.assert_called_once()

#####################################################################
#  Tests for moccasin_main in withdraw.py # EXPANDED
#####################################################################
def test_withdraw_moccasin_main(monkeypatch):
    from script.withdraw import moccasin_main
    from unittest.mock import Mock

    # Create mocks #
    mock_network = Mock()
    mock_coffee = Mock()
    mock_network.manifest_named.return_value = mock_coffee
    mock_network.name = "test_network"
    mock_coffee.address = "0x123"

    # Patch get_active_network #
    monkeypatch.setattr("script.withdraw.get_active_network", lambda: mock_network)

    # Call moccasin_main #
    result = moccasin_main()

    # Assert #
    mock_network.manifest_named.assert_called_once_with("coffee")
    mock_coffee.withdraw.assert_called_once()
    assert result is None  # withdraw returns None #


#####################################################################
#  Tests for script/storage.py  # EXPANDED 
#####################################################################
def test_deploy_storage(monkeypatch):
    from script.storage import deploy_storage
    from unittest.mock import Mock

    # Create mocks #
    mock_network = Mock()
    mock_fws = Mock()
    mock_fws.address = "0x456"
    mock_verify_result = Mock()
    mock_network.has_explorer.return_value = True
    mock_network.moccasin_verify.return_value = mock_verify_result

    #####################################
    # Mock deploy_storage --- IGNORE ---
    #####################################
    def mock_deploy():
        return mock_fws

    monkeypatch.setattr("script.storage.fun_with_storage.deploy", mock_deploy)
    monkeypatch.setattr("script.storage.get_active_network", lambda: mock_network)

    # Mock storage accesses #
    monkeypatch.setattr(
        "boa.env.get_storage",
        lambda addr, slot: {
            0: 25,  # favorite_number
            2: 222,  # my_fixed_array[0]
            1002: 1,  # dyn array length
            1003: 333,  # dyn array[0]
            1103: 0,  # mapping placeholder
        }.get(slot, 0),
    )

    # Mock boa.eval for mapping location #
    monkeypatch.setattr("boa.eval", lambda expr: 12345)  # Mock location

    # Call deploy_storage #
    deploy_storage()

    # Assert verification was attempted #
    mock_network.moccasin_verify.assert_called_once_with(mock_fws)
    mock_verify_result.wait_for_verification.assert_called_once()


def test_storage_moccasin_main(monkeypatch):
    from script.storage import moccasin_main
    from unittest.mock import Mock

    # Mock deploy_storage #
    mock_deploy = Mock()
    monkeypatch.setattr("script.storage.deploy_storage", mock_deploy)

    # Call moccasin_main #
    moccasin_main()

    # Assert deploy_storage was called #
    mock_deploy.assert_called_once()
