from brownie import accounts, config, SimpleStorage


def read_contract():
    # -1 will always get the most recent deployment of the contract
    latest_contract = SimpleStorage[-1]
    print(latest_contract)

    # now we can interact with the latest contract
    print(latest_contract.retrieve())


def main():
    read_contract()
