import csv
from datetime import datetime, timedelta
import random
import uuid
import argparse
import json

def generate_transaction_id():
    """
    Generate a unique transaction ID.

    Returns:
        str: A unique UUID as a string.
    """
    return str(uuid.uuid4())

def benford_amount():
    """
    Generate an amount that follows Benford's Law.

    Returns:
        float: A float value where the first digit follows Benford's Law distribution.
    """
    first_digit = random.choices(range(1, 10), weights=[30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6])[0]
    rest_digits = random.randint(0, 999999)
    return float(f"{first_digit}.{rest_digits:06d}")

def generate_recurring_transactions(config):
    """
    Generate recurring transactions based on the configuration.

    Args:
        config (dict): The configuration dictionary containing start_date, end_date, and recurring_transactions.

    Returns:
        list: A list of recurring transactions.
    """
    transactions = []
    current_date = config['start_date']
    while current_date <= config['end_date']:
        for rt in config.get('recurring_transactions', []):
            if current_date.day == rt['day']:
                amount = rt['amount'] * random.uniform(0.95, 1.05)
                transactions.append([
                    generate_transaction_id(),
                    current_date.strftime('%Y-%m-%d'),
                    'Payment',
                    round(amount, 2),
                    f"ACCT-{random.randint(1000, 9999)}",
                    rt['description'],
                    rt['vendor']
                ])
        current_date += timedelta(days=1)
    return transactions

def generate_random_transactions(config):
    """
    Generate random transactions based on the configuration.

    Args:
        config (dict): The configuration dictionary containing start_date, end_date, num_transactions, and vendors.

    Returns:
        list: A list of random transactions.
    """
    transactions = []
    date_range = (config['end_date'] - config['start_date']).days
    num_random = config['num_transactions'] - len(config.get('recurring_transactions', [])) * date_range // 30

    vendors = config.get('vendors', [])
    if not vendors:
        vendors = ["Default Vendor"]  # Fallback if no vendors are specified

    for _ in range(num_random):
        date = config['start_date'] + timedelta(days=random.randint(0, date_range))
        transaction_type = random.choice(['Purchase', 'Payment', 'Transfer', 'Deposit', 'Withdrawal'])
        amount = round(benford_amount() * 1000, 2)
        account = f"ACCT-{random.randint(1000, 9999)}"
        vendor = random.choice(vendors)
        description = f"{transaction_type} - {random.choice(['Office Supplies', 'Equipment', 'Services', 'Miscellaneous'])}"
        
        transactions.append([
            generate_transaction_id(),
            date.strftime('%Y-%m-%d'),
            transaction_type,
            amount,
            account,
            description,
            vendor
        ])
    return transactions

def apply_irregularities(transactions, config):
    """
    Apply irregularities to the transactions based on the configuration.

    Args:
        transactions (list): The list of transactions to apply irregularities to.
        config (dict): The configuration dictionary containing irregularity settings.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    irregularity_functions = {
        'high_amount': high_amount,
        'frequency_change': frequency_change,
        'double_spend': double_spend,
        'missing_id': missing_id,
        'incorrect_date': incorrect_date,
        'mismatched_description': mismatched_description,
        'wrong_account': wrong_account,
        'personal_expense': personal_expense,
        'benford_violation': benford_violation,
        'subtle_skimming': subtle_skimming,
        'seasonal_anomaly': seasonal_anomaly,
        'round_number_bias': round_number_bias
    }

    num_irregularities = int(len(transactions) * config.get('irregularity_percentage', 0.05))
    enabled_irregularities = config.get('enabled_irregularities', [])
    
    if not enabled_irregularities:
        print("Warning: No irregularities enabled in config. Skipping irregularity application.")
        return

    for _ in range(num_irregularities):
        index = random.randint(0, len(transactions) - 1)
        irregularity_type = random.choice(enabled_irregularities)
        if irregularity_type in irregularity_functions:
            irregularity_functions[irregularity_type](transactions, index, config)
        else:
            print(f"Warning: Unknown irregularity type '{irregularity_type}'. Skipping.")

def apply_cumulative_irregularity(transactions, config):
    """
    Apply cumulative irregularity to the transactions.

    Args:
        transactions (list): The list of transactions to apply cumulative irregularity to.
        config (dict): The configuration dictionary containing cumulative irregularity settings.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    if 'cumulative_irregularity' not in config.get('enabled_irregularities', []):
        return
    total_expenses = sum(t[3] for t in transactions if t[2] in ['Purchase', 'Payment'])
    threshold = total_expenses * config.get('cumulative_threshold', 0.005)
    cumulative_irregular = 0
    for transaction in transactions:
        if transaction[2] in ['Purchase', 'Payment'] and random.random() < 0.1:
            irregular_amount = round(random.uniform(1, 10), 2)
            transaction[3] += irregular_amount
            cumulative_irregular += irregular_amount
            if cumulative_irregular > threshold:
                break

