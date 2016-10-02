import mysql.connector


class BankRecordsAquisition(object):
    def __init__(self):
        self.contractors_handler = ContractorsHandler()

    def aquire(self, bank_record):
        self.contractors_handler.handle_bank_record(bank_record)


class DatabaseTableHandler(object):
    def __init__(self, table_name):
        self.cnx = mysql.connector.connect(user='root', host='localhost', database='finances', password='kasa')
        self.table_name = table_name

    def handle_bank_record(self, bank_record):
        raise NotImplementedError

    def _insert_into_table(self, add_query, add_data):
        """
        :param add_query: insert MYSQL query
        :param add_data: dict or tuple of inserted data
        """
        cursor = self.cnx.cursor()
        cursor.execute(add_query, add_data)
        self.cnx.commit()
        cursor.close()


class ContractorsHandler(DatabaseTableHandler):
    def __init__(self):
        super(ContractorsHandler, self).__init__('contractors')

    def handle_bank_record(self, bank_record):
        """
        :type bank_record:
        """
        contractor_record = ContractorRecord(bank_record)
        self._add_to_database(contractor_record)
        contractor_id = self._get_contractor_id(contractor_record['contractor_name'])
        return contractor_id

    def _add_to_database(self, contractor_record):
        add_contractor = \
            ("INSERT INTO {} "
             "(contractor_name) "
             "VALUES (%(contractor_name)s)".format(self.table_name))
        try:
            self._insert_into_table(add_contractor, contractor_record)
        except mysql.connector.errors.IntegrityError as e:
            if e.errno == 1062:
                print "Contractor with name {} is present in contractors table. Will not duplicate database entry.".format(
                    contractor_record['contractor_name'])

    def _get_contractor_id(self, contractor_name):

        contractor_id_query = \
            ("SELECT contractor_id FROM contractors WHERE contractor_name = %s"
             )
        cursor = self.cnx.cursor()
        cursor.execute(contractor_id_query, (contractor_name,))
        contractor_id = [contractor_id for contractor_id in cursor][0]
        return contractor_id


class BankRecord(dict):
    def __init__(self, operator, transaction_date, contractor_name, transaction_title, transaction_type, transaction_id,
                 amount, currency, balance_after_transaction):
        super(BankRecord, self).__init__(
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


class TransactionRecord(dict):
    def __init__(self, bank_record):
        super(TransactionRecord, self).__init__(
            operator=bank_record.operator,
            transaction_date=bank_record.transaction_date,
            amount=bank_record.amount
        )


class ContractorRecord(dict):
    def __init__(self, bank_record):
        super(ContractorRecord, self).__init__(
            contractor_name=bank_record['contractor_name']
        )
