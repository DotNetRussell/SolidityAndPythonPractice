from web3 import Web3
from brownie import FundMe, config, network, accounts, MockV3Aggregator

from scripts import helpfulscripts


def deploy_fund_me():
    account = helpfulscripts.get_account()

    print(f"Active Network: {network.show_active()}")
    if network.show_active() not in helpfulscripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
        publishSource = config["networks"][network.show_active()]["Validate"]

    else:
        if len(MockV3Aggregator) <= 0:
            helpfulscripts.deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        publishSource = config["networks"][network.show_active()]["Validate"]

    fund_me = FundMe.deploy(
        price_feed_address,  # first arg is constructor parameter
        {"from": account},
        publish_source=publishSource,
    )
    print(f"Contract deployed to address: {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
