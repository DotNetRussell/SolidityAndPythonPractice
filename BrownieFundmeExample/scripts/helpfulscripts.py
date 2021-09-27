from brownie import config, network, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        print("Getting account from auto-gnerated accounts")
        print(accounts[0])
        # get brownie auto generated account (it gens 10 this gets index 0)
        return accounts[0]
    else:
        print("Getting account from private key in config")
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print("Deploying Mocks")
    MockV3Aggregator.deploy(8, Web3.toWei(2000, "ether"), {"from": get_account()})
