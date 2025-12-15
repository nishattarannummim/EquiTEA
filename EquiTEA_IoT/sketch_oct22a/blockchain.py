from web3 import Web3
import time

# ----------------------------------
# Network Configuration (PLACEHOLDERS)
# ----------------------------------

INFURA_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"
ADMIN_ADDRESS = "0xADMIN_WALLET_ADDRESS"
CONTRACT_ADDRESS = "0xSMART_CONTRACT_ADDRESS"

# ----------------------------------
# Smart Contract ABI
# ----------------------------------
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string","name": "workerID","type": "string"},
            {"internalType": "uint256","name": "weightInKg","type": "uint256"}
        ],
        "name": "processWage",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string","name": "workerID","type": "string"},
            {"internalType": "address","name": "walletAddress","type": "address"}
        ],
        "name": "registerWorker",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string","name": "workerID","type": "string"},
            {"internalType": "uint256","name": "ratePerKg","type": "uint256"}
        ],
        "name": "setWageRate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string","name": "","type": "string"}],
        "name": "wageRates",
        "outputs": [{"internalType": "uint256","name": "","type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string","name": "","type": "string"}],
        "name": "workerWallets",
        "outputs": [{"internalType": "address","name": "","type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Connect to Sepolia
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
print("Connected to Sepolia:", web3.is_connected())

# Create contract object
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)


# ----- Helper: send transaction and wait for confirmation -----
def send_transaction(txn):
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Transaction sent! Tx hash: {web3.to_hex(tx_hash)}")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    print(f"Transaction confirmed in block {receipt.blockNumber}")
    return receipt


# ----- Blockchain functions -----
def register_worker(worker_id, wallet_address):
    """Register a worker"""
    wallet_address = Web3.to_checksum_address(wallet_address)
    nonce = web3.eth.get_transaction_count(ADMIN_ADDRESS)
    txn = contract.functions.registerWorker(worker_id, wallet_address).build_transaction({
        'from': ADMIN_ADDRESS,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': web3.to_wei('20', 'gwei')
    })
    return send_transaction(txn)


def set_wage_rate(worker_id, rate_per_kg):
    """Set wage rate in wei per kg"""
    nonce = web3.eth.get_transaction_count(ADMIN_ADDRESS)
    txn = contract.functions.setWageRate(worker_id, rate_per_kg).build_transaction({
        'from': ADMIN_ADDRESS,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': web3.to_wei('20', 'gwei')
    })
    return send_transaction(txn)


def get_rate_per_kg(worker_id):
    """Fetch wage rate"""
    return contract.functions.wageRates(worker_id).call()


def process_wage(worker_id, weight_kg):
    """Pay the worker ETH = rate_per_kg * weight_kg"""
    rate = get_rate_per_kg(worker_id)
    if rate == 0:
        print("Wage rate is 0. Set rate first!")
        return None

    value = rate * weight_kg
    nonce = web3.eth.get_transaction_count(ADMIN_ADDRESS)
    txn = contract.functions.processWage(worker_id, weight_kg).build_transaction({
        'from': ADMIN_ADDRESS,
        'nonce': nonce,
        'gas': 250000,
        'gasPrice': web3.to_wei('20', 'gwei'),
        'value': value
    })
    return send_transaction(txn)









