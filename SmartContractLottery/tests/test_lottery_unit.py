from brownie import Lottery, accounts, config, network, exceptions
from scripts import deploy, helpfulscripts
from web3 import Web3
import pytest


def test_get_entrance_fee():
    if network.show_active() not in helpfulscripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy.deployLotto()
    fee = lottery.getEntranceFee()
    expected_fee = 2500000

    assert expected_fee == fee


def test_cant_enter_unless_starter():
    if network.show_active() not in helpfulscripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy.deployLotto()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": helpfulscripts.getAccount(), "value":lottery.getEntranceFee()})


def test_can_start_and_enter_lotto():
    if network.show_active() not in helpfulscripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy.deployLotto()
    account = helpfulscripts.getAccount()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})

    assert lottery.players(0) == account


def test_can_end_lotto():
    if network.show_active() not in helpfulscripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy.deployLotto()
    account = helpfulscripts.getAccount()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    helpfulscripts.fundWithLink(lottery)
    lottery.endLottery({"from": account})

    assert lottery.lottery_state() == 2


def test_does_lotto_pick_correct_winner():
    if network.show_active() not in helpfulscripts.LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy.deployLotto()
    account = helpfulscripts.getAccount()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": helpfulscripts.getAccount(1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": helpfulscripts.getAccount(2), "value": lottery.getEntranceFee()})
    helpfulscripts.fundWithLink(lottery)

    tx = lottery.endLottery({"from": account})

    requestId = tx.events["RequestedRandomness"]["requestId"]
    helpfulscripts.getContract("vrf-coordinator").callBackWithRandomness(requestId, 777, lottery.address, {"from": account})

    startingAccountBalance = account.balance()
    lotteryBalance = lottery.balance()

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == startingAccountBalance + lotteryBalance