# Irregularity functions
def high_amount(transactions, index, config):
    """
    Apply high amount irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    transactions[index][3] = round(random.uniform(50000, 100000), 2)

def frequency_change(transactions, index, config):
    """
    Apply frequency change irregularity to a recurring transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    if any(rt['description'] in transactions[index][5] for rt in config.get('recurring_transactions', [])):
        new_day = random.randint(1, 28)
        transactions[index][1] = transactions[index][1][:8] + f"{new_day:02d}"

def double_spend(transactions, index, config):
    """
    Apply double spend irregularity by duplicating a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to duplicate.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    duplicate = transactions[index].copy()
    duplicate[0] = generate_transaction_id()
    duplicate[1] = (datetime.strptime(duplicate[1], '%Y-%m-%d') + timedelta(minutes=random.randint(1, 60))).strftime('%Y-%m-%d %H:%M')
    transactions.append(duplicate)

def missing_id(transactions, index, config):
    """
    Apply missing ID irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    transactions[index][0] = ''

def incorrect_date(transactions, index, config):
    """
    Apply incorrect date irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    future_date = config['end_date'] + timedelta(days=random.randint(1, 30))
    transactions[index][1] = future_date.strftime('%Y-%m-%d')

def mismatched_description(transactions, index, config):
    """
    Apply mismatched description irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    if transactions[index][2] == 'Deposit':
        transactions[index][5] = 'Withdrawal - Miscellaneous'
    elif transactions[index][2] == 'Withdrawal':
        transactions[index][5] = 'Deposit - Miscellaneous'

def wrong_account(transactions, index, config):
    """
    Apply wrong account irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    transactions[index][4] = f"WRONG-{random.randint(100, 999)}"

def personal_expense(transactions, index, config):
    """
    Apply personal expense irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    personal_vendors = config.get('personal_vendors', ["Personal Vendor"])
    personal_descriptions = config.get('personal_expense_descriptions', ["Personal Expense"])
    transactions[index][6] = random.choice(personal_vendors)
    transactions[index][5] = random.choice(personal_descriptions)
    transactions[index][3] = round(random.uniform(100, 5000), 2)

def benford_violation(transactions, index, config):
    """
    Apply Benford's Law violation irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    first_digit = random.choice([5, 6])
    rest_digits = random.randint(0, 999999)
    transactions[index][3] = float(f"{first_digit}.{rest_digits:06d}") * 1000

def subtle_skimming(transactions, index, config):
    """
    Apply subtle skimming irregularity to a set of transactions.

    Args:
        transactions (list): The list of transactions.
        index (int): The starting index of the transactions to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    for i in range(index, min(index + 10, len(transactions))):
        transactions[i][3] *= 0.99

def seasonal_anomaly(transactions, index, config):
    """
    Apply seasonal anomaly irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    if datetime.strptime(transactions[index][1], '%Y-%m-%d').month in [1, 2, 12]:
        transactions[index][5] = "Summer Equipment Purchase"
        transactions[index][3] = round(random.uniform(5000, 10000), 2)

def round_number_bias(transactions, index, config):
    """
    Apply round number bias irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        None: This function modifies the transactions list in-place.
    """
    transactions[index][3] = round(transactions[index][3], -2)

def load_config(config_file):
    """
    Load and parse the configuration file.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        dict: The parsed configuration as a dictionary.
    """
    with open(config_file, 'r') as f:
        config = json.load(f)
    config['start_date'] = datetime.strptime(config['start_date'], '%Y-%m-%d')
    config['end_date'] = datetime.strptime(config['end_date'], '%Y-%m-%d')
    return config

def save_to_csv(transactions, filename):
    """
    Save the transactions to a CSV file.

    Args:
        transactions (list): The list of transactions to save.
        filename (str): The name of the output CSV file.

    Returns:
        None: This function writes to a file.
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Transaction ID', 'Date', 'Type', 'Amount', 'Account', 'Description', 'Vendor'])
        writer.writerows(transactions)

def generate_transactions(config):
    """
    Generate all transactions based on the configuration.

    Args:
        config (dict): The configuration dictionary.

    Returns:
        list: A sorted list of all generated transactions.
    """
    transactions = []
    transactions.extend(generate_recurring_transactions(config))
    transactions.extend(generate_random_transactions(config))
    apply_irregularities(transactions, config)
    apply_cumulative_irregularity(transactions, config)
    return sorted(transactions, key=lambda x: x[1])  # Sort by date

def main():
    """
    The main function to run the script.

    This function parses command-line arguments, loads the configuration,
    generates transactions, and saves them to a CSV file.

    Returns:
        None: This function executes the script's main logic.
    """
    parser = argparse.ArgumentParser(description="Generate fake transaction data with configurable irregularities.")
    parser.add_argument('-c', '--config', default='config.json', help='Path to the configuration file')
    parser.add_argument('-o', '--output', default='fake_transactions.csv', help='Output CSV file name')
    args = parser.parse_args()

    config = load_config(args.config)
    transactions = generate_transactions(config)
    save_to_csv(transactions, args.output)

    print(f"{len(transactions)} fake transactions have been generated and saved to '{args.output}'")

if __name__ == "__main__":
    main()