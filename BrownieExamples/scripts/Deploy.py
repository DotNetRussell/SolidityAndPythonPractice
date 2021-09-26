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
#
# list all of the known brownie networks (development get built and tore down each brownie instance)
# ~brownie networks list
#
from brownie import accounts, config, SimpleStorage, network


def get_account():

    if network.show_active() == "development":
        # get brownie auto generated account (it gens 10 this gets index 0)
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_simple_storage(account):

    # this retrieves the account setup at commandline
    # account = accounts.load("freecodecamp-account")

    # this setups an account from a private key stored in an environment variable named PRIVATE_KEY in the .env file
    # account = accounts.add(os.getenv("PRIVATE_KEY"))

    # getting the same private key as above but from the config instead of the os env var
    # account = accounts.add(config["wallets"]["from_key"])

    # this gets the simple storage contract and deploys it from the account assigned above
    simple_storage = SimpleStorage.deploy({"from": account})
    return simple_storage


def storeValueAndRetrieveValue(simple_storage, account):
    # brownie is smart enough to know if it's a transaction or a callv
    stored_value = simple_storage.retrieve()
    print("Stored Value: " + str(stored_value))
    transaction = simple_storage.store(20, {"from": account})
    transaction.wait(1)
    stored_value = simple_storage.retrieve()
    print("Updated Stored Value: " + str(stored_value))


def main():
    account = get_account()
    storage_contract = deploy_simple_storage(account)
    storeValueAndRetrieveValue(storage_contract, account)
