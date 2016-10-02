import input_read
import db
from datetime import date, datetime, timedelta

def load_from_ing_file(ing_csv_file_path):
    # bank_records = input_read.read_ing_history(ing_csv_file_path)
    bank_records = [
        db.BankRecord('Jan Kazimierz', date(1999, 7, 14), 'Zabka', 'Zakup', 'przelew', 11, 12.5, 'PLN', 13.0),
        db.BankRecord('Roman Dmowski', date(1999, 5, 16), 'Rossmann', 'Zakup', 'przelew', 11, 12.5, 'PLN', 13.0)
    ]
    bank_records_aquisition = db.BankRecordsAquisition()
    for bank_record in bank_records:
        bank_records_aquisition.aquire(bank_record)

