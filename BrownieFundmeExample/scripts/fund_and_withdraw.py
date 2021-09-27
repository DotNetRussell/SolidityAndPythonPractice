from brownie import FundMe
from scripts import helpfulscripts


def fund():
    fund_me = FundMe[-1]
    account = helpfulscripts.get_account()
    enterance_fee = fund_me.GetEnteranceFee()
    print(enterance_fee)

    fund_me.fund({"from": account, "value": enterance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = helpfulscripts.get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
