from brownie import DNRToken
from scripts import helpfulscripts
from web3 import Web3

def deploy_token():
    account = helpfulscripts.getAccount()
    dnrToken = DNRToken.deploy(Web3.toWei(1000000, "ether"), {"from": account})
    print(dnrToken.name() + " has been deployed to your local test net")


def main():
    deploy_token()