import pdfplumber
import re
import os
import pandas as pd

def extract_transaction_data(pdf_path):
    fields = {
        'recipient': [
            'Címzett neve',
            'Címzett számlaszáma',
            'Terhelés összege',
            'Értéknap',
            'Közlemény',
            'Megjegyzés',
            'Partnerek közti egyedi azonosító'
        ],
        'payer': [
            'Megbízó neve',
            'Megbízó számlaszáma',
            'Jóváírás összege',
            'Értéknap',
            'Közlemény',
            'Partnerek közti egyedi azonosító'
        ]
    }

    transactions = []
    
    # Open pdf file
    with pdfplumber.open(pdf_path) as pdf:
        # Combine all pages
        full_text = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
        full_text = '\n'.join(full_text)

        # Credit or debit
        transaction_blocks = re.split(r'\n(?=Címzett neve|Megbízó neve)', full_text)
        
        for block in transaction_blocks:
            transaction = {'recipient': {}, 'payer': {}}
            current_section = None
            
            for line in block.strip().split('\n'):
                line = line.strip()
                
                if line.startswith('Címzett neve'):
                    current_section = 'recipient'
                    key = 'Címzett neve'
                    value = line[len(key):].strip()
                    transaction[current_section][key] = value
                    continue
                    
                elif line.startswith('Megbízó neve'):
                    current_section = 'payer'
                    key = 'Megbízó neve'
                    value = line[len(key):].strip()
                    transaction[current_section][key] = value
                    continue
                    
                if current_section:
                    sorted_keys = sorted(fields[current_section], 
                                      key=lambda x: len(x), 
                                      reverse=True)
                    
                    for key in sorted_keys:
                        if line.startswith(key):
                            value = line[len(key):].strip()
                            # Seperate currency from number
                            if key in ['Terhelés összege', 'Jóváírás összege']: 
                                match = re.match(r'(-?[\d\s]+,\d{2})\s([A-Z]{3})', value)
                                if match:
                                    amount, currency = match.groups()
                                    transaction[current_section][key] = amount
                                    transaction[current_section][f"{key} deviza"] = currency
                                else:
                                    transaction[current_section][key] = value
                            elif key == 'Közlemény':
                                # Extract information from bank statement message
                                transaction[current_section][key] = value
                                match = re.search(r'(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2})', value)
                                if match:
                                    tDate = match.group(1)
                                    transaction[current_section]["Tranzakció dátum"] = tDate
                                match2 = re.search(r'(\d{4}\.\d{2}\.\d{2} \d{2}:\d{18}) (.+)', value)
                                if match2:
                                    businessPartner = match2.group(2)[10:]
                                    transaction[current_section]["Üzleti partner"] = businessPartner
                            else:
                                transaction[current_section][key] = value
                            break  

            if transaction['recipient'] or transaction['payer']:
                transactions.append(transaction)

    return transactions

def prepare_dataframe_for_export(transactions):
    flat_transactions = []
    for transaction in transactions:
        flat_transaction = {}
        for section, data in transaction.items():
            flat_transaction.update(data)
        flat_transactions.append(flat_transaction)

    df = pd.DataFrame(flat_transactions)

    # Rename columns
    column_mapping = {
        'Címzett neve': 'RecipientName',
        'Címzett számlaszáma': 'RecipientAccountNumber',
        'Terhelés összege': 'DebitAmount',
        'Értéknap': 'Date',
        'Közlemény': 'Notice',
        'Megjegyzés': 'Comment',
        'Partnerek közti egyedi azonosító': 'UniqueIdentifier',
        'Megbízó neve': 'PayerName',
        'Megbízó számlaszáma': 'PayerAccountNumber',
        'Jóváírás összege': 'CreditAmount',
        'Tranzakció dátum': 'TransactionDate',
        'Üzleti partner': 'BusinessPartner',
        'Terhelés összege deviza': 'DebitCurrency',
        'Jóváírás összege deviza': 'CreditCurrency'
    }

    df.rename(columns=column_mapping, inplace=True)
    return df

def process_directory(directory_path):
    all_transactions = []

    # Process all bank statements in dir
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            transactions = extract_transaction_data(pdf_path)
            all_transactions.extend(transactions)

    df = prepare_dataframe_for_export(all_transactions)

    # Sort by date
    df_sorted = df.sort_values(by='Date')
    return df_sorted

if __name__ == "__main__":
    # Request user to input the directory path
    directory_path = input("Enter the directory path where the bank statement PDFs are located: ")
    output_csv_path = f"transactions.csv"
    df_sorted = process_directory(directory_path)
    df_sorted.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"Transaction data has been exported to {output_csv_path}")