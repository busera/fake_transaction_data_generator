# Fake Transaction Data Generator

## Overview

This Python script generates a dataset of fake financial transactions, designed for audit training and testing purposes. It creates a CSV file containing a mix of normal transactions and various types of irregularities, ranging from simple anomalies to sophisticated patterns that require advanced analytical techniques to detect.

## Features

- Generates a configurable number of transactions over a specified date range
- Includes both recurring and random transactions
- Implements Benford's Law for realistic amount distribution
- Introduces a variety of configurable irregularities and anomalies
- Highly flexible and modular design
- Detailed Google-style docstrings for all functions

## Requirements

- Python 3.6 or higher
- No additional libraries required (uses only Python standard library)

## Installation

1. Clone this repository or download the `generate_transactions.py` script.
2. Ensure you have Python 3.6 or higher installed on your system.

## Usage

1. Create a configuration file (e.g., `config.json`) with your desired settings.
2. Run the script using the following command:

   ```
   python generate_transactions.py -c config.json -o output.csv
   ```

   - `-c` or `--config`: Path to the configuration file (default: 'config.json')
   - `-o` or `--output`: Name of the output CSV file (default: 'fake_transactions.csv')

3. The script will generate transactions based on your configuration and save them to the specified output file.

## Configuration

The `config.json` file allows you to customize various aspects of the generated data. Here's an example structure:

```json
{
    "num_transactions": 10000,
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "irregularity_percentage": 0.05,
    "cumulative_threshold": 0.005,
    "enabled_irregularities": [
        "high_amount",
        "frequency_change",
        "double_spend",
        "missing_id",
        "incorrect_date",
        "mismatched_description",
        "wrong_account",
        "personal_expense",
        "benford_violation",
        "subtle_skimming",
        "seasonal_anomaly",
        "round_number_bias",
        "cumulative_irregularity"
    ],
    "vendors": [
        "ABC Office Supplies",
        "XYZ Tech Solutions",
        "123 Cleaning Services"
    ],
    "personal_vendors": [
        "Luxury Resort & Spa",
        "Designer Clothing Co.",
        "Gourmet Restaurant"
    ],
    "personal_expense_descriptions": [
        "Team Building Retreat",
        "Client Entertainment",
        "Office Decor"
    ],
    "recurring_transactions": [
        {"vendor": "City Power & Utilities", "amount": 500, "day": 15, "description": "Monthly Utility Bill"},
        {"vendor": "Prime Office Rentals", "amount": 2000, "day": 1, "description": "Office Rent"}
    ]
}
```

You can add or remove vendors, personal vendors, personal expense descriptions, and recurring transactions as needed. The script will adapt to these changes automatically.

## Output

The script generates a CSV file with the following columns:

1. Transaction ID
2. Date
3. Type
4. Amount
5. Account
6. Description
7. Vendor

## Types of Transactions and Irregularities

### Normal Transactions

- Recurring transactions (e.g., rent, utilities)
- Random transactions with amounts following Benford's Law

### Irregularities

1. High Amount: Unusually large transaction amounts
2. Frequency Change: Altered dates for recurring transactions
3. Double Spend: Duplicated transactions with slight time differences
4. Missing ID: Transactions with no ID
5. Incorrect Date: Future-dated transactions
6. Mismatched Description: Descriptions not matching transaction types
7. Wrong Account: Incorrect account number formats
8. Personal Expense: Personal expenses disguised as business expenses
9. Benford's Law Violation: Amounts not following Benford's Law distribution
10. Subtle Skimming: Slight reductions across multiple transactions
11. Seasonal Anomaly: Out-of-season transactions
12. Round Number Bias: Suspiciously round transaction amounts
13. Cumulative Irregularity: Small discrepancies spread across multiple transactions

## Key Functions

The script includes the following main functions:

- `generate_transaction_id()`: Generates a unique transaction ID
- `benford_amount()`: Generates an amount following Benford's Law
- `generate_recurring_transactions(config)`: Generates recurring transactions
- `generate_random_transactions(config)`: Generates random transactions
- `apply_irregularities(transactions, config)`: Applies various irregularities to transactions
- `apply_cumulative_irregularity(transactions, config)`: Applies cumulative irregularity
- `load_config(config_file)`: Loads and parses the configuration file
- `save_to_csv(transactions, filename)`: Saves transactions to a CSV file
- `generate_transactions(config)`: Orchestrates the entire transaction generation process

Each irregularity type also has its own function (e.g., `high_amount()`, `frequency_change()`, etc.).

## Customization

You can easily customize the script by:

- Modifying the configuration file to change transaction parameters, vendors, etc.
- Adding new irregularity types by defining new functions and adding them to the `irregularity_functions` dictionary in `apply_irregularities()`
- Adjusting the logic in existing irregularity functions to match specific scenarios

## Purpose and Use Cases

This dataset is designed for:

- Training auditors and financial analysts
- Testing fraud detection algorithms
- Practicing data analysis and visualization techniques
- Developing and validating audit procedures

## Note

The transactions and irregularities in this dataset are entirely fictional and generated for educational and testing purposes only. They do not represent real financial data or actual fraudulent activities.

## Contributing

Feel free to fork this project and submit pull requests with improvements or additional features. Some ideas for enhancements:

- Add more types of irregularities
- Implement additional configuration options
- Create visualizations of the generated data
- Develop companion analysis tools

## License

This project is open-source and available under the MIT License.