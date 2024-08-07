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

    This function applies various types of irregularities to the transactions
    as specified in the configuration. It also includes cumulative irregularities
    if enabled in the config.

    Args:
        transactions (list): A list of transaction records to potentially modify.
            Each transaction is expected to be a list or tuple containing
            transaction details.
        config (dict): The configuration dictionary containing irregularity settings.
            Expected to have an 'irregularities' key with sub-dictionaries for
            each irregularity type, including 'cumulative_irregularity'.

    Returns:
        list: A list of tuples, each containing:
            - transaction_id (str): The ID of the modified transaction.
            - irregularity_type (str): The type of irregularity applied.
            - description (str): A description of the modification made.

    Prints:
        - The total number of irregularities to be applied (including cumulative).
        - A list of irregularity types to be applied.
        - A description of each applied irregularity as it's processed.

    Note:
        This function modifies the `transactions` list in-place. The returned list
        only contains information about the applied irregularities, not the
        modified transactions themselves.
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

    irregularity_config = config.get('irregularities', {})
    total_irregularities = sum(irregularity_config.get(irr, {}).get('count', 0) for irr in irregularity_functions.keys())
    
    # Add cumulative irregularity count if enabled
    cumulative_config = irregularity_config.get('cumulative_irregularity', {})
    if cumulative_config.get('enabled', False):
        total_irregularities += cumulative_config.get('count', 0)
    
    print(f"Total irregularities to apply: {total_irregularities}")
    
    applied_irregularities = []
    irregularities_to_apply = []

    for irregularity_type, irregularity_function in irregularity_functions.items():
        count = irregularity_config.get(irregularity_type, {}).get('count', 0)
        irregularities_to_apply.extend([irregularity_type] * count)

    random.shuffle(irregularities_to_apply)
    
    #print(f"Irregularities to apply: {irregularities_to_apply}")

    for irregularity_type in irregularities_to_apply:
        index = random.randint(0, len(transactions) - 1)
        description = irregularity_functions[irregularity_type](transactions, index, config)
        applied_irregularities.append((transactions[index][0], irregularity_type, description))
        #print(f"Applied {irregularity_type}: {description}")

    return applied_irregularities

def apply_cumulative_irregularity(transactions, config):
    """
    Apply cumulative irregularity to the transactions based on the configuration.

    This function applies a cumulative irregularity to a subset of transactions.
    The number of affected transactions is determined by the 'count' specified
    in the configuration. The irregularity increases transaction amounts slightly,
    stopping when either the count is reached or a cumulative threshold is exceeded.

    Args:
        transactions (list): A list of transaction records to potentially modify.
        config (dict): The configuration dictionary containing irregularity settings.

    Returns:
        list: A list of tuples, each containing:
            - transaction_id (str): The ID of the modified transaction.
            - irregularity_type (str): Always 'cumulative_irregularity'.
            - description (str): A description of the modification made.

    The function uses the following configuration parameters:
        - irregularities.cumulative_irregularity.enabled (bool): Whether to apply this irregularity.
        - irregularities.cumulative_irregularity.count (int): Maximum number of transactions to modify.
        - irregularities.cumulative_irregularity.threshold (float): Cumulative increase limit as a fraction of total expenses.

    If the cumulative irregularity is not enabled in the config, an empty list is returned.
    """
    applied_irregularities = []
    irregularity_config = config.get('irregularities', {}).get('cumulative_irregularity', {})
    if not irregularity_config.get('enabled', False):
        return applied_irregularities

    count = irregularity_config.get('count', 0)
    total_expenses = sum(t[3] for t in transactions if t[2] in ['Purchase', 'Payment'])
    threshold = total_expenses * irregularity_config.get('threshold', 0.005)
    cumulative_irregular = 0

    for transaction in transactions:
        if len(applied_irregularities) >= count:
            break
        if transaction[2] in ['Purchase', 'Payment']:
            irregular_amount = round(random.uniform(1, 10), 2)
            transaction[3] += irregular_amount
            cumulative_irregular += irregular_amount
            applied_irregularities.append((transaction[0], 'cumulative_irregularity', f"Amount increased by {irregular_amount:.2f}"))
            if cumulative_irregular > threshold:
                break

    return applied_irregularities

