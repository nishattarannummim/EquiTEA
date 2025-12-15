from web3 import Web3

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


# ----------------------------------
# Web3 Setup
# ----------------------------------

web3 = Web3(Web3.HTTPProvider(INFURA_URL))
assert web3.is_connected(), "Web3 connection failed"

contract = web3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=CONTRACT_ABI
)

DEFAULT_RATE_ETH = 0.00001
DEFAULT_RATE_WEI = web3.to_wei(DEFAULT_RATE_ETH, "ether")

nonce_tracker = {}

def get_nonce(address=ADMIN_ADDRESS):
    pending = web3.eth.get_transaction_count(address, "pending")
    last = nonce_tracker.get(address, pending - 1)
    nonce_tracker[address] = max(pending, last + 1)
    return nonce_tracker[address]

def send_transaction(txn):
    signed_txn = web3.eth.account.sign_transaction(
        txn, private_key=PRIVATE_KEY
    )
    tx_hash = web3.eth.send_raw_transaction(
        signed_txn.raw_transaction
    )
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return web3.to_hex(tx_hash)

# ----------------------------------
# Core Functions
# ----------------------------------

def register_worker(worker_id, wallet_address):
    wallet_address = Web3.to_checksum_address(wallet_address)
    txn = contract.functions.registerWorker(
        worker_id, wallet_address
    ).build_transaction({
        "from": ADMIN_ADDRESS,
        "nonce": get_nonce(),
        "gas": 200000,
        "gasPrice": web3.to_wei("20", "gwei")
    })
    return send_transaction(txn)

def set_wage_rate(worker_id, rate_per_kg=DEFAULT_RATE_WEI):
    txn = contract.functions.setWageRate(
        worker_id, rate_per_kg
    ).build_transaction({
        "from": ADMIN_ADDRESS,
        "nonce": get_nonce(),
        "gas": 200000,
        "gasPrice": web3.to_wei("20", "gwei")
    })
    return send_transaction(txn)

def process_wage(worker_id, weight_kg):
    txn = contract.functions.processWage(
        worker_id, int(weight_kg)
    ).build_transaction({
        "from": ADMIN_ADDRESS,
        "nonce": get_nonce(),
        "gas": 300000,
        "gasPrice": web3.to_wei("20", "gwei"),
        "value": DEFAULT_RATE_WEI  # prototype: fixed payment
    })
    return send_transaction(txn)
