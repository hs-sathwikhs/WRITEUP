import os
import time
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# Connect to Sepolia (Public RPC or use your own Alchemy/Infura URL)
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Inject POA middleware (needed for some testnets like Sepolia)
web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

if not web3.is_connected():
    print("Failed to connect to Sepolia network.")
    exit()

print("Connected to Sepolia!")

# Set your private key as an environment variable or paste it here (BE CAREFUL WITH REAL FUNDS! USE A BURNER WALLET)
PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE"  # Replace with your private key or set via environment variable
if PRIVATE_KEY == "YOUR_PRIVATE_KEY_HERE":
    print("Please set your private key in the script or via the PRIVATE_KEY environment variable.")
    exit()

account = web3.eth.account.from_key(PRIVATE_KEY)
address = account.address
print(f"Using address: {address}")

CONTRACT_ADDRESS = "0x53e442053A5Fd72e4e3BAb21D24fca700CDFc612"

# Minimal ABI for the functions we need
ABI = [
    {
        "inputs": [],
        "name": "enterTheCave",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "revealFlag",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def enter_cave():
    print("Building transaction for enterTheCave()...")
    nonce = web3.eth.get_transaction_count(address)
    
    tx = contract.functions.enterTheCave().build_transaction({
        'chainId': 11155111, # Sepolia Chain ID
        'gas': 200000,
        'maxFeePerGas': web3.to_wei('10', 'gwei'),
        'maxPriorityFeePerGas': web3.to_wei('1', 'gwei'),
        'nonce': nonce,
    })

    print("Signing transaction...")
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)

    print("Sending transaction...")
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)  # Fixed deprecation
    
    print(f"Transaction sent! Hash: {web3.to_hex(tx_hash)}")
    print("Waiting for receipt...")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction confirmed in block:", receipt.blockNumber)

def get_flag():
    print("Calling revealFlag()...")
    flag = contract.functions.revealFlag().call({'from': address})
    print("\n========================================")
    print(f"YOUR FLAG: {flag}")
    print("========================================\n")

if __name__ == "__main__":
    # 1. First send the transaction (uncomment if you haven't done it yet)
    enter_cave()
    
    # 2. Then get the flag
    get_flag()
