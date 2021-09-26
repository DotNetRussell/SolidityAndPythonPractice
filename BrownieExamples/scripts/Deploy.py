# helpful commands
#
# deploy python script with brownie
# ~brownie run scripts/Deploy.py
#
# Compile contracts under ./contracts folder
# ~brownie compile
#
# Initialize brownie
# ~brownie init
#
# create a new account to use (prompts for private key)
# ~brownie accounts new freecodecamp-account
#
# list all accounts
# ~brownie accounts list
#
# delete browning account
# ~brownie account delete freecodecamp-account

from brownie import accounts


def deploy_simple_storage():
    account = accounts.load("freecodecamp-account")
    print(account)


def main():
    deploy_simple_storage()
