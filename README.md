# Fake Transaction Data Generator

## Overview

This Python script generates a dataset of fake financial transactions, designed for audit training and testing purposes. It creates a CSV file containing a mix of normal transactions and various types of irregularities, ranging from simple anomalies to sophisticated patterns that require advanced analytical techniques to detect.

It creates two CSV files:
- A file containing a mix of normal transactions and various types of irregularities.
- A file listing all the irregularities applied, including their types and descriptions.

## Features

- Generates a configurable number of transactions over a specified date range
- Includes both recurring and random transactions
- Implements Benford's Law for realistic amount distribution
- Introduces a variety of configurable irregularities and anomalies
- Provides a separate log of all applied irregularities for easy reference
- Flexible and modular design

## Requirements

- Python 3.6 or higher
- No additional libraries required (uses only Python standard library)

## Installation

1. Clone this repository or download the `generate_transactions.py` script.
2. Ensure you have Python 3.6 or higher installed on your system.

## Usage

1. Create a configuration file (e.g., config.json) with your desired settings.
2. Run the script using the following command:

    ```
    python generate_transactions.py -c config.json -o transactions.csv -a irregularities.csv
    ```

    - `-c` or `--config`: Path to the configuration file (default: 'config.json')
    - `-o` or `--output`: Name of the output CSV file for transactions (default: 'fake_transactions.csv')
    - `-a` or `--anomalies`: Name of the output CSV file for irregularities (default: 'irregularities.csv')

    The script will generate transactions based on your configuration and save them to the specified output files.

## Output Files

1. Transactions CSV file:
   - Columns: Transaction ID, Date, Type, Amount, Account, Description, Vendor

2. Irregularities CSV file:
   - Columns: Transaction ID, Irregularity Type, Description

The irregularities file provides a detailed log of all anomalies introduced into the dataset, making it easier to validate detection algorithms or train auditors.

## Configuration

The `config.json` file allows you to customize various aspects of the generated data. Here's an example structure:

```json
{
    "num_transactions": 1000,
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "irregularities": {
        "high_amount": {
            "count": 10
        },
        "frequency_change": {
            "count": 10
        },
        "double_spend": {
            "count": 10
        },
        "missing_id": {
            "count": 2
        },
        "incorrect_date": {
            "count": 10
        },
        "mismatched_description": {
            "count": 10
        },
        "wrong_account": {
            "count": 10
        },
        "personal_expense": {
            "count": 10
        },
        "benford_violation": {
            "count": 10
        },
        "subtle_skimming": {
            "count": 30
        },
        "seasonal_anomaly": {
            "count": 10
        },
        "round_number_bias": {
            "count": 10
        },
        "cumulative_irregularity": {
            "enabled": true,
            "count": 36,
            "threshold": 0.005
        }
    },
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
        {
            "vendor": "City Power & Utilities",
            "amount": 500,
            "day": 15,
            "description": "Monthly Utility Bill"
        },
        {
            "vendor": "Prime Office Rentals",
            "amount": 2000,
            "day": 1,
            "description": "Office Rent"
        }
    ]
}
```

In this configuration:
- `total` sets the total number of irregularities to generate
- Each irregularity type has a `count` field to specify how many of that type to generate
- If the sum of individual counts is less than `total`, additional random irregularities will be added to reach the total
- `cumulative_irregularity` has its own configuration with `enabled`, `threshold`, and `probability` fields

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