# Irregularity functions
def high_amount(transactions, index, config):
    """
    Apply high amount irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    original_amount = transactions[index][3]
    transactions[index][3] = round(random.uniform(50000, 100000), 2)
    return f"Amount increased from {original_amount:.2f} to {transactions[index][3]:.2f}"

def frequency_change(transactions, index, config):
    """
    Apply frequency change irregularity to a recurring transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    if any(rt['description'] in transactions[index][5] for rt in config.get('recurring_transactions', [])):
        original_date = transactions[index][1]
        new_day = random.randint(1, 28)
        transactions[index][1] = transactions[index][1][:8] + f"{new_day:02d}"
        return f"Date changed from {original_date} to {transactions[index][1]}"
    return "No change (not a recurring transaction)"

def double_spend(transactions, index, config):
    """
    Apply double spend irregularity by duplicating a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to duplicate.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    duplicate = transactions[index].copy()
    duplicate[0] = generate_transaction_id()
    original_date = duplicate[1]
    duplicate[1] = (datetime.strptime(duplicate[1], '%Y-%m-%d') + timedelta(minutes=random.randint(1, 60))).strftime('%Y-%m-%d %H:%M')
    transactions.append(duplicate)
    return f"Transaction duplicated with new ID {duplicate[0]} and date changed from {original_date} to {duplicate[1]}"

def missing_id(transactions, index, config):
    """
    Apply missing ID irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    original_id = transactions[index][0]
    transactions[index][0] = ''
    return f"Transaction ID removed (original ID: {original_id})"

def incorrect_date(transactions, index, config):
    """
    Apply incorrect date irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    original_date = transactions[index][1]
    future_date = config['end_date'] + timedelta(days=random.randint(1, 30))
    transactions[index][1] = future_date.strftime('%Y-%m-%d')
    return f"Date changed from {original_date} to future date {transactions[index][1]}"

def mismatched_description(transactions, index, config):
    """
    Apply mismatched description irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    original_description = transactions[index][5]
    if transactions[index][2] == 'Deposit':
        transactions[index][5] = 'Withdrawal - Miscellaneous'
    elif transactions[index][2] == 'Withdrawal':
        transactions[index][5] = 'Deposit - Miscellaneous'
    return f"Description changed from '{original_description}' to '{transactions[index][5]}'"

def wrong_account(transactions, index, config):
    """
    Apply wrong account irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    original_account = transactions[index][4]
    transactions[index][4] = f"WRONG-{random.randint(100, 999)}"
    return f"Account number changed from {original_account} to {transactions[index][4]}"

def personal_expense(transactions, index, config):
    """
    Apply personal expense irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    personal_vendors = config.get('personal_vendors', ["Personal Vendor"])
    personal_descriptions = config.get('personal_expense_descriptions', ["Personal Expense"])
    original_vendor = transactions[index][6]
    original_description = transactions[index][5]
    original_amount = transactions[index][3]
    transactions[index][6] = random.choice(personal_vendors)
    transactions[index][5] = random.choice(personal_descriptions)
    transactions[index][3] = round(random.uniform(100, 5000), 2)
    return f"Changed to personal expense: Vendor from '{original_vendor}' to '{transactions[index][6]}', " \
           f"Description from '{original_description}' to '{transactions[index][5]}', " \
           f"Amount from {original_amount:.2f} to {transactions[index][3]:.2f}"

def benford_violation(transactions, index, config):
    """
    Apply Benford's Law violation irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    original_amount = transactions[index][3]
    first_digit = random.choice([5, 6])
    rest_digits = random.randint(0, 999999)
    transactions[index][3] = float(f"{first_digit}.{rest_digits:06d}") * 1000
    return f"Amount changed from {original_amount:.2f} to {transactions[index][3]:.2f} (violating Benford's Law)"

def subtle_skimming(transactions, index, config):
    """
    Apply subtle skimming irregularity to a set of transactions.

    Args:
        transactions (list): The list of transactions.
        index (int): The starting index of the transactions to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    affected_transactions = []
    for i in range(index, min(index + 10, len(transactions))):
        original_amount = transactions[i][3]
        transactions[i][3] *= 0.99
        affected_transactions.append(f"Transaction {transactions[i][0]}: {original_amount:.2f} to {transactions[i][3]:.2f}")
    return f"Subtle skimming applied to {len(affected_transactions)} transactions: " + ", ".join(affected_transactions)

