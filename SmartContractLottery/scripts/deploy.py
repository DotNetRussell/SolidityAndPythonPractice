from brownie import Lottery, config, network
from scripts import helpfulscripts

import time

def deployLotto():
    account = helpfulscripts.getAccount(id="freecodecamp-account")

    # address priceFeedAddress,
    # address vrfCoordinator,
    # address link,
    # uint256 fee,
    # bytes32 keyhash
    lottery = Lottery.deploy(
        helpfulscripts.getContract("eth_usd_price_feed").address,
        helpfulscripts.getContract("vrf-coordinator").address,
        helpfulscripts.getContract("link-token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verfiy",False)
        )

    print("Lottery deployed successfully")
    return lottery


def startLotto():
    account = helpfulscripts.getAccount(id="freecodecamp-account")
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lotto has been started")


def enterLotto():
    account = helpfulscripts.getAccount(id="freecodecamp-account")
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 1000000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("Lotto Entered!")


def endLotto():
    account = helpfulscripts.getAccount(id="freecodecamp-account")
    lottery = Lottery[-1]
    fundtx = helpfulscripts.fundWithLink(lottery.address)
    fundtx.wait(1)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    print("Lotto has ended!")
    time.sleep(10)
    print(f"Lottery winner is {lottery.recentWinner()}")


def main():
    deployLotto()
    startLotto()
    enterLotto()
    endLotto()