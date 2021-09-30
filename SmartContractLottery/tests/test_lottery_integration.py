from brownie import network
from scripts import helpfulscripts, deploy
import pytest
import time


def test_can_pick_winner():
    pass

    if network.show_active() in helpfulscripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy.deployLotto()
    account = helpfulscripts.getAccount()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEnteranceFee() + 1000})
    lottery.enter({"from": account, "value": lottery.getEnteranceFee() + 1000})
    lottery.enter({"from": account, "value": lottery.getEnteranceFee() + 1000})
    helpfulscripts.fundWithLink(lottery)
    lottery.endLottery({"from": account})
    time.sleep(10)

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
