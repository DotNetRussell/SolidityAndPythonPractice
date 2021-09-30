from brownie import config, network, accounts, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken, interface
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev", "kovan"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

contract_to_mock = {
        "eth_usd_price_feed": MockV3Aggregator,
        "vrf-coordinator": VRFCoordinatorMock,
        "link-token": LinkToken
    }


def getAccount(index=None, id=None):
    if index:
        return accounts[index]
    elif id:
        return accounts.load(id)
    elif (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        print("Getting account from auto-gnerated accounts")
        print(accounts[0])
        # get brownie auto generated account (it gens 10 this gets index 0)
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def getContract(contractName):
    print(f"Fetching contract {contractName}")
    contractType = contract_to_mock[str(contractName)]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contractType) <= 0:
            deployMocks()
        contract = contractType[-1]
    else:
        contract_address = config["networks"][network.show_active()][contractName]
        contract = Contract.from_abi(
            contractType._name, contract_address, contractType.abi
        )

    return contract


def fundWithLink(contractAddress, account=None, linkToken=None, amount=100000000000000000):
    account = account if account else getAccount()
    linkToken = linkToken if linkToken else getContract("link-token")
    #tx = linkToken.transfer(contractAddress, amount, {"from": account})
    linkTokenContract = interface.LinkTokenInterface(linkToken.address)
    tx = linkTokenContract.transfer(contractAddress, amount, {"from":account})
    tx.wait(1)
    print("Link contract funded")
    return tx


def deployMocks():
    print("Deploying Mocks...")
    account = getAccount()
    MockV3Aggregator.deploy(8, Web3.toWei(2000, "ether"), {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from":account})
    print("Mocks Deployed!")
