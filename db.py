import mysql.connector


class DatabaseClient(object):
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', host='localhost', database='finances', password='kasa')
        self.contractors_table_name = 'contractors'

    def add_contractor(self, contractor_info):
        add_contractor_query = \
            ("INSERT INTO {} "
             "(contractor_name) "
             "VALUES (%(contractor_name)s)".format(self.contractors_table_name))
        try:
            self._insert_into_table(add_contractor_query, contractor_info)
        except mysql.connector.errors.IntegrityError as e:
            if e.errno == 1062:
                print "Contractor with name {} is present in contractors table. Will not duplicate database entry.".format(
                    contractor_info['contractor_name'])

    def _get_contractor_id(self, contractor_name):

        contractor_id_query = \
            ("SELECT contractor_id FROM contractors WHERE contractor_name = %s"
             )
        cursor = self.cnx.cursor()
        cursor.execute(contractor_id_query, (contractor_name,))
        contractor_id = [contractor_id for contractor_id in cursor][0]
        return contractor_id

    def _insert_into_table(self, add_query, add_data):
        """
        :param add_query: insert MYSQL query
        :param add_data: dict or tuple of inserted data
        """
        cursor = self.cnx.cursor()
        cursor.execute(add_query, add_data)
        self.cnx.commit()
        cursor.close()


class TransactionInfo(dict):
    def __init__(self, operator, transaction_date, amount):
        super(TransactionInfo, self).__init__(
            operator=operator,
            transaction_date=transaction_date,
            amount=amount
        )


class ContractorInfo(dict):
    def __init__(self, contractor_name):
        super(ContractorInfo, self).__init__(
            contractor_name=contractor_name
        )

class SingleRecordsAccumulator(object):
    def __init__(self):
        self.database_client = DatabaseClient()
    def accumulate(self, ing_record):
        """

        :param ing_record:
        :return:
        """
        contractor_info = ing_record.formContractorInfo()
        self.database_client.add_contractor(contractor_info)

def accumulate_records(ing_records):
    """
    Method for accumulating info from the list of ing_records to database.

    :param ing_records: list of IngCsvRecord instances
    :type ing_records: list[IngCsvRecord]
    """
    single_records_accumulator = SingleRecordsAccumulator()
    for ing_record in ing_records:
        single_records_accumulator.accumulate(ing_record)
