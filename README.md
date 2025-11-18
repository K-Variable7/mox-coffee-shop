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

## Extra Credit [Modules]
- The price feed logic is modularized into a separate module, allowing for easier maintenance and potential reuse in other contracts.
- Coverage should be above 90% for all functions in the contract (challenge yourselves to reach 100%!).
- Include detailed docstrings for all functions and modules to enhance code readability and maintainability.
- Implement error handling for edge cases, such as invalid price feed addresses or insufficient funds.
- Write additional tests to cover scenarios like price feed failures or unexpected ETH/USD rates.
- Optimize gas usage by minimizing state changes and using efficient data structures where applicable.