def seasonal_anomaly(transactions, index, config):
    """
    Apply seasonal anomaly irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    date_str = transactions[index][1]
    # Handle potential time component in the date string
    if ' ' in date_str:
        date_str = date_str.split(' ')[0]  # Take only the date part
    
    transaction_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    if transaction_date.month in [1, 2, 12]:  # Winter months
        original_description = transactions[index][5]
        original_amount = transactions[index][3]
        transactions[index][5] = "Summer Equipment Purchase"
        transactions[index][3] = round(random.uniform(5000, 10000), 2)
        return f"Seasonal anomaly: Description changed from '{original_description}' to '{transactions[index][5]}', " \
               f"Amount changed from {original_amount:.2f} to {transactions[index][3]:.2f} during winter month"
    return "No change (not in winter months)"


def round_number_bias(transactions, index, config):
    """
    Apply round number bias irregularity to a transaction.

    Args:
        transactions (list): The list of transactions.
        index (int): The index of the transaction to modify.
        config (dict): The configuration dictionary.

    Returns:
        str: Description of the applied irregularity.
    """
    original_amount = transactions[index][3]
    transactions[index][3] = round(transactions[index][3], -2)  # Round to nearest 100
    return f"Amount rounded from {original_amount:.2f} to {transactions[index][3]:.2f}"

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

def save_irregularities_to_csv(irregularities, filename):
    """
    Save the list of irregularities to a CSV file.

    Args:
        irregularities (list): The list of irregularities to save.
        filename (str): The name of the output CSV file.

    Returns:
        None: This function writes to a file.
    """
    print(f"Saving {len(irregularities)} irregularities to {filename}")
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Transaction ID', 'Irregularity Type', 'Description'])
        writer.writerows(irregularities)
    print(f"Finished saving irregularities to {filename}")

def generate_transactions(config):
    transactions = []
    transactions.extend(generate_recurring_transactions(config))
    transactions.extend(generate_random_transactions(config))
    
    irregularities = []
    double_spend_count = 0
    for irregularity in apply_irregularities(transactions, config):
        if irregularity[1] == 'double_spend':
            double_spend_count += 1
        irregularities.append(irregularity)
    
    cumulative_irregularities = apply_cumulative_irregularity(transactions, config)
    if cumulative_irregularities:
        irregularities.extend(cumulative_irregularities)

    print(f"Double spend irregularities: {double_spend_count}")
    print(f"Other irregularities: {len(irregularities) - double_spend_count}")
    print(f"Cumulative irregularities: {len(cumulative_irregularities)}")
    
    return sorted(transactions, key=lambda x: x[1]), irregularities

def main():
    """
    The main function to run the script.

    This function parses command-line arguments, loads the configuration,
    generates transactions, and saves them to CSV files.

    Returns:
        None: This function executes the script's main logic.
    """
    parser = argparse.ArgumentParser(description="Generate fake transaction data with configurable irregularities.")
    parser.add_argument('-c', '--config', default='config.json', help='Path to the configuration file')
    parser.add_argument('-o', '--output', default='fake_transactions.csv', help='Output CSV file name for transactions')
    parser.add_argument('-a', '--anomalies', default='irregularities.csv', help='Output CSV file name for irregularities')
    args = parser.parse_args()

    config = load_config(args.config)
    transactions, irregularities = generate_transactions(config)
    
    print(f"Number of irregularities before saving: {len(irregularities)}")
    #print(f"First few irregularities: {irregularities[:5]}")  # Print the first 5 irregularities

    save_to_csv(transactions, args.output)
    save_irregularities_to_csv(irregularities, args.anomalies)

    print(f"{len(transactions)} fake transactions have been generated and saved to '{args.output}'")
    print(f"{len(irregularities)} irregularities have been logged and saved to '{args.anomalies}'")

if __name__ == "__main__":
    main()