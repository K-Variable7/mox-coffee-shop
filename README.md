# Mox Coffee Shop
- Welcome to the Coffee Shop!

## Quickstart
- Install dependencies
- Deploy the mock price feed
- Deploy the contract
- Run tests
- View documentation
- Enjoy your coffee!


## Purpose
- This is a simple smart contract that allows users to buy a coffee (send ETH) to the contract owner, provided that the amount sent is at least $5 worth of ETH. The contract uses a price feed to determine the current ETH/USD exchange rate.
- The contract is modularized to separate the price fetching logic into its own module for better organization and reusability.
- The contract is written in Vyper and uses Chainlink's AggregatorV3Interface for price feeds.
- Feel free to explore the code and contribute!
- Happy coding and enjoy your coffee! ☕

## Notes
- Make sure to replace the price feed address with the appropriate one for your network when deploying the contract.
- This project is for educational purposes and should not be used in production without proper security audits.