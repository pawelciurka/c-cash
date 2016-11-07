import input_read
import db
from datetime import date, datetime, timedelta


def load_ing_records(ing_csv_file_path):
    # bank_records = input_read.read_ing_history(ing_csv_file_path)
    ing_records = [
        IngCsvRecord('Jan Kazimierz', date(1999, 7, 14), 'Zabka', 'Zakup', 'przelew', 11, 12.5, 'PLN', 13.0),
        IngCsvRecord('Roman Dmowski', date(1999, 5, 16), 'Rossmann', 'Zakup', 'przelew', 11, 12.5, 'PLN', 13.0)
    ]
    return ing_records


class IngCsvRecord(dict):
    def __init__(self, operator, transaction_date, contractor_name, transaction_title, transaction_type, transaction_id,
                 amount, currency, balance_after_transaction):
        super(IngCsvRecord, self).__init__(
            operator=operator,
            transaction_date=transaction_date,
            contractor_name=contractor_name,
            transaction_title=transaction_title,
            transaction_type=transaction_type,
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            balance_after_transaction=balance_after_transaction
        )

    def formContractorInfo(self):
        return db.ContractorInfo(self['contractor_name'])
