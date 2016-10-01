import mysql.connector
from datetime import date, datetime, timedelta


class DatabaseClient(object):
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', host='localhost', database='finances', password='kasa')
        self.contractors_table_name = 'contractors'
    def _insert_into_table(self, add_query, add_data):
        cursor = self.cnx.cursor()
        cursor.execute(add_query, add_data)
        self.cnx.commit()
        cursor.close()

    def insert_contractor(self, contractor_record):
        add_contractor = \
            ("INSERT INTO {} "
             "(contractor_name) "
             "VALUES (%(contractor_name)s)".format(self.contractors_table_name))
        try:
            self._insert_into_table(add_contractor, contractor_record)
        except mysql.connector.errors.IntegrityError as e:
            if e.errno == 1062:
                print "Contractor with name {} is present in contractors table. Will not duplicate database entry.".format(
                    contractor_record['contractor_name'])

        # contractor_id_query = \
        #     ("SELECT * FROM contractors WHERE contractor_name = 'Ryszard Lubicz'"
        #      )
        # cursor = self.cnx.cursor()
        # x = cursor.execute(contractor_id_query, contractor_record['contractor_name'])
        # pass


    def insert_transaction(self, transaction_record):
        """

        :param transaction_record:
        :type transaction_record: TransactionRecord
        :return:
        """
        add_transaction = \
            ("INSERT INTO operations "
             "(date, amount) "
             "VALUES (%s, %s)")
        cursor = self.cnx.cursor()
        cursor.execute(add_transaction)

class TransactionRecord(dict):
    def __init__(self, operator, transaction_date, amount):
        super(TransactionRecord, self).__init__(operator=operator, transaction_date=transaction_date, amount=amount)

class ContractorRecord(dict):
    def __init__(self, contractor_name):
        self.table_name = 'contractors'
        super(ContractorRecord, self).__init__(contractor_name=contractor_name)
if __name__ == '__main__':
    pass
    # query = (
    #     "CREATE TABLE `operations` ("
    #     "  `operation_id` int(11) NOT NULL AUTO_INCREMENT,"
    #     "  `date` date NOT NULL,"
    #     "  `amount` float NOT NULL,"
    #     "  `contractor_id` int NOT NULL,"
    #     "  `operator_id` int NOT NULL,"
    #     "  PRIMARY KEY (`operation_id`)"
    #     ") ENGINE=InnoDB")
    # db_client = DatabaseClient()
    # cursor = db_client.cnx.cursor()
    # cursor.execute(query)
    tr = TransactionRecord(operator='Ja')
    pass