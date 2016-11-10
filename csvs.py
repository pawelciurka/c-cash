import db
import csv
from datetime import date, datetime, timedelta
from unidecode import unidecode
import tempfile
from collections import OrderedDict

def read_ing_csv(ing_csv_file_path):
    converted_file_path = convert_english_to_polish(ing_csv_file_path)
    ing_records = extract_transactions_from_csv(converted_file_path, 'Anonymous')

    return ing_records

def convert_english_to_polish(ing_csv_file_path):
    with open(ing_csv_file_path) as f:
        text = f.read()
    result = ''
    for i in text:
        try:
            result += i.encode('1252').decode('1252')
        except (UnicodeEncodeError, UnicodeDecodeError):
            result += unidecode(i)
    with tempfile.TemporaryFile(suffix='.csv', delete=False) as f:
        f.write(result)
        converted_file_path = f.name
    return converted_file_path

def extract_transactions_from_csv(ing_csv_file_path, operator):
    with open(ing_csv_file_path, "r") as f:
        f.seek(0)
        for _ in range(18):
            next(f)
        d_reader = csv.DictReader(f, delimiter=';')
        ing_records = []
        for row in d_reader:
            if row['Saldo po transakcji'] is None:
                continue
            try:
                amount = float(row['Kwota transakcji (waluta rachunku)'].replace(',', '.'))
            except:
                amount = 0
            balance_after_transaction = float(row['Saldo po transakcji'].replace(',', '.'))
            transaction_date = datetime.strptime(row['Data transakcji'], '%d.%m.%Y' )
            if amount<0:
                transaction_type = 'EXPENSE'
            else:
                transaction_type = 'INCOME'
            ing_record = IngRecord(
                operator=operator,
                transaction_date=transaction_date,
                contractor_name=row['Dane kontrahenta'],
                transaction_title=row['Tytu3'],
                transaction_type=transaction_type,
                transaction_id=row['Nr transakcji'],
                amount=amount,
                currency=row['Waluta'],
                balance_after_transaction=balance_after_transaction
            )
            ing_records.append(ing_record)
    return ing_records


class IngRecord(OrderedDict):
    def __init__(self, operator, transaction_date, contractor_name, transaction_title, transaction_id, transaction_type,
                 amount, currency, balance_after_transaction):
        super(IngRecord, self).__init__(
            operator=operator,
            transaction_date=transaction_date,
            contractor_name=contractor_name,
            transaction_title=transaction_title,
            transaction_id=transaction_id,
            transaction_type=transaction_type,
            amount=amount,
            currency=currency,
            balance_after_transaction=balance_after_transaction
        )

    def formContractorInfo(self):
        return db.ContractorInfo(self['contractor_name'])
