# Bank Statement PDF to CSV Converter

This repository contains a Python script that extracts transaction data from bank statement PDFs and exports it to a CSV file. This script is designed to work with bank statements that follow a specific structure and naming conventions as described below.

## Bank Statement Structure

The script is designed to process bank statements with the following fields for each transaction:

### Recipient Information
- **Címzett neve**: The name of the transaction recipient.
- **Címzett számlaszáma**: The bank account number of the recipient.
- **Terhelés összege**: The amount debited in the transaction.
- **Értéknap**: The value date of the transaction.
- **Közlemény**: The narrative or message attached to the transaction.
- **Megjegyzés**: Any additional comments regarding the transaction.
- **Partnerek közti egyedi azonosító**: A unique identifier for the transaction between partners.

### Payer Information
- **Megbízó neve**: The name of the transaction payer.
- **Megbízó számlaszáma**: The bank account number of the payer.
- **Jóváírás összege**: The amount credited in the transaction.
- **Partnerek közt egyedi azonosító**: A unique identifier for the transaction between partners.

### Additional Extracted Fields
- **Tranzakció dátum**: The date and time when the transaction took place.
- **Üzleti partner**: Business partner involved in the transaction.

## CSV Output Details

The resulting CSV file will have the following columns, which correspond to the fields listed above but translated to English:

- `RecipientName`: The name of the recipient.
- `RecipientAccountNumber`: The account number of the recipient.
- `DebitAmount`: The amount debited from the payer's account.
- `DebitCurrency`: The currency of the debited amount.
- `Date`: The date value when the transaction is effective.
- `Notice`: The transaction narrative.
- `Comment`: Additional comments.
- `UniqueIdentifier`: Unique transaction identifier.
- `PayerName`: The name of the payer.
- `PayerAccountNumber`: The account number of the payer.
- `CreditAmount`: The amount credited to the recipient's account.
- `CreditCurrency`: The currency of the credited amount.
- `TransactionDate`: The date and time the transaction was processed.
- `BusinessPartner`: Business partner information from the transaction.

## Usage Instructions

### Prerequisites
- Ensure you have Python installed on your system.
- Install the required libraries using pip:
  ```bash
  pip install pdfplumber pandas
  ```

### Running the Script

1. Run the script with the following command:
   ```bash
   python your_script_name.py
   ```

2. The script will prompt you to enter the directory path of the PDFs and the year for the transactions.

3. Once the script runs successfully, it will produce a CSV file named `transactions_<year>.csv` in the current directory.

### Example
```
Enter the directory path where the bank statement PDFs are located: /path/to/pdf/directory
Enter the year for the transactions: 2025
```

The generated CSV file will be in the format `transactions_2025.csv`.

## Note

This script is tailored to extract information based on the specified field names in the bank statement. If your bank statement has a different format, you may need to modify the script to accommodate those changes.