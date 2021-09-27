from scripts.helpfulscripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me

import pytest
from brownie import network, accounts, exceptions


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    enterance_fee = fund_me.GetEnteranceFee()
    tx = fund_me.fund({"from": account, "value": enterance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == enterance_fee

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()  # get random blank account
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})