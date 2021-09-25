#!/usr/bin/python3
import json
from web3 import Web3

#this file will compile our solidity contracts and output it into compiled_code.json

from solcx import install_solc
install_solc('v0.6.6')
from solcx import compile_standard

#reading our solidity files
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

#setting up the compiler 
compiled_sol = compile_standard(
    {
        "language": "Solidity", 
        "sources": 
        {
            "SimpleStorage.sol": 
            {
                "content": simple_storage_file
            }
        },    
        "settings": {
            "outputSelection": {
                "*" :{
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.6",)

#write out the complied code
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#get the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get the abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

with open("SimpleStorageAbi.json", "w") as file:
    json.dump(abi, file)

# Setup Ganache Connection
chain_id = 1337;
deployment_address = "0xC7cc779542DdCe98a7038123980CF0327bc6f1Bc"

#sorry moon boi's this isn't a live private key, just local testnet - gl on your github scraping 
private_key = "0xf8b342744c4350f5d19d2f7eef645857bb65a0afbc3ad44320b8440072902228"

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
# Get latest transaction
nonce = w3.eth.getTransactionCount(deployment_address)

#get a contract from the abi and bytecode
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

def CreateContract():
    transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "from": deployment_address, "nonce": nonce})
    
    signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    #push the transaction to the blockchain
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    #waiting for confiramtions 
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

def CallStoreFunction(numberToStore):
    store_tx = simple_storage.functions.store(numberToStore).buildTransaction({"chainId": chain_id, "from": deployment_address, "nonce": nonce + 1})

    signed_tx = w3.eth.account.sign_transaction(store_tx, private_key=private_key)
    #push the transaction to the blockchain
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    #waiting for confiramtions 
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt


#retrieve the contract
simple_storage = w3.eth.contract(address=CreateContract().contractAddress, abi=abi)

#make a call to the retireve function in our contract
print(simple_storage.functions.retrieve().call())

#Store the number 20 on the contract 
CallStoreFunction(20)

#make a call to the retireve function in our contract
print(simple_storage.functions.retrieve().call())
