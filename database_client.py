import mysql.connector

class DatabaseClient(object):
    def __init__(self):
        self.cnx = mysql.connector.connect(user='root', host='localhost', database='finances', password='kasa')

if __name__ == '__main__':
    query = (
        "CREATE TABLE `operations` ("
        "  `operation_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `date` date NOT NULL,"
        "  `amount` float NOT NULL,"
        "  `contractor_id` int NOT NULL,"
        "  `operator_id` int NOT NULL,"
        "  PRIMARY KEY (`operation_id`)"
        ") ENGINE=InnoDB")
    db_client = DatabaseClient()
    cursor = db_client.cnx.cursor()
    cursor.execute(query)