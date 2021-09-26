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

deployment_address = "0xA653b2825f56C01E02556291f826b0d039A00f4e"
# sorry moon boi's this isn't a live private key, just local testnet - gl on your github scraping
private_key = "0x45800fc611b16547f7f58969a353fab525a5476149c4c24f3b693b066b05e50c"


def deploy_simple_storage():
    account = accounts[0]
    print(account)


def main():
    deploy_simple_storage()
