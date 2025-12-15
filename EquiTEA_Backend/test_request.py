"""
test_request.py

Standalone script to test blockchain functions:
- register a worker
- set wage rate
- process wage

Replace WORKER_ID and WORKER_WALLET with your actual test data.
"""
from blockchain import register_worker, set_wage_rate, process_wage 

# ----------------------------
# Enter your test worker details
# ----------------------------
WORKER_ID = input("Enter worker ID: ").strip()
WORKER_WALLET = input("Enter worker wallet address: ").strip()
RATE_WEI = 1000000000000000  # 0.001 ETH

print("Registering worker...")
register_worker(WORKER_ID, WORKER_WALLET)

print("Setting wage rate...")
set_wage_rate(WORKER_ID, RATE_WEI)

weight_kg = float(input("Enter collected weight (kg): "))
print("Processing wage...")
process_wage(WORKER_ID, weight_kg=5)
